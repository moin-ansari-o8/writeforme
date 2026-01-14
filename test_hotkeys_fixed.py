"""
Test Hotkey Detection with Better Logic
"""
import keyboard
import time

print("=" * 60)
print("Hotkey Detection Test (Fixed)")
print("=" * 60)
print("\nTesting hotkeys:")
print("  1. Win+Shift (hold and release)")
print("  2. Win+Ctrl+Shift (press to toggle)")
print("\nPress Ctrl+C to exit\n")
print("-" * 60)

is_toggle_active = False
is_recording = False

def on_toggle():
    global is_toggle_active
    if is_toggle_active:
        print("✓ Win+Ctrl+Shift - Toggle OFF")
        is_toggle_active = False
    else:
        print("✓ Win+Ctrl+Shift - Toggle ON")
        is_toggle_active = True

def on_push_to_talk():
    global is_recording
    if not is_toggle_active:
        print("✓ Win+Shift - PRESSED (hold mode started)")
        is_recording = True
        
        # Monitor release
        def monitor_release():
            while keyboard.is_pressed('win') and keyboard.is_pressed('shift'):
                time.sleep(0.05)
            if is_recording:
                print("✓ Win+Shift - RELEASED (stopping)")
        
        import threading
        threading.Thread(target=monitor_release, daemon=True).start()

# Register hotkeys - toggle first (higher priority)
keyboard.add_hotkey('win+ctrl+shift', on_toggle, suppress=True)
keyboard.add_hotkey('win+shift', on_push_to_talk, suppress=True, trigger_on_release=False)

print("Listening for hotkeys...")
print("(This will help debug the issue)\n")

try:
    keyboard.wait()
except KeyboardInterrupt:
    print("\n\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
