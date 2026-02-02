# WriteForMe - Background Speech-to-Text Service

**Version:** 2.0 - Background Service Edition

## ✨ What's New

- **🔇 Silent Background Mode** - Runs in system tray, no console window
- **🚫 No AI Prompts** - Direct speech-to-text (no AI refinement overhead)
- **🪟 Windows Auto-Start** - Option to launch on Windows login
- **🎯 System Tray Control** - Simple Start/Stop/Exit menu
- **⌨️ Global Hotkeys Still Work** - Same `Win+Shift` and `Win+Ctrl+Shift` shortcuts

---

## 🚀 Quick Start

### Running the Application

**Option 1: Double-click the EXE**
```
dist\WriteForMe.exe
```

**Option 2: From command line**
```powershell
.\dist\WriteForMe.exe
```

The app will:
1. Launch silently (no console window)
2. Appear as an icon in your Windows system tray
3. Start listening for hotkeys automatically

---

## 🎮 How to Use

### System Tray Menu

Right-click the WriteForMe icon in your system tray:

- **Start Listening** / **Stop Listening** - Toggle the service on/off
- **Auto-start with Windows** - Enable/disable auto-launch on login
- **Quit WriteForMe** - Exit the application

### Global Hotkeys

Once running, use these anywhere in Windows:

| Hotkey | Function |
|--------|----------|
| `Win+Shift` (Hold) | **Push-to-talk** - Hold keys, speak, release to stop |
| `Win+Ctrl+Shift` (Press) | **Toggle mode** - Press once to start recording, press again to stop |

### Workflow

1. **Press hotkey** → Widget appears
2. **Speak your text** → Real-time transcription
3. **Release/press again** → Processing
4. **Auto-paste** → Text pasted into active window
5. **Widget hides** → Ready for next dictation

---

## 🔧 Building from Source

### Install Dependencies

```powershell
cd W:\workplace-1\writeforme
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Build Executable

```powershell
.\build-exe.ps1
```

Or manually:

```powershell
pyinstaller --clean WriteForMe.spec
```

Output: `dist\WriteForMe.exe`

---

## 📋 Features

✅ **Direct Speech-to-Text** - Fast, no AI refinement delays  
✅ **Background Service** - Runs silently in system tray  
✅ **Global Hotkeys** - Works from any application  
✅ **Auto-Paste** - Instantly pastes transcribed text  
✅ **History Tracking** - Saves to `transcriptions_history.json`  
✅ **Single Instance** - Only one instance can run at a time  
✅ **Windows Auto-Start** - Optional launch on login  
✅ **Portable EXE** - No installation required  

---

## 🛠️ Architecture Changes

### Files Modified

1. **[main.py](main.py)** - Removed AI prompt, added `silent_mode` parameter
2. **[launcher.py](launcher.py)** - NEW: System tray launcher with single-instance lock
3. **[WriteForMe.spec](WriteForMe.spec)** - Updated to build launcher.py, excluded webrtcvad
4. **[requirements.txt](requirements.txt)** - Added `pystray` and `psutil`

### How It Works

```
WriteForMe.exe (launcher.py)
    ↓
System Tray Icon (pystray)
    ↓
Background Thread → WisprFlowLocal (main.py)
    ↓
Global Hotkey Listener (pynput)
    ↓
Speech-to-Text (faster-whisper)
    ↓
Auto-Paste (pyperclip + pyautogui)
```

---

## ⚙️ Configuration

### Enable Auto-Start

Right-click tray icon → Check "Auto-start with Windows"

This adds WriteForMe to:
```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
```

### Disable Auto-Start

Right-click tray icon → Uncheck "Auto-start with Windows"

---

## 🐛 Troubleshooting

### App Won't Start

**Symptom:** Clicking exe does nothing

**Fix:** Check if already running
- Look for WriteForMe icon in system tray
- Open Task Manager, look for "WriteForMe.exe"
- If found, close it and try again

---

### Hotkeys Not Working

**Symptom:** Pressing `Win+Shift` does nothing

**Possible causes:**
1. Service stopped - Right-click tray icon → "Start Listening"
2. Another app captured the hotkey
3. Running in elevated/admin app (hotkeys can't reach)

---

### Widget Not Appearing

**Symptom:** Hotkey works but widget doesn't show

**Fix:**
- Widget may be off-screen
- Try pressing hotkey and check all monitors
- Close app, delete lock file: `%LOCALAPPDATA%\WriteForMe\writeforme.lock`
- Restart app

---

### Multiple Instances Warning

**Symptom:** "WriteForMe is already running" message

**Fix:**
```powershell
# Delete lock file
Remove-Item "$env:LOCALAPPDATA\WriteForMe\writeforme.lock" -Force
```

Then restart the app.

---

## 📝 Technical Notes

### No AI Mode

This version defaults to **direct transcription** without AI refinement:
- ✅ Faster processing
- ✅ Lower resource usage
- ✅ No API keys required
- ❌ No grammar correction
- ❌ No formatting improvements

To enable AI refinement, modify [main.py](main.py):
```python
self.use_ai_refinement = True  # Change from False
```

### Dependencies Excluded

- `webrtcvad` - Voice activity detection (optional, caused build issues)
- PyQt6 - Dashboard UI (not needed for background mode)

### Build Size

**WriteForMe.exe**: ~150-200 MB
- Includes Python runtime
- faster-whisper model
- NumPy, Pillow, etc.

---

## 🔒 Privacy & Security

- ✅ **100% Local** - No cloud services
- ✅ **Offline** - No internet required
- ✅ **No Telemetry** - No data collection
- ✅ **History Saved Locally** - `transcriptions_history.json`

---

## 📄 License

Same as original WriteForMe project.

---

## 🙏 Credits

Built on top of:
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) - Speech recognition
- [pynput](https://github.com/moses-palmer/pynput) - Global hotkeys
- [pystray](https://github.com/moses-palmer/pystray) - System tray icon
- [PyInstaller](https://pyinstaller.org/) - Executable packaging

---

**Enjoy hands-free typing! 🎤**
