# WriteForMe

A local, offline AI-powered voice dictation tool inspired by [Wispr Flow](https://wisprflow.ai/). Uses continuous speech recognition and local LLaMA AI for intelligent text dictation.

## Features

- 🎙️ **Continuous Speech Recognition**: Records everything you say until you press stop
- 🤖 **Local AI Processing**: Uses Ollama models to refine and organize your speech
- 📝 **7 Writing Modes**: 
  - Smart Dictation (default)
  - Professional Email
  - Casual Email
  - AI Prompt Writer (for developers)
  - Creative Writing
  - Grammar Correction Only
  - Technical Documentation
- 🎯 **Intelligent Model Selection**: Each mode uses the optimal AI model for that task
- 📋 **Auto-Paste**: Automatically pastes refined text into focused input fields
- 🎨 **Clean Widget UI**: Bottom-screen overlay with mode selector and real-time visualizer
- 🔒 **100% Local**: No cloud dependencies, all processing happens on your machine

## Workflow

1. **Launch**: Run `python main.py`
2. **Widget Appears**: Small overlay at bottom of screen with mode selector
3. **Select Mode**: Choose writing mode from dropdown (Default, Professional Email, Casual, etc.)
4. **Recording Starts**: Automatically begins recording audio
5. **Visualization**: Waveform shows your audio input in real-time
6. **User Speaks**: Continue speaking until you're done
7. **Click Stop**: Process your speech
8. **AI Processing**: Transcription sent to optimal AI model based on selected mode
9. **Auto-Paste**: Refined text is pasted automatically into your focused input field

## Requirements

- Python 3.8+
- Ollama running locally with models (Mistral, Gemma3, Llama3.2, DeepSeek R1)
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
2. Pull recommended models:
   ```bash
   ollama pull mistral:7b-instruct
   ollama pull gemma3
   ollama pull llama3.2
   ollama pull deepseek-r1:8b
   ```
3. Ensure Ollama is running:
   ```bash
   ollama serve
   ```
   
**Note**: You can use any models you have installed. See `MODEL_GUIDE.md` for detailed model recommendations.

## Usage

### Start the Application

```bash
python main.py
```

### Controls

- **Mode Selector** (top): Choose writing mode from dropdown
- **Cancel Button** (left): Discard current recording and restart
- **Stop Button** (right): Process and paste your speech
- **Drag**: Click and drag the widget to reposition it

### Tips

- **Select the right mode** for your task (email, creative writing, etc.)
- Speak naturally - the AI will clean up filler words
- Wait for "Ready for next dictation" before starting again
- The widget visualizer shows your audio input in real-time
- Ensure your input field is focused before clicking Stop

## Writing Modes

See `MODEL_GUIDE.md` for detailed information about each mode and which AI model it uses.

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
- Verify model is installed: `ollama list`

### "No audio recorded"
- Check microphone permissions
- Test microphone in system settings

### "Could not understand audio"
- Speak clearly and closer to the microphone
- Reduce background noise
- Check internet connection (needed for Google Speech Recognition)

### Paste not working
- Ensure an input field is focused before clicking Stop
- Try clicking in a text editor first

## Architecture

```
main.py              - Main application orchestrator
├── gui_widget.py    - Tkinter widget with visualizer
├── audio_recorder.py - Continuous audio recording (PyAudio)
├── speech_to_text.py - Speech recognition (Google SR)
├── ai_refiner.py    - Text refinement (Ollama/LLaMA)
├── paste_manager.py - Clipboard & auto-paste (PyAutoGUI)
└── config.py        - Configuration settings
```

## License

MIT License - Free to use and modify

## Credits

Inspired by [Wispr Flow](https://wisprflow.ai/) - making local voice dictation accessible to everyone!
