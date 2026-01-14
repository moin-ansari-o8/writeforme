# WriteForMe Dashboard - Technical Architecture & UI Component Guide

## Project Overview
**WriteForMe** is a speech-to-text desktop application with AI refinement capabilities. It features a modern glassmorphism UI built with PyQt6, offering real-time audio transcription using Faster-Whisper and AI-powered text refinement via Cohere API.

## Core Technology Stack

### Frontend Framework
- **PyQt6** (v6.x) - Qt-based GUI framework for Python
  - `PyQt6.QtWidgets` - UI components (QMainWindow, QPushButton, QLabel, QFrame, etc.)
  - `PyQt6.QtCore` - Core functionality (QTimer, QPropertyAnimation, pyqtSignal, etc.)
  - `PyQt6.QtGui` - Graphics/painting (QPainter, QColor, QLinearGradient, etc.)

### Backend Services
- **faster-whisper** (v1.0.0+) - Offline speech-to-text transcription (small model, CPU/int8)
- **Cohere API** (v5.0.0+) - AI text refinement (command-r7b-12-2024 model)
- **PyAudio** (v0.2.14) - Audio recording from microphone
- **webrtcvad** - Voice Activity Detection (VAD)
- **numpy** (v1.26.3+) - Audio data processing

### Data & Storage
- **JSON** - Transcription history storage (`transcriptions_history.json`)
- **python-dotenv** - Environment variable management (.env file for API keys)

## Application Architecture

### Main Components (5 Custom Classes)

#### 1. **GlassDashboard** (QMainWindow)
- Main frameless window with transparency
- Size: 1100x750px
- Features:
  - Frameless window (Qt.WindowType.FramelessWindowHint)
  - Transparent background (WA_TranslucentBackground)
  - Custom window dragging
  - Rounded 20px border radius
  - Dark gradient background (RGB: 18,18,18 → 24,24,24)

#### 2. **GlassFrame** (QFrame)
- Reusable glass panel component
- Parameters: `blur_radius=20`, `opacity=0.3`
- Features:
  - QGraphicsBlurEffect for backdrop blur
  - Semi-transparent white fill
  - Rounded corners (16px radius)
  - Subtle border overlay

#### 3. **ModernButton** (QPushButton)
- Custom button with smooth hover animations
- Features:
  - QPropertyAnimation for color transitions (200ms, OutCubic easing)
  - Default: rgba(60,60,65,200)
  - Hover: rgba(80,80,85,230)
  - Rounded 12px corners
  - Minimum height: 44px

#### 4. **TranscriptionCard** (QFrame)
- History item display card
- Height: 140px fixed
- Features:
  - Clickable (emits `card_clicked` signal to show details)
  - Shows: timestamp, mode badge, text preview (120 chars), word count
  - Actions: Re-inject button, Delete button
  - Background: rgba(45,45,48,245) - almost opaque

#### 5. **TranscriptionDetailDialog** (QDialog)
- Modal popup for full transcription view
- Size: 700x600px fixed
- Features:
  - Frameless with rounded 20px corners
  - Glass effect background
  - Shows: timestamp, mode, raw text (scrollable), refined text (scrollable), word count
  - Close button in top right

## UI Layout Structure

```
GlassDashboard (Main Window)
├── Sidebar (Left, 260px width)
│   ├── App Name & Version
│   ├── Navigation Buttons (Home, History, Settings, Statistics)
│   └── Status Indicator (Capsule Active)
│
└── Content Area (Right, glass frame with rounded corners)
    ├── Title Bar (Top Right)
    │   ├── Drag Area (for window movement)
    │   └── Window Controls (Minimize, Maximize, Close - 35x35px)
    │
    └── Tabbed Content (QStackedWidget)
        ├── Home Tab
        │   ├── Welcome Header
        │   ├── Model Selector (Dropdown: Cohere, Vibe Coder, Casual Chatter)
        │   ├── Input Container (Gemini-style, 24px radius)
        │   │   ├── Text Input (QTextEdit, placeholder: "Ask anything...")
        │   │   ├── Mic Button (🎤, right side, 40x40px, transparent)
        │   │   └── Submit Button (➤, right side, 40x40px, blue rgba(70,130,255))
        │   ├── Status Label (Processing states)
        │   └── Result Container (Shows refined text)
        │
        ├── History Tab
        │   ├── Header (Title + Entry Count + Sort Dropdown + Export)
        │   ├── Search Bar (48px height, rounded 12px)
        │   └── Scrollable Card List (TranscriptionCard instances)
        │
        ├── Settings Tab
        │   └── Sections (AI Provider, Writing Mode)
        │
        └── Statistics Tab
            └── (Placeholder)
```

## Design System

### Color Palette
- **Primary Background**: rgba(35,35,38,0.98) - Main content areas
- **Secondary Background**: rgba(45,45,50,0.95) - Input boxes, cards
- **Hover States**: rgba(50,50,55) to rgba(80,80,85)
- **Accent Blue**: rgba(70,130,255,0.9) - Submit button, selections
- **Text Primary**: rgb(220,220,220) - Main text
- **Text Secondary**: rgba(255,255,255,0.7) - Labels, descriptions
- **Text Muted**: rgba(255,255,255,0.5) - Timestamps, hints
- **Borders**: rgba(70,70,75,0.5) - Subtle outlines

### Border Radius Standards
- Window: 20px
- Input containers: 24px
- Buttons (large): 20px
- Cards: 12px
- Small buttons: 8px
- Dropdown: 10px

### Spacing System
- Container margins: 20-40px
- Element spacing: 8-24px
- Button padding: 6-12px
- Input padding: 12-20px

### Typography
- Font: "Segoe UI"
- Headers: 28px Bold
- Subheaders: 16-20px Bold
- Body: 13-14px Regular
- Small: 11-12px Regular

## Key Features & Interactions

### Home Tab Functionality
1. **Voice Recording**:
   - Click mic button → starts recording (button turns red ⏹)
   - Uses `AudioRecorder` class (background thread)
   - Shows status: "🎤 Recording..."
   - Click again → stops, processes with Faster-Whisper
   - Status changes: "⏳ Processing..." → "🔄 Transcribing..." → "✨ Refining..." → "✅ Done!"

2. **Text Submission**:
   - Type in text area → click submit (➤)
   - Directly refines with Cohere AI
   - Shows result in expandable container below

3. **Model Selection**:
   - Dropdown with 3 modes:
     - "Cohere - Command R7B" (default Cohere)
     - "Vibe Coder Mode" (developer-focused refinement)
     - "Casual Chatter Mode" (preserves casual tone)

### History Tab Functionality
1. **Sorting**: Dropdown (Latest to Old / Old to Latest)
2. **Search**: Real-time filtering by refined text
3. **Card Actions**:
   - Click card → opens TranscriptionDetailDialog
   - "⟲ Re-inject" → copies text back to clipboard
   - "×" Delete → removes from list AND persists to JSON file
4. **Data Persistence**: All delete operations save to `transcriptions_history.json`

### Animation & Effects
- **Button Hover**: 200ms color transition (QPropertyAnimation, OutCubic)
- **Glass Blur**: QGraphicsBlurEffect with 20px radius
- **Window Dragging**: Custom mousePressEvent/mouseMoveEvent handlers
- **Status Fade**: QTimer.singleShot for auto-hiding messages (2-3 seconds)

## Backend Integration Points

### Audio Pipeline
```
AudioRecorder (pyaudio) 
  → VAD filtering (webrtcvad) 
  → numpy array conversion 
  → SpeechToText (faster-whisper small model) 
  → raw text string
```

### AI Refinement Pipeline
```
Raw text input 
  → AIRefiner class 
  → Cohere API (command-r7b-12-2024) 
  → Mode-specific prompt template 
  → refined text output
```

### Data Storage
```python
# JSON Structure
{
  "version": "1.0",
  "created_at": "ISO timestamp",
  "transcriptions": [
    {
      "timestamp": "ISO timestamp",
      "mode": "vibe_coder",
      "raw_text": "original speech...",
      "refined_text": "cleaned text...",
      "paste_success": true,
      "text_length": 123
    }
  ]
}
```

## Configuration Files

### .env (Required)
```
CohereAPIKey=your_api_key_here
```

### config.py
- `WRITING_MODES` dict: Defines AI refinement behavior per mode
- `AUDIO_SAMPLE_RATE`: 16000 Hz
- `AUDIO_CHANNELS`: 1 (mono)
- `AUDIO_CHUNK_SIZE`: 1024

## Styling Approach

### PyQt6 StyleSheet Syntax
- All styling done via inline `setStyleSheet()` calls
- QSS (Qt Style Sheets) - CSS-like syntax
- Supports pseudo-states: `:hover`, `:pressed`, `:focus`, `:disabled`
- Component-specific selectors: `QPushButton::drop-down`, `QScrollBar::handle`

### Example Patterns
```python
# Gemini-style input container
setStyleSheet("""
    QFrame {
        background: rgba(45, 45, 50, 0.95);
        border-radius: 24px;
    }
""")

# Hover-enabled button
setStyleSheet("""
    QPushButton {
        background: rgba(70, 130, 255, 0.9);
        border: none;
        border-radius: 20px;
    }
    QPushButton:hover {
        background: rgba(90, 150, 255, 1);
    }
""")
```

## File Structure
```
writeforme/
├── frontend/
│   └── dashboard_v2.py (1362 lines - main UI file)
├── audio_recorder.py (Audio capture + VAD)
├── speech_to_text.py (Faster-Whisper integration)
├── ai_refiner.py (Cohere API wrapper)
├── config.py (App configuration)
├── transcriptions_history.json (Data persistence)
├── requirements.txt (Dependencies)
├── .env (API keys - gitignored)
└── HANDOFF.md (This file)
```

## Dependencies (requirements.txt)

```
pyaudio==0.2.14
SpeechRecognition==3.10.1
requests==2.31.0
pyperclip==1.8.2
pyautogui==0.9.54
numpy>=1.26.3
pillow>=10.2.0
keyboard==0.13.5
pynput>=1.7.6
cohere>=5.0.0
python-dotenv>=1.0.0
google-genai>=0.1.0
groq>=0.4.0
ollama>=0.6.0
colorama>=0.4.6
faster-whisper>=1.0.0
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.0.0
PyQt6>=6.0.0
```

## Running the Application

### Setup
```bash
# Create virtual environment
python -m venv venv

# Activate venv (Windows)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file with API key
echo "CohereAPIKey=your_api_key_here" > .env
```

### Launch Dashboard
```bash
python frontend\dashboard_v2.py
```

### Launch Main App (Background Service)
```bash
python main.py
```

## Current UI State & Recent Changes

### Latest Improvements (January 2026)
1. ✅ Window has 20px curved border radius (smooth corners)
2. ✅ Input redesigned to Gemini style - mic + submit on right
3. ✅ Model selector enhanced with better dropdown styling
4. ✅ Window controls moved to top-right corner (mounted at edge)
5. ✅ JSON persistence for history delete operations
6. ✅ Submit button handles typed text input with AI refinement
7. ✅ Sorting options in history tab (Latest/Old)
8. ✅ Detail dialog shows full transcription on card click

### Known Behaviors
- App uses `WindowStaysOnTopHint` (always on top)
- Frameless window requires custom drag implementation
- Status messages auto-hide after 2-3 seconds
- History loads from JSON on startup
- All transcriptions stored with timestamp, mode, raw/refined text

## UI Refinement Guidelines

### What Can Be Improved
1. **Responsiveness**: Currently fixed 1100x750px size
2. **Animations**: Add more micro-interactions (card hover, input focus)
3. **Loading States**: Better visual feedback during AI processing
4. **Empty States**: History tab needs empty state design
5. **Error Handling**: Visual error states for API failures
6. **Accessibility**: Keyboard navigation, screen reader support
7. **Theme Support**: Currently only dark mode available
8. **Model Selector**: Could show model status/availability indicators
9. **Input Box**: Could support markdown preview for refined text
10. **Export Functionality**: Currently has button but no implementation

### Styling Constraints
- Must maintain glassmorphism aesthetic
- Keep frameless window design
- Preserve 20px window border radius
- Use existing color palette for consistency
- All components must work with transparency layers

## Code Organization

### Class Methods Overview

**GlassDashboard Methods:**
- `setup_window()` - Configure frameless transparent window
- `setup_ui()` - Build main UI layout
- `create_sidebar()` - Left navigation panel
- `create_home_tab()` - Main interaction tab
- `create_history_tab()` - Transcription list
- `create_settings_tab()` - Configuration UI
- `create_stats_tab()` - Statistics display
- `load_mock_data()` - Load from JSON file
- `save_to_json()` - Persist to JSON file
- `render_cards()` - Update history display
- `on_search()` - Filter transcriptions
- `on_sort_changed()` - Apply sorting
- `on_delete()` - Delete + persist
- `on_reinject()` - Copy to clipboard
- `on_card_clicked()` - Show detail dialog
- `toggle_recording()` - Start/stop recording
- `submit_prompt()` - Process text input
- `switch_tab()` - Navigation logic
- `toggle_maximize()` - Window maximize
- `mousePressEvent/mouseMoveEvent/mouseReleaseEvent` - Window dragging
- `paintEvent()` - Custom window background

### Signal/Slot Connections
- Button clicks → method callbacks
- Card interactions → signal emissions
- Search input → real-time filtering
- Model selector → mode switching
- Timer events → auto-hide status

## Performance Considerations

### Optimization Points
- Audio processing runs in separate thread (AudioRecorder)
- VAD filtering reduces unnecessary processing
- Transcription history loaded once at startup
- Cards rendered on-demand (not all at once)
- JSON saves only on delete (not on every action)

### Memory Management
- Audio buffer cleared after transcription
- Queue objects for thread-safe communication
- Proper widget cleanup when removing cards
- No memory leaks in animation loops

## Security Notes

### API Keys
- Stored in `.env` file (gitignored)
- Loaded via python-dotenv
- Never hardcoded in source

### Data Privacy
- All audio processing happens locally (Faster-Whisper)
- Only refined text sent to Cohere API
- Transcription history stored locally in JSON
- No telemetry or analytics

## Troubleshooting

### Common Issues
1. **PyQt6 not found**: Install from requirements.txt
2. **Audio device errors**: Check PyAudio installation and microphone access
3. **API errors**: Verify Cohere API key in .env file
4. **Faster-Whisper slow**: Uses CPU by default, consider GPU setup
5. **Window dragging not working**: Ensure drag_area mouse events are connected

### Debug Mode
- Check console output for error messages
- All classes print status messages to stdout
- Use `print()` statements in paintEvent for visual debugging

## Next Steps for UI Refinement

### Priority 1 (High Impact)
- [ ] Add empty state design for history tab
- [ ] Implement loading spinner during AI processing
- [ ] Add error state visuals (API failures, network issues)
- [ ] Improve card hover animations
- [ ] Add keyboard shortcuts (Esc to close, Enter to submit)

### Priority 2 (Polish)
- [ ] Smooth transitions between tabs
- [ ] Input box focus state animation
- [ ] Better scrollbar styling
- [ ] Add tooltips to buttons
- [ ] Implement export functionality

### Priority 3 (Enhancement)
- [ ] Light theme support
- [ ] Resizable window with min/max constraints
- [ ] Custom fonts/icon system
- [ ] Settings persistence
- [ ] Statistics tab implementation

## Contact & Support

For questions about this handoff or further development:
- Review `.github/mistakes.md` for common pitfalls
- Check `.github/temp-todo-*.md` files for task tracking
- Refer to this document for architecture decisions

---

**Document Version**: 1.0  
**Last Updated**: January 14, 2026  
**Status**: Active Development
