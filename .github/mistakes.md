# Historical Mistakes Log - WriteForMe

> This file tracks all past mistakes to prevent repetition.
> **NEVER delete entries** - only append new ones.

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

**Last Updated:** 2026-01-14
