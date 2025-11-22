"""
GUI Widget - Compact Pill Design
"""
import tkinter as tk
from tkinter import Canvas
import math
import config

class WidgetGUI:
    def __init__(self, on_cancel_callback, on_stop_callback):
        self.on_cancel = on_cancel_callback
        self.on_stop = on_stop_callback
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Wispr Flow Local")
        
        # Window settings
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        
        # Set transparency key
        self.root.attributes('-transparentcolor', config.COLOR_TRANSPARENT)
        self.root.configure(bg=config.COLOR_TRANSPARENT)
        
        # Set window size
        self.root.geometry(f"{config.WIDGET_WIDTH}x{config.WIDGET_HEIGHT}")
        
        # Position at bottom center
        self._position_window()
        
        # Visualizer data
        self.audio_levels = [0] * 20  # Fewer bars for compact design
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
        self.canvas.bind('<Button-1>', self._on_click)
        self._make_draggable()
        
        # Initial State
        self.state = "recording" # recording, processing
        self._draw_ui()
        
    def _position_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - config.WIDGET_WIDTH) // 2
        y = screen_height - config.WIDGET_HEIGHT - 80
        self.root.geometry(f"+{x}+{y}")

    def _make_draggable(self):
        self.canvas.bind('<Button-1>', self._start_drag, add='+')
        self.canvas.bind('<B1-Motion>', self._on_drag, add='+')
        
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
        
        # Draw Pill Background
        self._draw_rounded_rect(
            0, 0, config.WIDGET_WIDTH, config.WIDGET_HEIGHT, 
            radius=30, 
            fill=config.COLOR_BACKGROUND
        )
        
        if self.state == "recording":
            self._draw_recording_ui()
        elif self.state == "processing":
            self._draw_processing_ui()
            
    def _draw_recording_ui(self):
        # Cancel Button (Left)
        btn_radius = 18
        cy = config.WIDGET_HEIGHT // 2
        cx_cancel = 35
        
        # Grey Circle
        self.canvas.create_oval(
            cx_cancel - btn_radius, cy - btn_radius,
            cx_cancel + btn_radius, cy + btn_radius,
            fill=config.COLOR_BUTTON_CANCEL, outline="", tags="btn_cancel"
        )
        # X Icon
        x_size = 6
        self.canvas.create_line(
            cx_cancel - x_size, cy - x_size, cx_cancel + x_size, cy + x_size,
            fill="white", width=2, tags="btn_cancel"
        )
        self.canvas.create_line(
            cx_cancel + x_size, cy - x_size, cx_cancel - x_size, cy + x_size,
            fill="white", width=2, tags="btn_cancel"
        )
        
        # Stop Button (Right)
        cx_stop = config.WIDGET_WIDTH - 35
        
        # Red Circle
        self.canvas.create_oval(
            cx_stop - btn_radius, cy - btn_radius,
            cx_stop + btn_radius, cy + btn_radius,
            fill=config.COLOR_BUTTON_STOP, outline="", tags="btn_stop"
        )
        # Square Icon
        sq_size = 5
        self.canvas.create_rectangle(
            cx_stop - sq_size, cy - sq_size, cx_stop + sq_size, cy + sq_size,
            fill="white", outline="", tags="btn_stop"
        )
        
        # Visualizer (Center)
        self._draw_visualizer_bars()

    def _draw_visualizer_bars(self):
        # Area between buttons
        start_x = 70
        end_x = config.WIDGET_WIDTH - 70
        width = end_x - start_x
        cy = config.WIDGET_HEIGHT // 2
        
        bar_width = width / len(self.audio_levels)
        max_height = 20
        
        for i, level in enumerate(self.audio_levels):
            x = start_x + i * bar_width + (bar_width/2)
            h = max(2, level * max_height) # Min height 2
            
            self.canvas.create_line(
                x, cy - h, x, cy + h,
                fill=config.COLOR_VISUALIZER, width=3, capstyle=tk.ROUND
            )

    def _draw_processing_ui(self):
        cy = config.WIDGET_HEIGHT // 2
        cx = config.WIDGET_WIDTH // 2
        
        # Dots Text
        self.canvas.create_text(
            cx - 20, cy,
            text=". . . . . . . .",
            fill="white",
            font=("Arial", 16, "bold"),
            anchor="center"
        )
        
        # Spinner (Right side of text)
        spinner_x = cx + 60
        radius = 10
        
        # Draw spinner segments
        for i in range(8):
            angle = self.processing_angle + (i * 45)
            rad = math.radians(angle)
            
            x1 = spinner_x + math.cos(rad) * (radius - 4)
            y1 = cy + math.sin(rad) * (radius - 4)
            x2 = spinner_x + math.cos(rad) * radius
            y2 = cy + math.sin(rad) * radius
            
            alpha = (i + 1) / 8.0
            # Simulate alpha with grey levels since Tkinter canvas lines don't support alpha directly easily
            # We'll just use white for active and dark grey for inactive
            color = "#ffffff" if i > 4 else "#555555"
            
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2, capstyle=tk.ROUND)

    def _on_click(self, event):
        # Check tags at click location
        item = self.canvas.find_closest(event.x, event.y)
        tags = self.canvas.gettags(item)
        
        if "btn_cancel" in tags:
            if self.on_cancel: self.on_cancel()
        elif "btn_stop" in tags:
            if self.on_stop: self.on_stop()

    def update_visualizer(self, audio_level):
        if self.state != "recording": return
        
        normalized_level = min(audio_level / 3000.0, 1.0) # Adjusted sensitivity
        self.audio_levels.append(normalized_level)
        self.audio_levels.pop(0)
        
        # Redraw only visualizer part if possible, but full redraw is safer for clean UI
        self._draw_ui()

    def show_processing(self):
        self.state = "processing"
        self._animate_processing()
        
    def _animate_processing(self):
        if self.state == "processing":
            self.processing_angle = (self.processing_angle + 20) % 360
            self._draw_ui()
            self.root.after(50, self._animate_processing)

    def show_recording(self):
        self.state = "recording"
        self._draw_ui()
        
    def get_current_mode(self):
        # Defaulting to 'default' since UI selector is removed for compact design
        return "default"

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
