# run.py - Docker CLI Script for Persona AI Document Analyzer
# This script is used for the offline Docker-based command-line solution.
import os
import json
import time

# Import shared analysis module
from analyzer import analyze_documents

# --- CONFIGURATION ---
INPUT_DIR = "./input"
OUTPUT_DIR = "./output"
MODEL_PATH = "./model"


def run_persona_analysis():
    """
    Main CLI analysis pipeline.
    Reads persona/task from challenge1b_input.json, analyzes all PDFs
    in the input directory, and writes results to challenge1b_output.json.
    """
    # --- Load Input JSON ---
    input_json_path = os.path.join(INPUT_DIR, "challenge1b_input.json")
    try:
        with open(input_json_path, 'r') as f:
            input_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The input file was not found at {input_json_path}")
        return

    # --- Parse Persona and Task ---
    # Support both nested format (challenge spec) and flat format
    persona_field = input_data.get("persona", "")
    if isinstance(persona_field, dict):
        persona = persona_field.get("role", "Unknown Persona")
    else:
        persona = persona_field or "Unknown Persona"

    task_field = input_data.get("job_to_be_done", "")
    if isinstance(task_field, dict):
        job_to_be_done = task_field.get("task", "Unknown Task")
    else:
        job_to_be_done = task_field or "Unknown Task"

    print(f"Persona: {persona}")
    print(f"Task: {job_to_be_done}")

    # --- Collect PDF Files ---
    pdf_files = sorted([
        os.path.join(INPUT_DIR, f)
        for f in os.listdir(INPUT_DIR)
        if f.endswith(".pdf")
    ])

    if not pdf_files:
        print(f"Error: No PDF files found in {INPUT_DIR}")
        return

    print(f"Found {len(pdf_files)} PDF files")

    # --- Run Analysis (using shared module) ---
    start_time = time.time()
    results = analyze_documents(pdf_files, persona, job_to_be_done, model_path=MODEL_PATH)

    if "error" in results:
        print(f"Error: {results['error']}")
        return

    # --- Write Output ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_filename = "challenge1b_output.json"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)

    print(f"\nProcessing complete. Output written to {output_path}")
    print(f"Total execution time: {time.time() - start_time:.2f} seconds")
    print(f"Sections analyzed: {results['metadata'].get('total_sections_analyzed', 'N/A')}")


if __name__ == "__main__":
    run_persona_analysis()