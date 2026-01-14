# WriteForMe Vision

## What It Does

**WriteForMe is a local-first desktop dictation assistant that captures speech via keybindings, transcribes it, refines it with AI, and injects the polished text anywhere — instantly.**

---

## Who It's For

- Knowledge workers who think faster than they type
- Content creators who need friction-free dictation
- Anyone who wants clean, AI-polished text from raw speech

---

## How It Must Feel

- **Fast** — No waiting. Record → Process → Inject in seconds
- **Invisible** — No window switching. Works in any app
- **Calm** — Minimal UI. Just keybindings and a small visualizer

---

## Core Features

### 1. **Dual Recording Modes**

**Push-to-Talk Mode** (Win+Shift)
- Hold keys down → records speech
- Release keys → stops, processes, injects text
- Perfect for quick dictation

**Toggle Mode** (Win+Ctrl+Shift)
- Press once → starts recording
- Press again → stops and processes
- Perfect for longer dictation sessions

### 2. **Visual Feedback**

- Small visualizer popup appears during recording
- Shows audio waveform/indicator (already built in `writeforme` folder)
- Disappears after injection
- **Question:** Should we enhance the existing visualizer or is it good enough?

### 3. **AI Refinement Pipeline**

Speech → Transcription → AI Polish → Clean Text Output
- Raw speech converted to text
- AI refines grammar, punctuation, clarity
- Final polished text injected at cursor

### 4. **Dashboard UI**

Centralized app window for:
- **History** — View all past transcriptions
- **Settings** — Configure keybindings, AI model, audio device
- **Stats** — Usage patterns, word count, session history
- **Management** — Edit, delete, re-inject previous recordings

---

## Non-Negotiable Principles

1. **Local-First** — All processing happens on device (privacy)
2. **Zero Friction** — Never leave current app to dictate
3. **Instant Response** — UI never blocks, audio never lags
4. **Keybinding-First** — Mouse optional, keyboard sufficient
5. **Cancellable** — Every operation can be stopped mid-process

---

## Technical Must-Haves

- **Async Architecture** — Audio, AI, UI run independently
- **Background Processing** — App runs in system tray
- **Global Hotkeys** — Work from any application
- **Cross-App Injection** — Text appears where cursor is
- **State Persistence** — History survives restarts

---

## Success Criteria

✅ Can dictate and inject text in < 3 seconds  
✅ Keybindings work in any app (browser, IDE, notepad)  
✅ Visualizer appears instantly on keypress  
✅ Dashboard loads full history without lag  
✅ Cancelling mid-recording is instant  
✅ App uses < 200MB RAM when idle  

---

## What It's NOT

❌ Cloud-based service  
❌ Heavyweight electron app  
❌ Subscription model  
❌ Privacy-invasive analytics  
❌ Feature-bloated Swiss Army knife  

---

## Inspiration

**WisprFlow** — We match their keybinding UX and recording flow, but we own the full stack and keep everything local.

---

**Last Updated:** January 14, 2026
