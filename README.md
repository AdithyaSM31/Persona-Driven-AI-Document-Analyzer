# Persona-Driven AI Document Analyzer

🚀 **Deploy**: [Railway.app](https://railway.app) (Recommended) | 🎯 **Adobe India Hackathon 2025 - Round 1B**

An intelligent document analysis system that uses AI to extract and rank relevant sections from PDF documents based on user personas and specific tasks.

This repository contains the solution for Round 1B of the Adobe Hackathon. The project features both a modern web UI and a Docker-based command-line interface.

> **Note**: This app uses ML models (~500MB) which exceed Vercel's size limits. We recommend deploying to **Railway.app** or **Render.com** for ML apps. See [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md) for quick deployment.

## ✨ Features

### 🎨 Modern Web UI
- **Beautiful Dark/Light Theme**: Toggle between themes with glassmorphism effects
- **Animated Background**: Particle network and gradient orb animations
- **Drag & Drop Upload**: Easy PDF file upload with visual feedback
- **Real-time Analysis**: Interactive results with detailed section views
- **Responsive Design**: Works seamlessly on desktop and mobile

### 🤖 AI-Powered Analysis
- **Persona-Driven**: Customize analysis based on user roles and context
- **Smart Ranking**: AI-powered relevance scoring using sentence transformers
- **Task-Specific**: Analyzes documents for specific job-to-be-done scenarios
- **Structure Extraction**: Intelligently parses PDF table of contents

## 🛠️ Tech Stack

- **Backend**: Flask (Python) with Gunicorn
- **ML Model**: Sentence Transformers (all-MiniLM-L6-v2)
- **PDF Processing**: PyMuPDF
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Railway.app / Render.com (Web) + Docker (CLI)

## 📖 How It Works

This solution uses natural language processing to understand the semantic meaning of documents and user queries:

1. **Text Extraction**: Content from each PDF is extracted using **PyMuPDF**
2. **Vector Embedding**: A pre-trained **sentence-transformers** model converts the user's persona, their "job-to-be-done," and each section into numerical vectors (embeddings)
3. **Similarity Search**: We use **scikit-learn** to calculate cosine similarity between query and document vectors
4. **Ranking**: Sections with highest similarity scores are ranked and displayed

## 🚀 Getting Started

### Option 1: Web Application (Recommended)

#### Local Development

1. Clone the repository:
```bash
git clone https://github.com/AdithyaSM31/Persona-Driven-AI-Document-Analyzer.git
cd Persona-Driven-AI-Document-Analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the ML model:
```bash
python download_model.py
```

4. Run the web application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

#### Deploy to Cloud (Railway.app - Recommended)

**Quick Deploy to Railway** (Best for ML apps with large models):

1. Go to **https://railway.app**
2. Click **"Start a New Project"** → **"Deploy from GitHub repo"**
3. Select **`AdithyaSM31/Persona-Driven-AI-Document-Analyzer`**
4. Railway auto-deploys in 3-5 minutes!
5. Get your public URL from **Settings → Domains**

See [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md) for detailed instructions.

**Alternative: Render.com**

1. Go to **https://render.com**
2. New → **"Web Service"** → Connect GitHub
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `gunicorn -b 0.0.0.0:$PORT app:app --timeout 120`
5. Deploy!

> **Why not Vercel?** The ML model (~500MB) exceeds Vercel's 250MB size limit. Railway and Render are designed for ML apps with no size restrictions.

### Option 2: Docker CLI (Original Challenge Solution)

Follow these steps to set up the Docker-based command-line solution.

### **1. Model Preparation (One-time Setup)**

This project uses a Python script to download the required pre-trained model.

1.  First, install the Python dependencies from the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
2.  Next, run the `download_model.py` script. This will download the necessary model files into the `./model/` directory, making them available for the Docker build.
    ```bash
    python download_model.py
    ```

### **2. Prepare Your Input Files**

The system requires a collection of PDFs and a JSON file defining the persona and their task.

1.  Place all your PDF documents (e.g., `Breakfast Ideas.pdf`, `Dinner Ideas - Mains_1.pdf` (Collection 3)) inside the `./input` folder.

2.  Create a file named **`challenge1b_input.json`** inside the `./input` folder with the following structure:

    ```json
    {
      "persona": "Health-conscious home cook looking for quick meals",
      "job_to_be_done": "Find main course dinner recipes that are easy to prepare and use common ingredients."
    }
    ```

### **3. Build the Docker Image**

With the model and input files in place, run the following command from the project's root directory to build the Docker image:

```bash
docker build --platform linux/amd64 -t persona-analyzer:1.0 .
```

### **4. Run the Docker Container**

Use the command below to run the container. It will process the files in your `input` folder and generate a single **`challenge1b_output.json`** file in the `output` folder.

```bash
docker run --rm -v "$(pwd)/input":/app/input -v "$(pwd)/output":/app/output --network none persona-analyzer:1.0
```

## 📖 Web UI Usage

1. **Upload PDF**: Drag and drop or click to select PDF documents
2. **Define Persona**: Enter the user persona (e.g., "Software Engineer", "Product Manager")
3. **Specify Task**: Describe the job to be done (e.g., "Learn about API authentication")
4. **Analyze**: Click the analyze button and wait for results
5. **View Results**: See ranked sections with relevance scores
6. **Detailed View**: Click on any section card to view detailed analysis in a modal

## 📁 Project Structure

```
├── api/
│   └── index.py          # Vercel serverless function
├── static/
│   ├── css/
│   │   └── styles.css    # Styles with dark mode
│   └── js/
│       └── app.js        # Frontend logic & animations
├── templates/
│   └── index.html        # Main UI template
├── input/                # Input PDFs and JSON (Docker)
├── output/               # Output JSON (Docker)
├── app.py                # Local Flask server
├── run.py                # Docker CLI script
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
├── Dockerfile           # Docker configuration
└── README.md            # This file
```

## 🎨 UI Features

### Dark Mode Toggle
Switch between light and dark themes with a single click. Theme preference is saved locally.

### Animated Background
- **Particle Network**: Interactive particles that connect when nearby
- **Gradient Orbs**: Floating gradient spheres with smooth animations

### Glassmorphism Design
Modern frosted glass effect on cards and modals for a sophisticated look.

## 🔧 Configuration

### Environment Variables (Optional)

For Vercel deployment:
- `PYTHONUNBUFFERED=1` (already configured in vercel.json)

### Model Configuration

The app uses `sentence-transformers/all-MiniLM-L6-v2` model:
- **Local**: Downloads to `./model` directory
- **Vercel**: Downloads on first cold start (cached thereafter)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Authors

- **Adithya Sankar Menon** - [@AdithyaSM31](https://github.com/AdithyaSM31)
- Mayank Chauhan
- Piyush Maurya

## 🙏 Acknowledgments

- Sentence Transformers for the ML model
- Flask for the web framework
- Vercel for serverless deployment
- Adobe India for the hackathon challenge

---

Made with ❤️ for Adobe India Hackathon 2025
