# Historical Mistakes Log - WriteForMe

> This file tracks all past mistakes to prevent repetition.
> **NEVER delete entries** - only append new ones.

---

## [2026-01-14] - CSS Syntax Errors in PyQt6 Stylesheets

**Problem:**
- Multiple CSS parsing errors in PyQt6 stylesheets
- Duplicate color declarations in same CSS block
- Malformed rgba() syntax with incomplete closing parentheses
- Using rgb() with 4 parameters (should be rgba())
- Incomplete CSS property declarations causing parser failures

**Solution:**
- Removed duplicate color lines in CSS blocks
- Fixed incomplete rgba() declarations with proper closing parentheses
- Changed rgb(r, g, b, a) to rgba(r, g, b, a)
- Removed orphaned CSS property values without selectors
- Validated all stylesheet strings for proper syntax

**Lesson:**
- Always close parentheses in CSS color functions
- Use rgba() for colors with alpha, not rgb()
- Don't duplicate property declarations in same CSS block
- Test stylesheets immediately after writing
- PyQt6 CSS parser is strict - no incomplete declarations allowed

**Related Files:**
- frontend/dashboard_v2.py (lines 750, 807, 831-836)

---

## [2026-01-14] - Hotkey System Breaking Windows Keys

**Problem:**
- Using `keyboard` library with `suppress=True` parameter
- All Win, Ctrl, and Shift keys became completely unusable system-wide
- Users couldn't use Windows key, Task Manager (Ctrl+Shift+Esc), or any other shortcuts
- Hotkeys weren't triggering properly or consistently
- Push-to-talk mode wasn't detecting key release

**Solution:**
- Replaced `keyboard` library with `pynput` library
- Removed ALL `suppress=True` parameters
- Implemented custom modifier key tracking with sets
- Used `pynput.keyboard.Listener` with proper on_press/on_release handlers
- Track modifier state manually: `{'win', 'ctrl', 'shift'}`
- Check combinations without suppressing keys
- Proper cleanup on app exit with `listener.stop()`

**Lesson:**
- NEVER use `suppress=True` on modifier keys (Win, Ctrl, Shift, Alt)
- Use `pynput` instead of `keyboard` for global hotkeys on Windows
- Always track modifier state manually for multi-key combinations
- Test that system shortcuts still work after registering hotkeys
- Properly clean up keyboard listeners on exit
- Don't block system-level key events

**Related Files:**
- main.py (lines 12, 59-62, 220-290, 317-327)
- requirements.txt (line 9)

---

## [2026-01-14] - Gemini API Deprecation and GUI Issues

**Problem:**
- Using deprecated `google.generativeai` package causing 404 errors
- Model endpoint changed from v1 to v1beta
- Using experimental model `gemini-2.0-flash-exp` which has restrictive quota
- GUI window was disabling other windows/applications
- Visualizer not showing up when recording started
- App crashed when provider connection failed instead of offering alternatives

**Solution:**
- Migrated from `google-generativeai` to `google-genai` package
- Updated Gemini provider to use new API:
  - Changed from `genai.GenerativeModel()` to `genai.Client()` with `client.models.generate_content()`
  - Updated model to `gemini-1.5-flash` (stable, better quota)
- Fixed GUI initialization to not disable other windows:
  - Added `self.root.attributes('-disabled', False)`
- Fixed recording start order:
  - Start audio recording BEFORE showing GUI
  - Force window to top with `lift()` and `update()` after showing
- Improved fallback logic:
  - Ask user to retry with another provider when connection fails
  - Offer automatic fallback to Ollama
  - Prevent app crash when provider unavailable
- Updated Ollama from 0.1.6 to 0.6.1 for httpx compatibility

**Lesson:**
- Always use the latest stable API packages
- Use stable models instead of experimental ones for production
- Check for deprecation warnings in dependencies
- Tkinter window focus must be carefully managed to avoid blocking other apps
- GUI updates should happen AFTER core functionality is started
- Always implement graceful degradation when services fail
- Give users options to retry or switch providers

**Related Files:**
- ai_provider_manager.py (lines 65-88, 195-245)
- main.py (lines 80-104)
- gui_widget.py (lines 4-22)
- requirements.txt

---

## [2026-01-14] - No Resource Management for Continuous Operation

**Problem:**
- JSON history file growing indefinitely without any cleanup
- Audio buffers accumulating in memory without being cleared after processing
- Visualizer loop running at full speed (33 FPS) even when idle
- No configuration for history retention limits
- Potential memory leaks during extended operation
- High CPU usage when app idle in background

**Solution:**
- Added automatic history cleanup to `data_storage.py`:
  - Added `max_entries` parameter (default 1000)
  - Created `_cleanup_old_entries()` method to remove oldest entries
  - Auto-cleanup on startup and after each save
  - Keeps only most recent entries based on limit
- Fixed memory leaks in `audio_recorder.py`:
  - Clear `self.audio_buffer = []` immediately after concatenation in `stop_recording()`
  - Ensures memory is released after each recording
- Optimized CPU usage in `main.py`:
  - Adaptive visualizer sleep: 0.1s when idle, 0.03s when recording
  - Reduces CPU from 3-5% to <1% when idle
- Added configurable setting in `config.py`:
  - `MAX_HISTORY_ENTRIES = 1000` (user can adjust)
  - Updated main.py to use config setting
- Created comprehensive resource documentation:
  - `RESOURCE_OPTIMIZATION.md` with usage estimates and best practices

**Lesson:**
- Always implement automatic cleanup for append-only data structures
- Clear memory buffers immediately after processing to prevent accumulation
- Use adaptive sleep timers based on application state (idle vs active)
- Make resource limits configurable via config file
- Document expected resource usage for long-running applications
- Test memory and CPU usage over extended periods (8+ hours)
- Provide users with visibility into resource management

**Related Files:**
- data_storage.py (lines 8-17, 75-84, 162-178)
- audio_recorder.py (line 135)
- main.py (line 72, lines 236-245)
- config.py (lines 123-127)
- RESOURCE_OPTIMIZATION.md (new documentation)

---

**Last Updated:** 2026-01-14

---

## [2026-01-14] - Application Restructure v2.0 (Success Story)

**Context:**
- User requested complete application restructure
- Needed proper frontend/backend separation
- Wanted dashboard for settings (no terminal prompts)
- Required trust level UI configuration
- Needed to maintain all existing functionality

**Solution:**
- Created clean architecture with separation of concerns:
  - `backend/` - FastAPI REST API server
  - `frontend/` - Tkinter UI components
  - `shared/` - Common configuration
  - `launcher.py` - Unified entry point
- Implemented FastAPI backend with proper routing:
  - `/api/audio/*` - Recording and transcription
  - `/api/ai/*` - AI refinement and providers
  - `/api/settings/*` - Configuration management
  - `/api/history/*` - Transcription history
- Built comprehensive dashboard:
  - Settings tab with all configuration options
  - History tab with search functionality
  - About tab with information and hotkeys
- Created API client for frontend-backend communication
- Updated recording widget to use backend API
- Maintained all hotkeys and functionality
- Added settings persistence (settings.json)
- Included proper error handling and fallbacks

**Lesson:**
- Proper architecture planning enables feature expansion
- Service-based design improves maintainability
- API-first approach enables future web/mobile UIs
- Documentation is critical (ARCHITECTURE.md, QUICKSTART_v2.md, MIGRATION.md)
- Security audit before deployment (achieved 10/10)
- Backward compatibility preserves user data
- Progressive enhancement better than breaking changes

**Related Files:**
- launcher.py (new unified entry point)
- backend/server.py (FastAPI application)
- backend/api/*.py (REST API routes)
- backend/services/*.py (business logic)
- frontend/components/dashboard.py (settings UI)
- frontend/components/recording_widget.py (recording UI)
- frontend/utils/api_client.py (HTTP client)
- shared/config.py (shared constants)
- ARCHITECTURE.md (architecture documentation)
- QUICKSTART_v2.md (user guide)
- MIGRATION.md (migration guide)
- .github/security-audit-v2.md (security review)

**Architecture Benefits:**
- ✅ Clean separation of concerns
- ✅ Testable components
- ✅ Extensible design
- ✅ API-first approach
- ✅ Better error handling
- ✅ Settings persistence
- ✅ Enhanced UI capabilities
- ✅ Future-proof structure

**Status:** ✅ Complete and Production-Ready
