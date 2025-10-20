# ⚠️ IMPORTANT: VERCEL DEPLOYMENT NOT SUPPORTED

## Why This App Cannot Deploy to Vercel

This application uses machine learning models that are **too large for Vercel**:

- **ML Model Size**: ~500MB (sentence-transformers + PyTorch)
- **Vercel Size Limit**: 250MB maximum
- **Result**: Build will always fail on Vercel

## ✅ Supported Deployment Platforms

### **Railway.app** ⭐ RECOMMENDED
- ✅ No size limits
- ✅ $5 free credit
- ✅ Auto-deploy from GitHub
- 📖 See: `RAILWAY_DEPLOY.md`

### **Render.com**
- ✅ No size limits  
- ✅ Forever free tier
- ✅ Auto-deploy from GitHub
- 📖 See: `DEPLOYMENT_ALTERNATIVES.md`

### **Hugging Face Spaces**
- ✅ Built for ML models
- ✅ Free hosting
- 📖 See: `DEPLOYMENT_ALTERNATIVES.md`

## 🚀 Quick Deploy to Railway

1. Go to **https://railway.app**
2. Sign in with GitHub
3. Click **"Deploy from GitHub repo"**
4. Select this repository
5. Wait 3-5 minutes
6. Done! ✨

## 📝 Files in This Repo

- `vercel.json` - Disabled (kept for reference only)
- `api/index.py` - Vercel function (won't work due to size)
- `Procfile` - ✅ Works with Railway/Render
- `railway.json` - ✅ Railway configuration
- `app.py` - ✅ Main Flask app

## ⚠️ If You're Seeing This on Vercel

The build is failing because the model is too large. Please:

1. **Delete this Vercel project**
2. **Deploy to Railway instead**: https://railway.app
3. **See deployment guide**: `RAILWAY_DEPLOY.md`

## 🔗 Documentation

- **Railway Deploy Guide**: `RAILWAY_DEPLOY.md`
- **All Options**: `DEPLOYMENT_ALTERNATIVES.md`
- **Status**: `DEPLOYMENT_STATUS.md`

---

**TL;DR**: Use Railway.app, not Vercel, for this ML application.
