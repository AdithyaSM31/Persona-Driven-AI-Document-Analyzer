# ⚡ RENDER - QUICK REFERENCE CARD

## 🎯 Copy These Commands

### **Build Command:**
```bash
pip install -r requirements.txt
```

### **Start Command:**
```bash
gunicorn -b 0.0.0.0:$PORT app:app --timeout 120 --workers 1 --threads 4 --worker-class gthread --log-level info
```

### **Health Check Path (Optional):**
```
/api/health
```

---

## 📝 Settings Summary

| Field | Value |
|-------|-------|
| **Name** | `persona-ai-analyzer` |
| **Environment** | `Python 3` |
| **Branch** | `main` |
| **Root Directory** | (blank) |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn -b 0.0.0.0:$PORT app:app --timeout 120 --workers 1 --threads 4 --worker-class gthread --log-level info` |
| **Plan** | `Free` |

---

## ⏱️ Expected Timeline

- **Build**: 3-4 minutes
- **First Start**: 30-60 seconds (model download)
- **Total**: ~5-7 minutes
- **Status**: 🟢 Live at `https://[your-service].onrender.com`

---

## 🧪 Quick Test

1. Open your URL
2. Upload PDF
3. Enter: Persona + Task
4. Click "Analyze"
5. View results! ✨

---

**Full docs**: See `RENDER_COMMANDS.md`

**Need help?** Check `RENDER_PYMUPDF_FIX.md` for troubleshooting
