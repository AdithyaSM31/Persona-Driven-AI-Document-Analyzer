# api/index.py - Vercel Serverless Function
import os
import sys
import tempfile
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Ensure parent directory is in path so we can import analyzer
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import shared analysis module
from analyzer import load_model, get_model, analyze_documents

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

# Configuration
ALLOWED_EXTENSIONS = {'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint for document analysis"""
    try:
        print("\n=== New Analysis Request ===")

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

        # Save uploaded files to temp directory (serverless-safe)
        pdf_paths = []
        for file in files:
            if file and allowed_file(file.filename):
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
                file.save(temp_file.name)
                pdf_paths.append(temp_file.name)
                print(f"Saved file: {temp_file.name}")

        if not pdf_paths:
            print("Error: No valid PDF files")
            return jsonify({"error": "No valid PDF files uploaded"}), 400

        print(f"Starting analysis of {len(pdf_paths)} files...")

        # Analyze documents using shared module
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
        "model_loaded": get_model() is not None,
        "ready": True
    })


# Vercel serverless function handler
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()


# For local testing
if __name__ == '__main__':
    print("Starting Persona AI Document Analyzer...")
    print("Loading model...")
    load_model()
    if get_model():
        print("✓ Model loaded successfully!")
    else:
        print("⚠ Warning: Model not loaded.")
    print("\nStarting web server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
