# Clear Windows Icon Cache and Launch Dashboard
Write-Host "🔄 Clearing Windows Icon Cache..." -ForegroundColor Cyan

# Kill Explorer to clear icon cache
Stop-Process -Name explorer -Force
Start-Sleep -Seconds 2

# Clear icon cache database
$iconCache = "$env:LOCALAPPDATA\IconCache.db"
if (Test-Path $iconCache) {
    Remove-Item $iconCache -Force
    Write-Host "✅ Icon cache cleared" -ForegroundColor Green
}

# Also clear thumbnail cache
$thumbCache = "$env:LOCALAPPDATA\Microsoft\Windows\Explorer\thumbcache_*.db"
Get-ChildItem -Path "$env:LOCALAPPDATA\Microsoft\Windows\Explorer" -Filter "thumbcache_*.db" | Remove-Item -Force
Write-Host "✅ Thumbnail cache cleared" -ForegroundColor Green

# Restart Explorer
Start-Process explorer.exe
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "🚀 Launching WriteForMe Dashboard..." -ForegroundColor Cyan
Write-Host ""

# Launch the app
cd W:\workplace-1\writeforme
.\venv\Scripts\python.exe frontend\dashboard_v2.py
