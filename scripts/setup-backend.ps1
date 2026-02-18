# PowerShell Setup Script for Synesthesia Engine Backend

Write-Host "🦖 Setting up Synesthesia Engine Backend..." -ForegroundColor Green

# Step 1: Navigate to backend
Set-Location -Path "backend"

# Step 2: Install dependencies using parent venv
Write-Host "`n📦 Installing Python dependencies..." -ForegroundColor Cyan
& ..\.venv\Scripts\python.exe -m pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Installation failed. Check errors above." -ForegroundColor Red
    exit 1
}

# Step 3: Check for .env file
if (!(Test-Path ".env")) {
    Write-Host "`n⚠️  No .env file found. Copying from template..." -ForegroundColor Yellow
    Copy-Item ".env.template" ".env"
    Write-Host "⚠️  IMPORTANT: Edit backend/.env and add your ODYSSEY_API_KEY!" -ForegroundColor Yellow
    Write-Host "   Format: ODYSSEY_API_KEY=ody_your_key_here" -ForegroundColor White
} else {
    Write-Host "`n✅ .env file found" -ForegroundColor Green
}

# Step 4: Run the server
Write-Host "`n🚀 Starting FastAPI backend..." -ForegroundColor Cyan
Write-Host "   Server will start at: http://localhost:8000" -ForegroundColor White
Write-Host "   Press Ctrl+C to stop" -ForegroundColor White
Write-Host ""

& ..\.venv\Scripts\python.exe main.py
