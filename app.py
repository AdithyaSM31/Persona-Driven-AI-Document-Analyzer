# app.py - Flask Web Application for Persona AI Document Analyzer
import os
import json
import fitz  # PyMuPDF
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import time
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = './uploads'
MODEL_PATH = './model'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model once at startup
model = None

def load_model():
    global model
    if model is None:
        try:
            model = SentenceTransformer(MODEL_PATH)
            print("Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            model = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_structure_from_pdf(pdf_path):
    """Extract structure and content from PDF"""
    doc = fitz.open(pdf_path)
    outline = []
    full_text_sections = {}

    # Try to get structure from Table of Contents
    toc = doc.get_toc()
    if toc:
        for level, title, page_num in toc:
            title = title.strip()
            if not title:
                continue

            level_str = f"H{level}"
            section_entry = {"level": level_str, "text": title, "page": page_num}
            outline.append(section_entry)

            page = doc.load_page(page_num - 1)
            full_text_sections[title] = page.get_text("text")
    else:
        # Fallback: create single entry for whole document
        title = os.path.basename(pdf_path).replace('.pdf', '')
        outline.append({"level": "H1", "text": title, "page": 1})

        all_text = ""
        for page in doc:
            all_text += page.get_text("text") + "\n"
        full_text_sections[title] = all_text

    doc.close()
    title = os.path.basename(pdf_path)
    return {"title": title, "outline": outline}, full_text_sections

def analyze_documents(pdf_files, persona, job_to_be_done):
    """Main analysis function"""
    if model is None:
        return {"error": "Model not loaded. Please run download_model.py first."}

    start_time = time.time()

    # Generate query embedding
    query_text = f"Persona: {persona}. Task: {job_to_be_done}"
    query_embedding = model.encode(query_text)

    all_sections = []

    for pdf_file in pdf_files:
        structure, content = extract_structure_from_pdf(pdf_file)

        if not structure["outline"]:
            continue

        # Combine section title with full text
        section_texts_for_embedding = [
            item["text"] + " " + content.get(item["text"], "")
            for item in structure["outline"]
        ]

        section_embeddings = model.encode(section_texts_for_embedding)

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
            "processing_time": round(time.time() - start_time, 2)
        },
        "extracted_sections": [],
        "sub_section_analysis": []
    }

    # Get top 5 sections
    for i, section in enumerate(ranked_sections[:5]):
        output_data["extracted_sections"].append({
            "document": section["document"],
            "section_title": section["section_title"],
            "importance_rank": i + 1,
            "page_number": section["page"],
            "relevance_score": round(section["score"] * 100, 2)
        })

        refined_text = section["full_text"].strip().replace("\n", " ")
        if not refined_text:
            refined_text = "Content for this section is not available."

        output_data["sub_section_analysis"].append({
            "document": section["document"],
            "refined_text": refined_text[:500] + "..." if len(refined_text) > 500 else refined_text,
            "page_number": section["page"]
        })

    return output_data

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint for document analysis"""
    try:
        print("\n=== New Analysis Request ===")
        print(f"Request files: {request.files}")
        print(f"Request form: {request.form}")
        
        # Check if files are in the request
        if 'files[]' not in request.files:
            print("Error: No files uploaded")
            return jsonify({"error": "No files uploaded"}), 400

        files = request.files.getlist('files[]')
        persona = request.form.get('persona', '')
        job_to_be_done = request.form.get('job_to_be_done', '')

        print(f"Files received: {len(files)}")
        print(f"Persona: {persona}")
        print(f"Job to be done: {job_to_be_done}")

        if not persona or not job_to_be_done:
            print("Error: Missing persona or job_to_be_done")
            return jsonify({"error": "Persona and job to be done are required"}), 400

        if not files or files[0].filename == '':
            print("Error: No files selected")
            return jsonify({"error": "No files selected"}), 400

        # Save uploaded files
        pdf_paths = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                pdf_paths.append(filepath)
                print(f"Saved file: {filepath}")

        if not pdf_paths:
            print("Error: No valid PDF files")
            return jsonify({"error": "No valid PDF files uploaded"}), 400

        print(f"Starting analysis of {len(pdf_paths)} files...")
        # Analyze documents
        results = analyze_documents(pdf_paths, persona, job_to_be_done)

        # Clean up uploaded files
        for filepath in pdf_paths:
            try:
                os.remove(filepath)
                print(f"Cleaned up: {filepath}")
            except Exception as e:
                print(f"Failed to clean up {filepath}: {e}")

        print("Analysis complete!")
        return jsonify(results)

    except Exception as e:
        print(f"ERROR in analyze endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    })

if __name__ == '__main__':
    print("Starting Persona AI Document Analyzer...")
    print("Loading model...")
    load_model()
    if model:
        print("✓ Model loaded successfully!")
    else:
        print("⚠ Warning: Model not loaded. Please run 'python download_model.py' first.")
    print("\nStarting web server...")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
