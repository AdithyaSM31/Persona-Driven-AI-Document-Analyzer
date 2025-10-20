# 🎬 Quick Demo Guide

## Running the Web UI

### Option 1: Using PowerShell Script (Easiest)

```powershell
./start_web_ui.ps1
```

This will:
1. Check if the model exists (downloads if needed)
2. Start the Flask web server
3. Open the app at http://localhost:5000

### Option 2: Manual Steps

```powershell
# 1. Download model (first time only)
python download_model.py

# 2. Start the server
python app.py
```

Then open your browser to: **http://localhost:5000**

## Demo Walkthrough

### Step 1: Fill in the Persona
Example: `Health-conscious home cook looking for quick meals`

### Step 2: Describe the Task
Example: `Find main course dinner recipes that are easy to prepare and use common ingredients`

### Step 3: Upload PDF Files
- Click the upload area or drag & drop PDF files
- You can upload multiple PDFs at once
- Files are shown in a list with remove buttons

### Step 4: Click "Analyze Documents"
- The page shows a loading animation
- Processing takes a few seconds depending on file size

### Step 5: View Results
- **Metadata section** shows:
  - Number of documents analyzed
  - Your persona and task
  - Processing time
  - Timestamp

- **Top Sections** displays:
  - Top 5 most relevant sections ranked
  - Document name and page number
  - Relevance score percentage
  - Sections are color-coded and numbered

- **Detailed Analysis** shows:
  - Full text excerpts from each section
  - Document and page information

### Step 6: New Analysis
- Click "New Analysis" button to start over
- Form resets and you can upload new files

## Sample Test Data

You can test with the sample PDFs in the `input/` directory:

1. Navigate to the web UI
2. Upload any PDF files from `input/` folder
3. Use the sample persona/task from `challenge1b_input.json`

## Tips

- **Multiple Files**: Upload multiple PDFs to compare across documents
- **Different Personas**: Try different persona descriptions to see how results change
- **Mobile Testing**: Open on your phone to test responsive design
- **Drag & Drop**: Drag files directly from File Explorer to the upload area

## Troubleshooting

### Model Not Loading
If you see "Model not loaded" warning:
```powershell
python download_model.py
```

### Server Won't Start
- Check if port 5000 is already in use
- Try closing other applications using that port
- Or change the port in `app.py`

### Files Won't Upload
- Ensure files are PDF format
- Check file size (max 50MB per file)
- Make sure `uploads/` directory exists

## Features to Showcase

1. **Modern Design**: Clean, minimalist purple gradient theme
2. **Smooth Animations**: Fade-in effects, loading spinner, hover states
3. **Responsive**: Works on desktop, tablet, and mobile
4. **Drag & Drop**: Easy file upload with visual feedback
5. **Real-time Feedback**: Loading states and progress indicators
6. **Detailed Results**: Ranked sections with relevance scores
7. **Easy Reset**: One-click to start a new analysis

## Screenshot Moments

Best moments to capture:
1. Home page with empty form (clean state)
2. File upload area with dragged files
3. Loading animation
4. Results page with top sections
5. Detailed analysis cards
6. Mobile view (responsive design)

Enjoy exploring the Persona AI Document Analyzer! 🚀
