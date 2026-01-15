# Build & Run WriteForMe

.\build-exe.ps1

if (Test-Path "dist\WriteForMe.exe") {
    Write-Host "Launching WriteForMe.exe"
    Start-Process "dist\WriteForMe.exe"
}
