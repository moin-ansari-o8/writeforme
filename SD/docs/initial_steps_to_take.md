# Building WriteForMe (WisprFlow-like App)

## **STEP 0: Define Vision** ⏱️ 1 hour

Create `docs/vision.md`:
- What it does (one sentence)
- Who it's for
- How it must feel (fast, invisible, calm)

**Example:**  
_"WriteForMe is a local-first dictation assistant that turns speech into clean text and injects it anywhere with near-zero friction."_

---

## **STEP 1: Reverse Engineer WisprFlow** ⚠️ CRITICAL

Pick 5–7 key screenshots (dashboard, overlay, recording, settings)

For each screen document:
- What user sees
- What's clickable
- What happens on interaction
- What runs in background

**Output:** `docs/ui_breakdown.md`  
→ This prevents AI hallucination later

---

## **STEP 2: Define System Architecture**

Create `docs/system_design.md`:

### Core Components
- UI Renderer
- State Manager
- Audio Engine
- Transcription Engine
- Text Injector
- Settings & Persistence

### Non-Negotiable Rules
- UI never blocks
- Audio/AI run off UI thread
- Every long task is cancellable
- State is single source of truth

**If a tool violates these → reject it**

---

## **STEP 3: Choose Tech Stack**

**Backend:**
- Python 3.11+ (async)
- `sounddevice` + Silero VAD (audio)
- `faster-whisper` (local transcription)
- `pynput` (text injection)

**UI:**
- Phase 1–2: Flet (for speed)
- Phase 3: Migrate if needed

**Packaging:**
- PyInstaller (later)

---

## **STEP 4: Lock Repo Structure**

```
writeforme/
├── docs/
│   ├── vision.md
│   ├── ui_breakdown.md
│   └── system_design.md
├── src/
│   ├── state/
│   │   └── app_state.py
│   ├── engine/
│   │   ├── audio.py
│   │   ├── transcriber.py
│   │   └── injector.py
│   ├── ui/
│   │   ├── dashboard.py
│   │   ├── overlay.py
│   │   └── theme.py
│   └── main.py
└── requirements.txt
```

---

## **STEP 5: Build Order** ⚠️ DO NOT SKIP

### Phase 1: Core Engine (NO UI)
- Audio capture → silence detection → transcribe → terminal output
- **If not fast → stop and fix**

### Phase 2: State Manager
- Single object controls all state: `is_recording`, `current_text`, `last_error`, `mode`
- UI only reads state, never modifies directly

### Phase 3: UI Rendering
- Reflect state, not control logic
- Dashboard shows stats
- Overlay mirrors recording state
- **NO AI calls inside UI files**

### Phase 4: Text Injection
- Inject after transcription
- Handle cancellation safely
- No repeated typing bugs

### Phase 5: Polish
- Streaming text
- Cancel/restart
- Error handling
- Settings persistence
- **Animations come last**

---

## **STEP 6: AI Prompting Strategy**

❌ **NEVER:** "Build the app"

✅ **ALWAYS:** "Implement ONLY `src/engine/audio.py`. Do not touch UI. Respect async boundaries."

---

## **STEP 7: Performance Checklist** ⚠️ NON-OPTIONAL

Before calling it done, verify:
- ✅ UI FPS doesn't drop while recording
- ✅ Cancelling is instant
- ✅ Transcription doesn't freeze UI
- ✅ Overlay never steals focus

**If one fails → architecture issue, not styling**

---

## **STEP 8: Packaging & Branding** (LAST)

- App icon
- Startup behavior
- Auto-launch (optional)
- Installer

---

## **🎯 Core Truth**

You don't need more tools.  
You need **discipline before dopamine**.

Most builders fail because they:
- ❌ Code before thinking
- ❌ Choose UI before system
- ❌ Trust AI before structure

**You won't — if you follow this.**
