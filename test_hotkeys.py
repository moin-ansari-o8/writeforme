"""
Quick Test - Hotkey Detection
Run this to verify hotkeys are detected properly before running full app
"""
import keyboard
import time

print("=" * 60)
print("Hotkey Detection Test")
print("=" * 60)
print("\nTesting if hotkeys can be detected...")
print("Try pressing:")
print("  1. Win+Shift (hold and release)")
print("  2. Win+Ctrl+Shift (press)")
print("\nPress Ctrl+C to exit\n")
print("-" * 60)

def on_win_shift():
    print("✓ Win+Shift detected!")

def on_win_ctrl_shift():
    print("✓ Win+Ctrl+Shift detected!")

def on_shift_press(e):
    if keyboard.is_pressed('win'):
        print("  → Win+Shift pressed")

def on_shift_release(e):
    if keyboard.is_pressed('win'):
        print("  → Win+Shift released")

# Register handlers
keyboard.on_press_key('shift', on_shift_press, suppress=False)
keyboard.on_release_key('shift', on_shift_release, suppress=False)
keyboard.add_hotkey('win+ctrl+shift', on_win_ctrl_shift, suppress=False)

print("Listening for hotkeys...")
print("(This confirms keyboard library is working)\n")

try:
    keyboard.wait()  # Block forever
except KeyboardInterrupt:
    print("\n\n" + "=" * 60)
    print("Test Complete!")
    print("If you saw the messages above, hotkeys are working ✓")
    print("=" * 60)
