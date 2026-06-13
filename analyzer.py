# analyzer.py - Shared Core Analysis Module for Persona AI Document Analyzer
# This module contains all the shared logic for PDF extraction, embedding,
# and ranking. It is imported by app.py, run.py, and api/index.py.

import os
import re
import time
import threading
import numpy as np
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# --- Thread-safe Model Management ---

_model = None
_model_lock = threading.Lock()
_model_loading = False


def load_model(model_path='./model'):
    """
    Load the sentence-transformer model in a thread-safe manner.
    Tries local path first, then downloads from HuggingFace.
    Returns the loaded model or None on failure.
    """
    global _model, _model_loading

    # Fast path: model already loaded
    if _model is not None:
        return _model

    with _model_lock:
        # Double-check after acquiring lock
        if _model is not None:
            return _model

        if _model_loading:
            return None

        _model_loading = True
        try:
            print("Loading model...")
            if os.path.exists(model_path):
                _model = SentenceTransformer(model_path)
                print("Model loaded from local path!")
            else:
                print("Downloading model (first time only)...")
                _model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
                print("Model downloaded and loaded!")
        except Exception as e:
            print(f"Error loading model: {e}")
            _model = None
        finally:
            _model_loading = False

    return _model


def get_model():
    """Get the current model instance (may be None if not loaded)."""
    return _model


# --- PDF Structure Extraction ---

def _is_likely_heading(text):
    """
    Heuristic check: is this text likely a section/recipe heading?
    Returns False for ingredient lines, instruction continuations, etc.
    """
    text = text.strip()
    if not text:
        return False

    # Too short or too long for a title
    if len(text) < 2 or len(text) > 80:
        return False

    # Starts with bullet/list markers → ingredient or instruction
    list_prefixes = ['•', '●', '○', '▪', '–', '—', '-', '*',
                     'o ', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.']
    for prefix in list_prefixes:
        if text.startswith(prefix):
            return False

    # Looks like a measurement/ingredient (starts with a number + unit pattern)
    if re.match(r'^\d+[\s/]', text):
        return False

    # Continuation text (starts with lowercase)
    if text[0].islower():
        return False

    # Instruction-like text (starts with a verb in imperative form)
    instruction_starters = [
        'Add ', 'Stir ', 'Mix ', 'Pour ', 'Cook ', 'Bake ', 'Preheat ',
        'Place ', 'Remove ', 'Serve ', 'Drain ', 'Let ', 'Heat ', 'Bring ',
        'Combine ', 'Whisk ', 'Return ', 'Scramble ', 'Season ', 'Set ',
        'Spread ', 'Top ', 'Fold ', 'Roll ', 'Cut ', 'Slice ', 'Chop '
    ]
    for starter in instruction_starters:
        if text.startswith(starter):
            return False

    return True


def _detect_page_title(page, page_text, page_num):
    """
    Detect the most likely title/heading on a page using font-size analysis.

    Strategy:
    1. Use PyMuPDF's text dict to find the largest font on the page — this
       is typically the recipe/section name.
    2. If font analysis fails or all text is same size, fall back to
       heuristic-based detection (first line that looks like a heading).
    3. Last resort: use "Page N" as the title.
    """
    try:
        # Extract text blocks with font information
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]

        # Collect all text spans with their font sizes
        text_by_size = {}
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    size = round(span["size"], 1)
                    if text and len(text) > 1:
                        if size not in text_by_size:
                            text_by_size[size] = []
                        text_by_size[size].append(text)

        if text_by_size:
            # Get the largest font size
            max_size = max(text_by_size.keys())
            sizes = sorted(text_by_size.keys(), reverse=True)

            # Check if largest font is meaningfully bigger than body text
            if len(sizes) >= 2 and max_size > sizes[1] * 1.1:
                # There's a distinctly larger font — use it as title
                heading_texts = text_by_size[max_size]
                title = " ".join(heading_texts).strip()
                if title and _is_likely_heading(title):
                    return title[:80] if len(title) > 80 else title
    except Exception:
        pass

    # Fallback: find the first line that looks like a heading
    lines = [line.strip() for line in page_text.split('\n') if line.strip()]
    for line in lines[:5]:  # Check first 5 lines
        # Clean bullet prefixes
        clean = line
        for prefix in ['• ', '● ', '○ ', '▪ ']:
            if clean.startswith(prefix):
                clean = clean[len(prefix):].strip()

        if _is_likely_heading(clean):
            return clean[:80] if len(clean) > 80 else clean

    # Last resort
    return f"Section (Page {page_num + 1})"


def extract_structure_from_pdf(pdf_path):
    """
    Extract structure and content from a PDF document.

    Strategy:
    1. If the PDF has a Table of Contents (TOC), use it and extract text
       across the full page range of each section (not just the first page).
    2. If no TOC, use a smart per-page fallback: each page becomes its own
       section, with the first non-empty line as the section title. This is
       critical because most real-world PDFs (like recipe collections) lack
       a TOC, and treating the entire document as one section destroys
       ranking granularity.
    """
    doc = fitz.open(pdf_path)
    outline = []
    full_text_sections = {}

    toc = doc.get_toc()

    if toc:
        # --- Strategy 1: Use TOC with multi-page text extraction ---
        valid_toc = [(level, title.strip(), page_num)
                     for level, title, page_num in toc if title.strip()]

        for idx, (level, title, page_num) in enumerate(valid_toc):
            # Determine the end page for this section:
            # It runs until the next TOC entry's page (exclusive) or end of doc
            if idx + 1 < len(valid_toc):
                end_page = valid_toc[idx + 1][2]  # next section's start page
            else:
                end_page = len(doc) + 1  # last section goes to end of doc

            # Extract text across the full page range
            section_text = ""
            for pg in range(page_num - 1, min(end_page - 1, len(doc))):
                section_text += doc.load_page(pg).get_text("text") + "\n"

            level_str = f"H{level}"
            outline.append({"level": level_str, "text": title, "page": page_num})
            full_text_sections[title] = section_text.strip()
    else:
        # --- Strategy 2: Per-page fallback with smart title detection ---
        seen_titles = {}  # Track duplicate titles to make them unique

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text("text").strip()

            if not page_text or len(page_text) < 20:
                # Skip near-empty pages (cover pages, blank pages)
                continue

            title = _detect_page_title(page, page_text, page_num)

            # Handle duplicate titles by appending page number
            if title in seen_titles:
                seen_titles[title] += 1
                title = f"{title} (p.{page_num + 1})"
            else:
                seen_titles[title] = 1

            outline.append({
                "level": "H2",
                "text": title,
                "page": page_num + 1
            })
            full_text_sections[title] = page_text

    doc.close()
    doc_title = os.path.basename(pdf_path)
    return {"title": doc_title, "outline": outline}, full_text_sections


# --- Analysis Engine ---

def build_query_embedding(model, persona, job_to_be_done):
    """
    Build a task-weighted query embedding.

    The task description is typically more specific and discriminative than
    the persona, so we weight it more heavily. We encode persona and task
    separately, then combine with a 30/70 weighting.
    """
    persona_embedding = model.encode(persona)
    task_embedding = model.encode(job_to_be_done)

    # Weight: 30% persona context, 70% specific task
    query_embedding = 0.3 * persona_embedding + 0.7 * task_embedding

    return query_embedding


def find_relevant_snippet(full_text, query_embedding, model, max_length=500):
    """
    Instead of blindly truncating to the first 500 chars, find the most
    relevant snippet by scoring sentences against the query.
    Falls back to the beginning of the text if the text is short.
    """
    if len(full_text) <= max_length:
        return full_text.strip().replace("\n", " ")

    # Split into sentences/chunks (rough splitting by double newline or period)
    paragraphs = [p.strip() for p in full_text.split('\n\n') if p.strip()]

    if len(paragraphs) <= 1:
        # Can't split further, return truncated
        clean = full_text.strip().replace("\n", " ")
        return clean[:max_length] + "..."

    # Score each paragraph against the query
    try:
        para_embeddings = model.encode(paragraphs)
        similarities = cosine_similarity([query_embedding], para_embeddings)[0]

        # Get paragraphs sorted by relevance
        ranked = sorted(zip(similarities, paragraphs), reverse=True)

        # Build snippet from most relevant paragraphs
        snippet = ""
        for _, para in ranked:
            clean_para = para.replace("\n", " ").strip()
            if len(snippet) + len(clean_para) + 2 <= max_length:
                snippet += clean_para + " "
            else:
                remaining = max_length - len(snippet) - 3
                if remaining > 50:  # Only add if meaningful
                    snippet += clean_para[:remaining] + "..."
                break

        return snippet.strip() if snippet.strip() else full_text[:max_length].strip().replace("\n", " ") + "..."
    except Exception:
        # Fallback to simple truncation if embedding fails
        clean = full_text.strip().replace("\n", " ")
        return clean[:max_length] + "..."


def analyze_documents(pdf_files, persona, job_to_be_done, model_path='./model', top_n=5):
    """
    Main analysis pipeline.

    Args:
        pdf_files: List of paths to PDF files
        persona: User persona string
        job_to_be_done: Task description string
        model_path: Path to local model directory
        top_n: Number of top sections to return

    Returns:
        Dictionary with metadata, extracted_sections, and sub_section_analysis
    """
    # Load model
    current_model = load_model(model_path)
    if current_model is None:
        return {"error": "Model failed to load. Please try again."}

    start_time = time.time()

    # Generate task-weighted query embedding
    query_embedding = build_query_embedding(current_model, persona, job_to_be_done)

    all_sections = []

    for pdf_file in pdf_files:
        structure, content = extract_structure_from_pdf(pdf_file)

        if not structure["outline"]:
            continue

        # Combine section title with full text for better embedding context
        section_texts_for_embedding = [
            item["text"] + " " + content.get(item["text"], "")
            for item in structure["outline"]
        ]

        section_embeddings = current_model.encode(section_texts_for_embedding)

        if len(section_embeddings) == 0:
            continue

        similarities = cosine_similarity([query_embedding], section_embeddings)[0]

        for i, item in enumerate(structure["outline"]):
            all_sections.append({
                "document": os.path.basename(pdf_file),
                "page": item["page"],
                "section_title": item["text"],
                "score": float(similarities[i]),
                "full_text": content.get(item["text"], "")
            })

    ranked_sections = sorted(all_sections, key=lambda x: x["score"], reverse=True)

    # Prepare output
    output_data = {
        "metadata": {
            "input_documents": [os.path.basename(f) for f in pdf_files],
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "processing_time": round(time.time() - start_time, 2),
            "total_sections_analyzed": len(all_sections)
        },
        "extracted_sections": [],
        "sub_section_analysis": []
    }

    # Get top N sections
    for i, section in enumerate(ranked_sections[:top_n]):
        output_data["extracted_sections"].append({
            "document": section["document"],
            "section_title": section["section_title"],
            "importance_rank": i + 1,
            "page_number": section["page"],
            "relevance_score": round(section["score"] * 100, 2)
        })

        # Find the most relevant snippet instead of blind truncation
        refined_text = find_relevant_snippet(
            section["full_text"], query_embedding, current_model
        )
        if not refined_text:
            refined_text = "Content for this section is not available."

        output_data["sub_section_analysis"].append({
            "document": section["document"],
            "section_title": section["section_title"],
            "refined_text": refined_text,
            "page_number": section["page"]
        })

    return output_data
