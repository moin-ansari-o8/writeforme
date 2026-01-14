# 🚀 Quick Start Guide - WriteForMe with Hotkeys

## Prerequisites

1. **Install required packages** (already done):
   ```bash
   pip install -r requirements.txt
   ```

2. **Cohere API Key Setup:**
   - Create `.env` file in project root (already exists)
   - Add your Cohere API key: `CohereAPIKey=your_key_here`

---

## Testing

### Step 1: Test Hotkey Detection (Optional)
```bash
cd W:\workplace-1\writeforme
python test_hotkeys.py
```
- Try pressing Win+Shift and Win+Ctrl+Shift
- You should see detection messages
- Press Ctrl+C to exit

### Step 2: Run WriteForMe
```bash
cd W:\workplace-1\writeforme
python main.py
```

**Note:** You may need to run as Administrator for global hotkeys to work in all apps.

---

## Usage

### Push-to-Talk Mode (Quick Dictation)
1. **Hold** Win+Shift
2. Speak your text
3. **Release** Win+Shift
4. Text processes and pastes automatically

### Toggle Mode (Longer Sessions)
1. **Press** Win+Ctrl+Shift once to start
2. Speak as much as you want
3. **Press** Win+Ctrl+Shift again to stop
4. Text processes and pastes automatically

---

## What You'll See

1. **On Hotkey Press:**
   - Visualizer popup appears at bottom-center
   - Audio waveform shows you're recording

2. **During Processing:**
   - Visualizer shows "processing" animation
   - Takes 2-5 seconds depending on audio length

3. **After Completion:**
   - Text appears at cursor position
   - Visualizer disappears
   - Ready for next dictation

---

## Troubleshooting

### Hotkeys Not Working?
- **Run as Administrator** - Right-click terminal → "Run as Administrator"
- Some apps (like Task Manager) block global hotkeys

### No Audio Recording?
- Check microphone permissions
- Verify microphone is working in Windows settings

### AI Not Refining?
- Check `.env` file has valid Cohere API key
- Run `python test_cohere.py` to verify API connection
- Check API usage limits (Trial: 40 calls, Monthly: 1000 calls)

### Visualizer Not Appearing?
- Check if GUI is hidden behind other windows
- Try Win+Shift in an empty area of desktop first

---

## Tips

✅ **Best Practices:**
- Speak clearly and at normal pace
- Wait 0.5s after pressing hotkey before speaking
- Don't release too quickly in push-to-talk mode
- Use toggle mode for dictating longer paragraphs

✅ **Performance:**
- First dictation may be slower (model loading)
- Subsequent dictations are faster
- Keep sentences under 30 seconds for best results

---

## Next Steps

Once you verify it works:
1. Consider adding system tray icon
2. Build settings UI for customizing hotkeys
3. Create dashboard for viewing history
4. Package as standalone .exe

---

**Status:** Ready to test!  
**Run:** `python main.py` (as Administrator)
