# WriteForMe - Executable Build Guide

## 🎯 The Real Solution

**Windows taskbar shows the icon of the EXECUTABLE, not the script.**

When running `python.exe dashboard_v2.py`, Windows sees `python.exe` and shows Python's icon.

**Solution:** Package into `WriteForMe.exe` with embedded icon.

---

## 🔨 Build Instructions

### Quick Build (One Command)

```powershell
.\build-and-run.ps1
```

This will:
1. Install PyInstaller (if needed)
2. Clean previous builds
3. Create WriteForMe.exe with embedded icon
4. Launch the app

---

### Manual Build Steps

**Step 1: Install PyInstaller**
```powershell
.\venv\Scripts\activate
pip install pyinstaller
```

**Step 2: Build the executable**
```powershell
.\build-exe.ps1
```

**Step 3: Run the app**
```powershell
.\dist\WriteForMe.exe
```

---

## 📦 What Gets Built

**Output:** `dist/WriteForMe.exe`

**Embedded:**
- Custom icon (`wfm_logo.ico`) ✅
- PyQt6 runtime
- Application code
- Logo assets

**Size:** ~150-200 MB (includes PyQt6)

---

## ✅ After Building

**Windows will now show:**
- ✅ Custom WriteForMe icon in taskbar
- ✅ Custom icon in Alt+Tab
- ✅ Custom icon in Task Manager
- ✅ Proper app grouping

**No more Python icon!** 🎉

---

## 🔧 Build Configuration

The build is configured in `WriteForMe.spec`:

```python
exe = EXE(
    name='WriteForMe',
    icon='assets/wfm_logo.ico',  # Embedded icon
    console=False,               # No console window
    ...
)
```

---

## 📝 Development vs Production

**Development (source):**
```powershell
python frontend/dashboard_v2.py
```
- Shows Python icon in taskbar ❌
- Faster iteration
- Good for development

**Production (compiled):**
```powershell
.\dist\WriteForMe.exe
```
- Shows custom icon in taskbar ✅
- Standalone executable
- Ready for distribution

---

## 🚀 Distribution

To share your app:

1. Build the exe: `.\build-exe.ps1`
2. Copy `dist\WriteForMe.exe` to target machine
3. Users can run it directly (no Python needed!)

**Optional:** Create installer with NSIS or Inno Setup

---

## 🔄 Rebuilding

After code changes:
```powershell
.\build-exe.ps1
```

The script automatically cleans old builds.

---

## ⚙️ Advanced Options

**One-file build (current):**
- Single .exe file
- Slower startup
- Easier distribution

**One-folder build:**
```powershell
pyinstaller WriteForMe.spec --onedir
```
- Faster startup
- Multiple files in folder

---

## 🐛 Troubleshooting

**Issue:** Import errors after building
- Add missing imports to `hiddenimports` in `WriteForMe.spec`

**Issue:** Missing assets
- Add asset files to `datas` in `WriteForMe.spec`

**Issue:** Icon still not showing
- Restart Windows Explorer: `taskkill /f /im explorer.exe && start explorer.exe`
- Clear icon cache (see Windows docs)

---

## 📚 Next Steps

1. Run `.\build-and-run.ps1`
2. Check taskbar for custom icon
3. If satisfied, distribute `dist\WriteForMe.exe`

**That's it!** The taskbar icon issue is solved. 🎉
