# Build WriteForMe.exe

& .\venv\Scripts\Activate.ps1

# Install PyInstaller if needed
pip show pyinstaller >$null 2>&1
if ($LASTEXITCODE -ne 0) {
    pip install pyinstaller
}

# Clean previous builds
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }

# Build
pyinstaller --clean WriteForMe.spec

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build successful: dist\WriteForMe.exe"
} else {
    Write-Host "Build failed"
}
