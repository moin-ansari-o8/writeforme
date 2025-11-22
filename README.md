# WriteForMe

A local, offline AI-powered voice dictation tool inspired by [Wispr Flow](https://wisprflow.ai/). Uses continuous speech recognition and local Phi-3 Mini AI for intelligent text dictation.

## Features

- 🎙️ **Continuous Speech Recognition**: Records everything you say until you press stop
- 🤖 **Local AI Processing**: Uses Ollama (Phi-3 Mini) to refine and organize your speech
- 💾 **Data Persistence**: Automatically saves all transcriptions to `transcriptions_history.json` (never lose your work!)
- 📝 **7 Writing Modes**: 
  - Smart Dictation (default)
  - Professional Email
  - Casual Email
  - AI Prompt Writer (for developers)
  - Creative Writing
  - Grammar Correction Only
  - Technical Documentation
- 🎯 **Intelligent Model Selection**: Optimized for `phi3:mini` for fast, accurate results
- 📋 **Auto-Paste**: Automatically pastes refined text into focused input fields
- 💊 **Compact Pill UI**: Minimalist, draggable pill-shaped widget (280x60px)
- 🔒 **100% Local**: No cloud dependencies, all processing happens on your machine

## Workflow

1. **Launch**: Run `python main.py`
2. **Widget Appears**: Compact pill widget appears at bottom of screen
3. **Recording Starts**: Automatically begins recording audio
4. **Visualization**: Waveform shows your audio input in real-time
5. **User Speaks**: Continue speaking until you're done
6. **Click Stop (Square)**: Process your speech
7. **Processing UI**: Widget shows "Processing..." animation
8. **Auto-Paste & Save**: Refined text is saved to history and pasted automatically
9. **Auto-Hide**: Widget hides automatically when done

## Requirements

- Python 3.8+
- Ollama running locally with `phi3:mini` model
- Microphone
- Windows OS (tested on Windows)

## Installation

### 1. Install Python Dependencies

```bash
cd wispr_flow_local
pip install -r requirements.txt
```

**Note**: On Windows, you may need to install PyAudio separately:
```bash
pip install pipwin
pipwin install pyaudio
```

### 2. Install and Setup Ollama

1. Install Ollama from [ollama.ai](https://ollama.ai/)
2. Pull the required model:
   ```bash
   ollama pull phi3:mini
   ```
3. Ensure Ollama is running:
   ```bash
   ollama serve
   ```
   
**Note**: You can use other models by editing `config.py`.

## Usage

### Start the Application

```bash
python main.py
```

### Controls

- **Cancel Button** (Left 'X'): Discard current recording and hide widget
- **Stop Button** (Right Square): Process, save, and paste your speech
- **Drag**: Click and drag anywhere on the widget to reposition it

### Tips

- **Select the right mode** in `config.py` or via code (UI selector removed for compactness)
- Speak naturally - the AI will clean up filler words
- The widget visualizer shows your audio input in real-time
- Ensure your input field is focused before clicking Stop
- Check `transcriptions_history.json` if paste fails

## Writing Modes

See `MODEL_GUIDE.md` for detailed information about each mode. All modes now use `phi3:mini` by default for optimal speed/quality balance.

## Configuration

Edit `config.py` to customize:

- **Writing Modes**: Add custom modes or modify existing ones
- **AI Models**: Change which model each mode uses
- **AI Prompts**: Customize how each mode refines your text
- **Widget Position**: Adjust `WIDGET_WIDTH`, `WIDGET_HEIGHT`
- **Colors**: Customize `COLOR_VISUALIZER`, `COLOR_BUTTON_*`
- **Audio Settings**: Modify sample rate, chunk size, etc.

## Troubleshooting

### "AI connection test failed"
- Make sure Ollama is running: `ollama serve`
- Verify model is installed: `ollama list` (should show `phi3:mini`)

### "No audio recorded"
- Check microphone permissions
- Test microphone in system settings

### "Could not understand audio"
- Speak clearly and closer to the microphone
- Reduce background noise
- Check internet connection (needed for Google Speech Recognition)

### Paste not working
- Ensure an input field is focused before clicking Stop
- Check `transcriptions_history.json` - your text is safely saved there!

## Architecture

```
main.py              - Main application orchestrator
├── gui_widget.py    - Custom Tkinter pill widget
├── audio_recorder.py - Continuous audio recording (PyAudio)
├── speech_to_text.py - Speech recognition (Google SR)
├── ai_refiner.py    - Text refinement (Ollama/Phi-3)
├── paste_manager.py - Clipboard & auto-paste (PyAutoGUI)
├── data_storage.py  - JSON-based data persistence
└── config.py        - Configuration settings
```

## License

MIT License - Free to use and modify

## Credits

Inspired by [Wispr Flow](https://wisprflow.ai/) - making local voice dictation accessible to everyone!
