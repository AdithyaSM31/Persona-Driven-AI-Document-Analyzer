# 🚂 Deploy to Railway.app (Recommended for ML Apps)

## Why Railway Instead of Vercel?

**Issue with Vercel**: The ML model (sentence-transformers + PyTorch) is ~500MB, exceeding Vercel's 250MB limit.

**Railway.app Benefits**:
- ✅ **No size limits** for ML models
- ✅ **Free tier** with $5 credit
- ✅ **GitHub integration** for auto-deploy
- ✅ **Built for Python ML apps**
- ✅ **Faster cold starts** than serverless

## 🚀 Quick Deploy (5 Minutes)

### Step 1: Sign Up & Connect GitHub

1. Go to **https://railway.app**
2. Click **"Start a New Project"**
3. Sign in with GitHub
4. Authorize Railway to access your repositories

### Step 2: Deploy

1. Click **"Deploy from GitHub repo"**
2. Select **`AdithyaSM31/Persona-Driven-AI-Document-Analyzer`**
3. Railway auto-detects Python and starts building
4. Wait 3-5 minutes for first deployment

### Step 3: Configure (Optional)

Railway auto-configures everything, but you can verify:

1. **Environment Variables**: None needed (all configured)
2. **Start Command**: `gunicorn -b 0.0.0.0:$PORT app:app --timeout 120` (from Procfile)
3. **Port**: Auto-assigned by Railway

### Step 4: Get Your URL

1. Go to **Settings** → **Domains**
2. Click **"Generate Domain"**
3. Copy your public URL: `https://your-app.up.railway.app`

## 📁 Files Already Configured

I've created these files for Railway:

- ✅ `Procfile` - Tells Railway how to start the app
- ✅ `railway.json` - Railway configuration
- ✅ `runtime.txt` - Python version specification
- ✅ `requirements.txt` - Updated with gunicorn

## 🔧 What Happens During Deployment

1. **Build Phase** (2-3 minutes):
   - Installs Python 3.11
   - Installs all packages from `requirements.txt`
   - Downloads ML model (sentence-transformers)

2. **Deploy Phase** (30 seconds):
   - Starts gunicorn server
   - Loads ML model into memory
   - Makes app publicly accessible

3. **First Request**:
   - Instant! (model already loaded)
   - No cold starts like serverless

## 💰 Pricing

**Free Tier**: $5 credit (no credit card required)
- Enough for ~500 hours of runtime
- Perfect for demos and testing

**Pro Plan**: $5/month + usage
- More resources
- Custom domains
- Priority support

## 🎯 After Deployment

### Test Your App

```bash
# Health check
curl https://your-app.up.railway.app/api/health

# Or open in browser
https://your-app.up.railway.app
```

### Monitor

1. **Logs**: Railway Dashboard → Your Project → "View Logs"
2. **Metrics**: See CPU/Memory usage in real-time
3. **Deployments**: Track all deployments and rollback if needed

## 🔄 Auto-Deploy from GitHub

Railway automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Railway detects the push and redeploys automatically!

## 🐛 Troubleshooting

### Issue: Build fails
**Solution**: Check logs in Railway dashboard. Usually dependency issues.

### Issue: App crashes
**Solution**: Check logs. Might need to increase memory in settings.

### Issue: Slow first load
**Solution**: Railway keeps app running (no cold starts), but first ML inference might take 2-3 seconds.

## 📊 Compare: Railway vs Vercel

| Feature | Railway | Vercel |
|---------|---------|--------|
| ML Model Support | ✅ Yes | ❌ Size limit |
| Cold Starts | ✅ No | ⚠️ Yes |
| Free Tier | $5 credit | Yes |
| GitHub Integration | ✅ Yes | ✅ Yes |
| Custom Domains | ✅ Yes | ✅ Yes |
| Best For | ML/Python Apps | Static/Serverless |

## 🎓 Alternative: Render.com

If you prefer Render over Railway:

1. Go to https://render.com
2. New → "Web Service"
3. Connect GitHub repo
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `gunicorn -b 0.0.0.0:$PORT app:app --timeout 120`
6. Deploy!

## ✨ Summary

**Recommended**: Deploy to Railway.app for best ML app experience!

```bash
# Your links after deployment:
GitHub: https://github.com/AdithyaSM31/Persona-Driven-AI-Document-Analyzer
Railway: https://your-app.up.railway.app
```

Ready to deploy? Go to **https://railway.app** and click "Start a New Project"! 🚂
