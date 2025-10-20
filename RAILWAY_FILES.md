# Railway Deployment - Important Notes

## Files for Railway Deployment

- ✅ `Procfile` - Start command for Railway
- ✅ `nixpacks.toml` - Build configuration (forces Python, ignores Docker)
- ✅ `railway.json` - Railway settings
- ✅ `.railwayignore` - Excludes Dockerfile and model directory
- ✅ `requirements.txt` - Python dependencies
- ✅ `app.py` - Main Flask application

## Files NOT Used by Railway

- ❌ `Dockerfile.local` - Renamed from `Dockerfile` (for local Docker only)
- ❌ `run.py` - Docker CLI version (not needed for web deployment)
- ❌ `model/` - Excluded (will download automatically on first request)

## Why Dockerfile Was Renamed

The original `Dockerfile` was for the Docker CLI challenge solution. It expects:
- Pre-downloaded model in `./model/` directory
- Input PDFs in `./input/` directory
- Runs `run.py` script once and exits

Railway needs:
- Web server (Flask app) that stays running
- Model downloaded on-demand (not in Docker image)
- No input/output directories
- Uses `app.py` instead

## If You Want to Use Docker Locally

Rename back and use:
```bash
mv Dockerfile.local Dockerfile
python download_model.py
docker build -t persona-analyzer:1.0 .
docker run --rm -v "$(pwd)/input":/app/input -v "$(pwd)/output":/app/output --network none persona-analyzer:1.0
```

## Railway Deployment Process

1. Railway detects Python app (via `nixpacks.toml`)
2. Installs packages from `requirements.txt`
3. Starts app with command from `Procfile`
4. Model downloads automatically on first request
5. App stays running to handle web requests
