# 🚀 Vercel Deployment Guide

## Quick Deploy (Recommended)

### Option 1: Deploy via Vercel Dashboard

1. **Go to Vercel Dashboard**
   - Visit [vercel.com](https://vercel.com)
   - Sign in with your GitHub account

2. **Import Project**
   - Click "Add New" → "Project"
   - Select "Import Git Repository"
   - Choose `AdithyaSM31/Persona-Driven-AI-Document-Analyzer`

3. **Configure Project**
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: Leave empty (not needed)
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

4. **Deploy**
   - Click "Deploy"
   - Wait 2-5 minutes for first deployment (downloads ML model)
   - Your app will be live at `https://your-project.vercel.app`

### Option 2: Deploy via CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from Project Directory**
   ```bash
   cd "c:\Users\adith\Downloads\Persona AI Document Analyser\Adobe-India-Hacathon-Connecting-the-dots-2025-Round-1B-main"
   vercel
   ```

4. **Follow Prompts**
   - Set up and deploy: `Y`
   - Which scope: Select your account
   - Link to existing project: `N`
   - Project name: `persona-ai-document-analyzer` (or your choice)
   - Directory: `./` (default)
   - Override settings: `N`

5. **Deploy to Production**
   ```bash
   vercel --prod
   ```

## ⚙️ Configuration Details

### Files Created for Vercel

1. **`vercel.json`** - Vercel configuration
   - Routes all requests to the serverless function
   - Configures Python runtime

2. **`api/index.py`** - Serverless function
   - Modified Flask app for serverless environment
   - Uses `tempfile` instead of uploads directory
   - Auto-downloads model on first cold start

3. **`.vercelignore`** - Files to exclude from deployment
   - Model directory (downloads on Vercel)
   - Uploads directory
   - Python cache files

4. **`.gitignore`** - Files to exclude from Git
   - Virtual environments
   - Model files (too large for Git)
   - Python cache

### Important Notes

⚠️ **First Deployment Takes Longer**
- The ML model (~90MB) downloads on first cold start
- Expect 30-60 seconds for first request
- Subsequent requests are fast (model is cached)

⚠️ **Function Size Limits**
- Vercel free tier: 250MB function size limit
- Our app: ~150MB with model (within limit)
- Hobby tier: 50MB file upload limit

⚠️ **Cold Starts**
- Functions may "sleep" after inactivity
- First request after sleep: 5-10 seconds
- Consider upgrading for always-on functions

## 🔧 Environment Variables (Optional)

You can set these in Vercel Dashboard → Project Settings → Environment Variables:

- `PYTHONUNBUFFERED=1` (already set in vercel.json)

## 🧪 Testing Your Deployment

1. **Health Check**
   ```bash
   curl https://your-project.vercel.app/api/health
   ```
   Should return: `{"status": "healthy", "model_loaded": true}`

2. **Test Upload**
   - Open your deployed URL
   - Upload a PDF file
   - Enter persona and task
   - Click "Analyze Document"

## 🐛 Troubleshooting

### Issue: "Model not loaded"
**Solution**: Wait 30 seconds and refresh. Model is downloading on first start.

### Issue: "Function timeout"
**Solution**: 
- Vercel free tier: 10-second timeout
- Consider upgrading to Pro for 60-second timeout
- Or optimize model/reduce PDF size

### Issue: "File too large"
**Solution**: 
- Free tier: 50MB file limit
- Compress PDFs before upload
- Or upgrade Vercel plan

### Issue: "Build failed"
**Solution**: 
- Check `requirements.txt` for compatible versions
- Ensure all files are committed to Git
- Check build logs in Vercel dashboard

## 📊 Monitoring

### View Logs
1. Go to Vercel Dashboard
2. Select your project
3. Click "Deployments"
4. Click on a deployment
5. View "Functions" tab for logs

### Performance
- Check response times in Vercel Analytics
- Monitor function executions
- Set up error alerts

## 🔄 Updating Your Deployment

### Auto-Deploy (Recommended)
Every push to `main` branch automatically deploys:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

### Manual Deploy
```bash
vercel --prod
```

## 💡 Tips for Better Performance

1. **Keep Model Warm**: Set up monitoring to ping your app periodically

2. **Optimize PDFs**: 
   - Compress PDFs before upload
   - Limit to 5-10 MB per file

3. **Error Handling**: 
   - Check Vercel logs for errors
   - Monitor function execution times

4. **Custom Domain** (Optional):
   - Add custom domain in Vercel Dashboard
   - Configure DNS settings

## 📱 Share Your App

Your app is now live! Share it:
- Direct link: `https://your-project.vercel.app`
- GitHub: `https://github.com/AdithyaSM31/Persona-Driven-AI-Document-Analyzer`

## 🎓 Next Steps

1. ✅ Test thoroughly with different PDFs
2. ✅ Add custom domain (optional)
3. ✅ Set up analytics
4. ✅ Monitor performance
5. ✅ Share with team/portfolio

---

## 📞 Support

- Vercel Docs: https://vercel.com/docs
- GitHub Issues: https://github.com/AdithyaSM31/Persona-Driven-AI-Document-Analyzer/issues

Happy Deploying! 🚀
