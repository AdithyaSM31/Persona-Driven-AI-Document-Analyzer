# Start the Persona AI Document Analyzer Web UI
# Usage: ./start_web_ui.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Persona AI Document Analyzer - Web UI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if model exists
if (-not (Test-Path "./model")) {
    Write-Host "⚠️  Model not found!" -ForegroundColor Yellow
    Write-Host "Running download_model.py to download the model..." -ForegroundColor Yellow
    Write-Host ""
    python download_model.py
    Write-Host ""
}

# Start the Flask server
Write-Host "🚀 Starting web server..." -ForegroundColor Green
Write-Host "📍 Server will be available at: http://localhost:5000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python app.py
