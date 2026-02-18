# PowerShell Setup Script for Synesthesia Engine Frontend

Write-Host "🦖 Setting up Synesthesia Engine Frontend..." -ForegroundColor Green

# Step 1: Navigate to frontend
Set-Location -Path "frontend"

# Step 2: Install dependencies
Write-Host "`n📦 Installing Node dependencies..." -ForegroundColor Cyan
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Installation failed. Check errors above." -ForegroundColor Red
    exit 1
}

# Step 3: Run dev server
Write-Host "`n🚀 Starting Vite development server..." -ForegroundColor Cyan
Write-Host "   Frontend will start at: http://localhost:5173" -ForegroundColor White
Write-Host "   Press Ctrl+C to stop" -ForegroundColor White
Write-Host ""

npm run dev
