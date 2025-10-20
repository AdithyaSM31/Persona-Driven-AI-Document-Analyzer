# 🎨 Persona AI Document Analyzer - Web UI

A modern, minimalist web interface for the Persona AI Document Analyzer built with Flask, HTML, CSS, and JavaScript.

## ✨ Features

- **Modern Minimalist Design**: Clean, intuitive interface with smooth animations
- **Drag & Drop Upload**: Easy PDF file upload with drag-and-drop support
- **Real-time Analysis**: Live processing feedback with loading states
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Interactive Results**: Beautiful visualization of analysis results with relevance scores
- **Multiple File Support**: Upload and analyze multiple PDF documents simultaneously

## 🚀 Quick Start

### 1. Install Dependencies

First, make sure you have Python 3.8+ installed, then install the required packages:

```powershell
pip install -r requirements.txt
```

### 2. Download the Model (One-time Setup)

Download the sentence-transformer model:

```powershell
python download_model.py
```

This will download the model files to the `./model/` directory.

### 3. Start the Web Server

Run the Flask application:

```powershell
python app.py
```

The server will start on `http://localhost:5000`

### 4. Open in Browser

Open your web browser and navigate to:

```
http://localhost:5000
```

## 📖 How to Use

1. **Enter Persona**: Describe the user persona (e.g., "Health-conscious home cook looking for quick meals")

2. **Describe Task**: Enter the job to be done (e.g., "Find main course dinner recipes that are easy to prepare")

3. **Upload PDFs**: 
   - Click the upload area to select files, or
   - Drag and drop PDF files directly onto the upload area

4. **Analyze**: Click the "Analyze Documents" button

5. **View Results**: 
   - See the top 5 most relevant sections ranked by importance
   - View detailed analysis with full text excerpts
   - See metadata including processing time and relevance scores

6. **New Analysis**: Click "New Analysis" to start over with different documents

## 🏗️ Project Structure

```
├── app.py                  # Flask web application
├── run.py                  # Original CLI analyzer
├── download_model.py       # Model download script
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Main HTML template
├── static/
│   ├── css/
│   │   └── styles.css     # CSS styling
│   └── js/
│       └── app.js         # JavaScript logic
├── uploads/               # Temporary upload directory
└── model/                 # Downloaded ML model (created by download_model.py)
```

## 🎨 UI Features

### Design Elements

- **Color Scheme**: Purple gradient background with clean white cards
- **Typography**: Inter font family for modern, readable text
- **Icons**: SVG icons for scalability and performance
- **Animations**: Smooth transitions and loading states
- **Shadows**: Subtle depth for visual hierarchy

### Responsive Breakpoints

- **Desktop**: Full layout with side-by-side elements
- **Tablet** (< 768px): Stacked layout with adjusted spacing
- **Mobile** (< 480px): Optimized for small screens

## 🔧 API Endpoints

### `GET /`
Returns the main HTML page

### `POST /api/analyze`
Analyzes uploaded PDF documents

**Request:**
- `files[]`: PDF files (multipart/form-data)
- `persona`: User persona description (string)
- `job_to_be_done`: Task description (string)

**Response:**
```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "...",
    "job_to_be_done": "...",
    "processing_timestamp": "2025-10-20T12:00:00Z",
    "processing_time": 2.45
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "section_title": "Section Name",
      "importance_rank": 1,
      "page_number": 3,
      "relevance_score": 85.5
    }
  ],
  "sub_section_analysis": [...]
}
```

### `GET /api/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## 🛠️ Technologies Used

### Backend
- **Flask 3.0**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **sentence-transformers**: ML embeddings
- **PyMuPDF**: PDF text extraction
- **scikit-learn**: Similarity calculations

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **Vanilla JavaScript**: No framework dependencies
- **Google Fonts**: Inter font family

## 🐛 Troubleshooting

### Model Not Loaded
If you see a warning about the model not being loaded:
```powershell
python download_model.py
```

### Port Already in Use
If port 5000 is already in use, you can change it in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Change port here
```

### File Upload Issues
- Make sure uploaded files are PDF format
- Maximum file size is 50MB per file
- Check that the `uploads/` directory exists and is writable

## 📝 License

This project was created for the Adobe Hackathon 2025 - Round 1B.

## 👥 Authors

- Mayank Chauhan
- Adithya Sankar Menon
- Piyush Maurya

## 🙏 Acknowledgments

Built with ❤️ for Adobe Hackathon 2025
