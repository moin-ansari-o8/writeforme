# Quick launcher for WriteForMe Dashboard
# Run this to test the glassmorphism UI

Write-Host "✨ WriteForMe Dashboard Launcher" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "⚠️  Virtual environment not activated" -ForegroundColor Yellow
    Write-Host "   Activating venv..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
}

# Check if customtkinter is installed
Write-Host "🔍 Checking dependencies..." -ForegroundColor White
$ctkInstalled = python -c "import customtkinter" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "📦 Installing customtkinter..." -ForegroundColor Yellow
    pip install customtkinter
} else {
    Write-Host "✅ CustomTkinter is installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Launching dashboard..." -ForegroundColor Cyan
Write-Host ""

# Launch dashboard
cd frontend
python dashboard.py

cd ..
