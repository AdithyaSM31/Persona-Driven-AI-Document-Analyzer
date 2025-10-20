# 🚀 Render Deployment Commands

## Complete Configuration for Render.com

### 📋 Service Settings

| Setting | Value |
|---------|-------|
| **Name** | `persona-ai-analyzer` (or your choice) |
| **Environment** | `Python 3` |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Root Directory** | Leave blank |
| **Plan** | `Free` (or Starter if needed) |

---

## ⚙️ Build & Start Commands

### **Build Command** 
Copy and paste this into the "Build Command" field:

```bash
pip install -r requirements.txt
```

**What it does:**
- Installs all Python dependencies from `requirements.txt`
- Downloads PyMuPDF 1.24.0 (binary wheel - no compilation!)
- Installs sentence-transformers and ML dependencies
- Takes ~2-3 minutes

---

### **Start Command**
Copy and paste this into the "Start Command" field:

```bash
gunicorn -b 0.0.0.0:$PORT app:app --timeout 120 --workers 1 --threads 4 --worker-class gthread --log-level info
```

**What it does:**
- Starts Gunicorn WSGI server
- Binds to `0.0.0.0:$PORT` (Render provides $PORT automatically)
- `app:app` means Flask app from `app.py`
- `--timeout 120` allows 2 minutes for model loading
- `--workers 1` single worker (sufficient for free tier)
- `--threads 4` handles 4 concurrent requests per worker
- `--worker-class gthread` threaded worker for better performance
- `--log-level info` detailed logs for debugging

---

## 🔧 Environment Variables (Optional)

If you want to customize settings, add these in Render's "Environment" tab:

| Key | Value | Description |
|-----|-------|-------------|
| `PYTHON_VERSION` | `3.11.9` | Specify Python version |
| `PORT` | (Auto-set by Render) | Don't set manually |
| `MODEL_PATH` | `./model` | Local model cache directory |

**Note:** For basic setup, you don't need to add any environment variables!

---

## 📦 Step-by-Step Setup on Render

### 1. Create New Web Service
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account (if not already)
4. Select repository: **Persona-Driven-AI-Document-Analyzer**

### 2. Configure Service
Fill in the form with these exact values:

```
Name: persona-ai-analyzer
Region: Oregon (US West) or closest to you
Branch: main
Root Directory: (leave blank)
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn -b 0.0.0.0:$PORT app:app --timeout 120 --workers 1 --threads 4 --worker-class gthread --log-level info
Plan: Free
```

### 3. Advanced Settings (Optional)
Click **"Advanced"** if you want to customize:

- **Auto-Deploy**: Yes (deploys on every git push)
- **Health Check Path**: `/api/health`
- **Health Check Grace Period**: 300 seconds (5 minutes for initial model download)

### 4. Create Web Service
Click **"Create Web Service"** button at the bottom

---

## ⏱️ Deployment Timeline

```
00:00 → 00:30   Cloning repository from GitHub
00:30 → 01:00   Setting up Python environment
01:00 → 03:00   Installing dependencies (pip install)
                ├─ Flask, Flask-CORS, gunicorn ✅
                ├─ PyMuPDF 1.24.0 (binary wheel) ✅
                ├─ sentence-transformers ✅
                └─ numpy, scikit-learn ✅
03:00 → 04:00   Build complete, starting service
04:00 → 05:00   First request: Downloading ML model
                └─ all-MiniLM-L6-v2 (~90MB)
05:00 → 05:30   Health check passing
05:30           🎉 Deploy successful!
```

**Total Time:** 5-7 minutes

---

## 🔍 How to Verify Build Success

### Check Build Logs
Look for these success indicators:

```bash
# ✅ Dependencies installed
Successfully installed Flask-3.0.0 Flask-CORS-4.0.0 gunicorn-21.2.0
Successfully installed PyMuPDF-1.24.0
Successfully installed sentence-transformers-2.2.2

# ✅ No compilation errors
# You should NOT see:
#   - "Compiling C++ code..."
#   - "error: 'FzStextPage' does not name a type"
#   - "Build failed"

# ✅ Service started
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Using worker: gthread
[INFO] Booting worker with pid: 1
```

### Check Service Status
Once deployed, you should see:
- **Status**: 🟢 Live
- **URL**: `https://persona-ai-analyzer.onrender.com`
- **Last Deploy**: "Just now"
- **Health Check**: ✅ Passing

---

## 🧪 Test Your Deployed App

### 1. Open Your URL
Click the URL in Render dashboard or go to:
```
https://[your-service-name].onrender.com
```

### 2. You Should See:
- ✨ Animated particle background
- 🌓 Dark/light mode toggle
- 📤 Drag-and-drop file upload area
- 🎨 Modern glassmorphism UI

### 3. Test Functionality:
```bash
# Upload PDF
- Drag PDF file or click to browse
- Example: input/challenge1b_input.json (if you have PDFs)

# Enter Analysis Details
- Persona: "Data scientist analyzing research papers"
- Task: "Extract key insights and methodologies"

# Analyze
- Click "Analyze Documents"
- First time: 30-60 seconds (model downloads)
- Subsequent: 2-5 seconds (instant!)

# View Results
- See analysis cards with similarity scores
- Click "View Detailed Analysis" for modal popup
- Check structure extraction (TOC, metadata)
```

---

## 🐛 Troubleshooting

### Build Fails: "PyMuPDF compilation error"
**Solution:** Verify `requirements.txt` has:
```python
PyMuPDF==1.24.0  # NOT 1.23.26!
```

### Start Fails: "Address already in use"
**Solution:** Don't hardcode port in `app.py`. Use:
```python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

### Health Check Fails: "Timeout"
**Solution:** Increase timeout in start command:
```bash
gunicorn -b 0.0.0.0:$PORT app:app --timeout 180  # 3 minutes
```

### Out of Memory: "Worker timeout"
**Solution:** Reduce workers/threads:
```bash
gunicorn -b 0.0.0.0:$PORT app:app --workers 1 --threads 2
```
Or upgrade to Starter plan (512MB → 2GB RAM)

---

## 📁 Files Used by Render

```
📦 Persona-Driven-AI-Document-Analyzer/
├── 📄 requirements.txt          ← Build command reads this
├── 📄 app.py                     ← Start command runs this
├── 📄 runtime.txt (optional)     ← Specifies Python version
├── 📁 templates/
│   └── 📄 index.html             ← Main UI
├── 📁 static/
│   ├── 📁 css/
│   │   └── 📄 styles.css         ← Styling
│   └── 📁 js/
│       └── 📄 app.js             ← Frontend logic
└── 📁 model/ (created at runtime) ← ML model cache
```

---

## 🔄 Auto-Deploy on Git Push

Once configured, every time you push to `main`:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render automatically:
1. Detects the push
2. Starts new build
3. Runs build command
4. Runs start command
5. Replaces old deployment (zero downtime!)

---

## 💰 Free Tier Limits

| Resource | Free Tier | Your Usage | Status |
|----------|-----------|------------|--------|
| **Build Minutes** | 500/month | ~5-7 min/deploy | ✅ ~70 deploys/month |
| **Bandwidth** | 100 GB/month | Minimal (API calls) | ✅ More than enough |
| **Storage** | Persistent disk | ~200MB (model) | ✅ Plenty of space |
| **Uptime** | Spins down after 15min idle | N/A | ⚠️ First request slow after idle |
| **RAM** | 512 MB | ~300MB (app + model) | ✅ Fits comfortably |

**Note:** Free tier apps spin down after 15 minutes of inactivity. First request after idle takes 30-60 seconds to cold start.

---

## 🚀 Quick Copy-Paste Setup

### For Render Dashboard Form:

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn -b 0.0.0.0:$PORT app:app --timeout 120 --workers 1 --threads 4 --worker-class gthread --log-level info
```

**Health Check Path:**
```
/api/health
```

**That's it!** Click "Create Web Service" and you're done! 🎉

---

## 📞 Support Resources

- **Render Docs**: https://render.com/docs
- **Python on Render**: https://render.com/docs/deploy-flask
- **Troubleshooting**: https://render.com/docs/troubleshooting-deploys
- **Community**: https://community.render.com

---

## ✅ Checklist

Before deploying, ensure:

- [x] `requirements.txt` has `PyMuPDF==1.24.0`
- [x] `app.py` uses `os.environ.get('PORT', 5000)`
- [x] `app.py` has lazy model loading (loads on first request)
- [x] All changes committed and pushed to GitHub
- [x] GitHub repository connected to Render
- [x] Build command and start command configured
- [x] Service created and deploying

**Once all checked, your app should deploy successfully!** 🎊

---

**Next Step:** Go to https://dashboard.render.com and create your web service with these commands! 🚀
