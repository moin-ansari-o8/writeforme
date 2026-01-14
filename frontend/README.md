# 🎨 WriteForMe Dashboard - Glassmorphism UI

Beautiful standalone dashboard for testing the WriteForMe interface before full integration.

## ✨ Features

### **Glassmorphism Design**
- **Frosted glass panels** with semi-transparency
- **Acrylic blur effects** for depth and layering
- **Smooth animations** on hover and interactions
- **Subtle glows** and border highlights
- **Dark mode optimized** (#0a0a0a backgrounds)

### **Three Main Tabs**

#### 📜 **History Tab**
- View all past transcriptions with timestamps
- **Search functionality** to filter by content/mode
- **Re-inject button** to paste text again
- **Delete individual entries** or clear all
- **Export to text** file capability
- Beautiful card layout with hover effects

#### ⚙️ **Settings Tab**
- **AI Provider selection** (Cohere, Gemini, Groq, Ollama)
- **Writing mode** (Vibe Coder, Casual Chatter)
- **Hotkey display** (Win+Shift, Win+Ctrl+Shift)
- **Audio device selection**
- **Voice detection sensitivity**
- **Appearance toggles** (visualizer, system tray)

#### 📊 **Statistics Tab**
- **Summary cards**: Total transcriptions, words, success rate, today's count
- **Activity chart**: Last 7 days visualization
- **Mode usage**: Pie chart showing most used modes
- **Recent activity timeline** with timestamps

## 🚀 Quick Start

### **1. Install Dependencies**

```powershell
cd W:\workplace-1\writeforme
.\venv\Scripts\activate
pip install customtkinter
```

### **2. Launch Dashboard**

```powershell
cd frontend
python dashboard.py
```

### **3. Test the UI**

- Navigate between tabs using the left sidebar
- Search transcriptions in History tab
- Adjust settings in Settings tab
- View stats in Statistics tab
- Test all buttons and interactions

## 📁 Project Structure

```
frontend/
├── dashboard.py              # Main launcher - run this file
├── requirements.txt          # Frontend dependencies
├── README.md                # This file
│
├── assets/
│   └── styles.py            # Glassmorphism color palette & theme
│
├── components/
│   ├── glass_card.py        # Reusable glass cards
│   ├── glass_button.py      # Beautiful buttons with variants
│   └── glass_input.py       # Search bars, dropdowns, inputs
│
└── tabs/
    ├── history_tab.py       # Transcription history view
    ├── settings_tab.py      # Configuration panel
    └── stats_tab.py         # Usage analytics
```

## 🎨 Design System

### **Color Palette**
- **Background**: `#0a0a0a` (deep black)
- **Glass Panels**: `#1a1a1a` at 70% opacity
- **Accent Primary**: `#6366f1` (indigo with glow)
- **Accent Success**: `#10b981` (green)
- **Text Primary**: `#e0e0e0` (bright)
- **Text Secondary**: `#9ca3af` (muted)

### **Typography**
- **Font Family**: Segoe UI (Windows native)
- **Monospace**: Consolas (for hotkeys/code)
- **Sizes**: 11px - 32px range
- **Weights**: Normal, Medium, Bold

### **Spacing & Radius**
- **Padding**: 8px - 32px scale
- **Border Radius**: 8px - 20px for smooth corners
- **Button Height**: 40px standard

## 🔗 Integration Plan

### **Phase 1: Standalone Testing** ✅ (Current)
- Test UI components independently
- Verify design and interactions
- Use mock data for visualization

### **Phase 2: Data Integration** (Next)
- Connect to `data_storage.py` for real transcription history
- Integrate with `paste_manager.py` for re-injection
- Save settings to `settings.json` file

### **Phase 3: Full Integration**
- Add system tray icon to launch dashboard
- Connect Settings tab to live configuration
- Real-time stats updates from transcriptions
- Background operation with capsule visualizer

## 🛠️ Customization

### **Change Colors**
Edit `assets/styles.py` to customize the theme:

```python
ACCENT_PRIMARY = "#your-color"  # Change accent color
BG_GLASS = "#your-color"        # Change glass panel color
```

### **Add More Tabs**
1. Create new tab file in `tabs/`
2. Import in `dashboard.py`
3. Add to navigation sidebar
4. Implement tab switching logic

### **Modify Mock Data**
Edit `_load_mock_data()` methods in each tab to test different scenarios.

## 🐛 Known Limitations

- **Mock data only** - not connected to live transcriptions yet
- **No real re-injection** - just prints to console
- **No settings persistence** - resets on restart
- **Simple charts** - using frames/bars (no matplotlib yet)

## 📝 TODO

- [ ] Connect to `data_storage.py` for real history
- [ ] Implement settings persistence (`settings.json`)
- [ ] Add toast notifications for user feedback
- [ ] Add confirmation dialogs for destructive actions
- [ ] Integrate with `paste_manager.py` for re-injection
- [ ] Add keyboard shortcuts (Ctrl+F for search)
- [ ] System tray icon integration
- [ ] Real-time stats calculations
- [ ] Export functionality
- [ ] Theme customization UI

## 🎯 Testing Checklist

- [ ] Launch dashboard successfully
- [ ] Switch between all three tabs
- [ ] Search transcriptions in History tab
- [ ] Hover over cards (should lighten)
- [ ] Click Re-inject button (logs to console)
- [ ] Click Delete button (removes card)
- [ ] Change AI provider in Settings
- [ ] Toggle switches (should change color)
- [ ] View stats cards and charts
- [ ] Resize window (should be responsive)
- [ ] Click About button (modal dialog)
- [ ] Click Exit button (closes app)

## 💡 Tips

- **Ctrl+Scroll** to zoom in/out (Windows)
- Press **Tab** to navigate inputs with keyboard
- **Esc** to close About dialog
- Use **scroll wheel** in scrollable sections

---

**Built with ❤️ using CustomTkinter**
**Designed for beauty, performance, and user experience**
