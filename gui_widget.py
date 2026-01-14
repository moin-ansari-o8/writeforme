"""
GUI Widget - Sleek Capsule Design
"""
import tkinter as tk
from tkinter import Canvas
import math
import config
import random

class WidgetGUI:
    def __init__(self, on_cancel_callback, on_stop_callback):
        self.on_cancel = on_cancel_callback
        self.on_stop = on_stop_callback
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Wispr Flow Local")
        
        # Window settings - configure properly to avoid disabling other windows
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        
        # Set transparency key
        self.root.attributes('-transparentcolor', config.COLOR_TRANSPARENT)
        self.root.configure(bg=config.COLOR_TRANSPARENT)
        
        # Set window size
        self.root.geometry(f"{config.WIDGET_WIDTH}x{config.WIDGET_HEIGHT}")
        
        # Don't grab focus or disable other windows
        self.root.attributes('-disabled', False)
        
        # Position at bottom center
        self._position_window()
        
        # Visualizer data
        self.num_bars = 8 # Reduced for cleaner, more spacious look
        self.audio_levels = [0.01] * self.num_bars
        self.target_levels = [0.01] * self.num_bars
        
        # Smoothing constants
        self.attack = 0.4   # Fast jump up
        self.release = 0.15 # Slow glide down
        
        # VAD state
        self.is_speech_active = False
        self.hangover_frames = 0
        self.max_hangover = 15 # ~300ms at 20ms smoothing loop
        
        self.is_running = True
        self.processing_angle = 0
        
        # Create Canvas
        self.canvas = Canvas(
            self.root,
            width=config.WIDGET_WIDTH,
            height=config.WIDGET_HEIGHT,
            bg=config.COLOR_TRANSPARENT,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind events
        self._make_draggable()
        
        # Initial State
        self.state = "recording" # recording, processing
        self._draw_ui()
        
        # Start smoothing loop
        self._smooth_visualizer()
        
    def _position_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - config.WIDGET_WIDTH) // 2
        y = screen_height - config.WIDGET_HEIGHT - 60
        self.root.geometry(f"+{x}+{y}")

    def _make_draggable(self):
        self.canvas.bind('<Button-1>', self._start_drag)
        self.canvas.bind('<B1-Motion>', self._on_drag)
        
    def _start_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y
        
    def _on_drag(self, event):
        x = self.root.winfo_x() + (event.x - self.drag_x)
        y = self.root.winfo_y() + (event.y - self.drag_y)
        self.root.geometry(f"+{x}+{y}")

    def _draw_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1, x2, y1 + radius,
            x2, y2 - radius,
            x2, y2, x2 - radius, y2,
            x1 + radius, y2,
            x1, y2, x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def _draw_ui(self):
        self.canvas.delete("all")
        
        # Draw Pill Background (Capsule) - Perfectly rounded ends
        h = config.WIDGET_HEIGHT
        w = config.WIDGET_WIDTH
        r = h // 2
        
        # Left circle
        self.canvas.create_oval(0, 0, h, h, fill=config.COLOR_BACKGROUND, outline="")
        # Right circle
        self.canvas.create_oval(w - h, 0, w, h, fill=config.COLOR_BACKGROUND, outline="")
        # Middle rectangle
        self.canvas.create_rectangle(r, 0, w - r, h, fill=config.COLOR_BACKGROUND, outline="")
        
        if self.state == "recording":
            self._draw_recording_ui()
        elif self.state == "processing":
            self._draw_processing_ui()
            
    def _draw_recording_ui(self):
        cy = config.WIDGET_HEIGHT // 2
        
        # Cancel Button (Left)
        cx_cancel = config.WIDGET_HEIGHT // 2
        btn_radius = 9  # Slightly smaller for compact design
        self.canvas.create_oval(
            cx_cancel - btn_radius, cy - btn_radius,
            cx_cancel + btn_radius, cy + btn_radius,
            fill=config.COLOR_BUTTON_CANCEL, outline="", tags="btn_cancel"
        )
        self.canvas.create_text(cx_cancel, cy, text="×", fill="white", font=("Arial", 11), tags="btn_cancel")
        
        # Stop Button (Right - No menu button anymore)
        cx_stop = config.WIDGET_WIDTH - (config.WIDGET_HEIGHT // 2)  # Positioned at right edge
        
        # Circular Red Button with White Square
        self.canvas.create_oval(
            cx_stop - btn_radius, cy - btn_radius,
            cx_stop + btn_radius, cy + btn_radius,
            fill=config.COLOR_BUTTON_STOP, outline="", tags="btn_stop"
        )
        # Small square icon
        s = 3
        self.canvas.create_rectangle(cx_stop-s, cy-s, cx_stop+s, cy+s, fill="white", outline="", tags="btn_stop")
        
        # Visualizer (Center) - balanced between cancel and stop
        self._draw_visualizer_bars(end_x_offset=28) # Adjusted for single button on right
        
        # Bind clicks
        self.canvas.tag_bind("btn_cancel", "<Button-1>", lambda e: self.on_cancel())
        self.canvas.tag_bind("btn_stop", "<Button-1>", lambda e: self.on_stop())

    def _draw_visualizer_bars(self, end_x_offset=45):
        cy = config.WIDGET_HEIGHT // 2
        
        # FIXED LAYOUT for perfect spacing
        # Instead of calculating spacing from width, we define it fixed
        bar_width = 2
        spacing = 5  # Increased spacing for fewer bars
        
        # Calculate total width of the visualizer group
        total_width = (self.num_bars * bar_width) + ((self.num_bars - 1) * spacing)
        
        # Center the group dynamically
        # Available width center point needs to be calculated carefully
        # Or we just center it in the whole widget, but biased if buttons are uneven?
        # Let's center it in the available space between buttons
        
        start_x_limit = 32 # Space for cancel button (reduced)
        end_x_limit = config.WIDGET_WIDTH - end_x_offset # Space for stop button
        
        available_center = start_x_limit + (end_x_limit - start_x_limit) / 2
        start_x = available_center - (total_width / 2)
        
        max_height = 10
        
        for i, level in enumerate(self.audio_levels):
            # Precise x calculation
            x = start_x + i * (bar_width + spacing) + (bar_width / 2)
            
            # Use a non-linear scaling for better low-volume visibility
            h = max(1.5, math.sqrt(level) * max_height)
            
            self.canvas.create_line(
                x, cy - h, x, cy + h,
                fill=config.COLOR_VISUALIZER, width=bar_width, capstyle=tk.ROUND
            )

    def _draw_processing_ui(self):
        cy = config.WIDGET_HEIGHT // 2
        cx = config.WIDGET_WIDTH // 2
        
        # Smooth pulsing dots
        num_dots = 3
        dot_spacing = 12
        for i in range(num_dots):
            offset = (i - 1) * dot_spacing
            # Pulse based on angle
            pulse = math.sin(math.radians(self.processing_angle + i * 60)) * 0.5 + 0.5
            size = 2 + pulse * 2
            
            # Simulate alpha with grey levels
            val = int(150 + pulse * 105)
            color = f"#{val:02x}{val:02x}{val:02x}"
            
            self.canvas.create_oval(
                cx + offset - size, cy - size,
                cx + offset + size, cy + size,
                fill=color, outline=""
            )

    def _smooth_visualizer(self):
        if not self.is_running: return
        
        # Advanced Smoothing (EMA with Attack/Release)
        changed = False
        for i in range(self.num_bars):
            # Move current level towards target with different speeds
            diff = self.target_levels[i] - self.audio_levels[i]
            
            if diff > 0:
                # Attack: Fast jump up
                self.audio_levels[i] += diff * self.attack
            else:
                # Release: Slow glide down
                self.audio_levels[i] += diff * self.release
            
            # Slowly decay target level
            self.target_levels[i] *= 0.85
            if self.target_levels[i] < 0.01: self.target_levels[i] = 0.01
            
            if abs(diff) > 0.001:
                changed = True
        
        # Update hangover counter
        if self.hangover_frames > 0:
            self.hangover_frames -= 1
        else:
            self.is_speech_active = False
            
        if self.state == "processing":
            self.processing_angle = (self.processing_angle + 10) % 360
            changed = True
            
        if changed:
            self._draw_ui()
            
        self.root.after(20, self._smooth_visualizer)

    def update_visualizer(self, data):
        """Update visualizer with FFT frequency bands and VAD status"""
        if self.state != "recording" or data is None: return
        
        bands, is_speech = data
        
        # Update speech state with hangover
        if is_speech:
            self.is_speech_active = True
            self.hangover_frames = self.max_hangover
            
        # Only update targets if speech is active (or within hangover period)
        if not self.is_speech_active:
            return
            
        # bands is a list of 18 floats from FFT
        for i in range(min(len(bands), self.num_bars)):
            # Sensitivity adjustment per band
            boost = 1.0 + (i / self.num_bars) * 2.0
            val = (bands[i] / 5000.0) * boost
            
            # Apply non-linear scaling to make it "pop"
            normalized_val = min(val, 1.0)
            
            # Update target only if higher to prevent flickering
            if normalized_val > self.target_levels[i]:
                self.target_levels[i] = normalized_val

    def show_processing(self):
        self.state = "processing"
        
    def show_recording(self):
        self.state = "recording"
        
    def get_current_mode(self):
        return "vibe_coder"

    def show(self):
        self.root.deiconify()
        
    def hide(self):
        self.root.withdraw()
        
    def start(self):
        self.root.mainloop()
        
    def destroy(self):
        self.is_running = False
        self.root.quit()
        self.root.destroy()
