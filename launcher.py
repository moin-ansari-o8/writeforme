"""
WriteForMe Background Launcher
Runs WriteForMe as a system tray application with auto-start support
"""
import sys
import os
import threading
import time
from pathlib import Path
import pystray
from PIL import Image
import winreg
import ctypes

# High DPI awareness for Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

# Get base directory
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
ICON_PATH = ASSETS_DIR / "wfm_logo.ico"
LOCK_FILE = Path(os.environ.get("LOCALAPPDATA", os.path.expanduser("~"))) / "WriteForMe" / "writeforme.lock"

# Application name for Windows registry
APP_NAME = "WriteForMe"
APP_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


class WriteForMeLauncher:
    """Background launcher with system tray"""
    
    def __init__(self):
        self.app = None
        self.app_thread = None
        self.running = False
        self.icon = None
        
        # Ensure lock directory exists
        LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
        
    def check_single_instance(self):
        """Ensure only one instance is running"""
        if LOCK_FILE.exists():
            try:
                with open(LOCK_FILE, 'r') as f:
                    pid = int(f.read().strip())
                
                # Check if process is still running
                import psutil
                if psutil.pid_exists(pid):
                    print(f"WriteForMe is already running (PID: {pid})")
                    return False
                else:
                    print(f"Removing stale lock file (PID {pid} not running)")
                    LOCK_FILE.unlink()
            except (ValueError, FileNotFoundError):
                LOCK_FILE.unlink()
        
        # Create lock file with current PID
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
        
        return True
    
    def cleanup_lock(self):
        """Remove lock file on exit"""
        try:
            if LOCK_FILE.exists():
                LOCK_FILE.unlink()
        except Exception:
            pass
    
    def is_autostart_enabled(self):
        """Check if app is in Windows startup"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, APP_KEY, 0, winreg.KEY_READ)
            try:
                value, _ = winreg.QueryValueEx(key, APP_NAME)
                winreg.CloseKey(key)
                return True
            except WindowsError:
                winreg.CloseKey(key)
                return False
        except WindowsError:
            return False
    
    def enable_autostart(self):
        """Add app to Windows startup"""
        try:
            exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, APP_KEY, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Failed to enable autostart: {e}")
            return False
    
    def disable_autostart(self):
        """Remove app from Windows startup"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, APP_KEY, 0, winreg.KEY_WRITE)
            winreg.DeleteValue(key, APP_NAME)
            winreg.CloseKey(key)
            return True
        except Exception as e:
            print(f"Failed to disable autostart: {e}")
            return False
    
    def start_app(self):
        """Start WriteForMe in background thread"""
        if self.running:
            return
        
        def run_app():
            from main import WisprFlowLocal
            self.app = WisprFlowLocal(silent_mode=True)
            self.running = True
            self.app.run()
        
        self.app_thread = threading.Thread(target=run_app, daemon=True)
        self.app_thread.start()
        
        # Update icon menu
        if self.icon:
            self.icon.menu = self.create_menu()
    
    def stop_app(self):
        """Stop WriteForMe"""
        if not self.running:
            return
        
        if self.app:
            self.app.cleanup()
        self.running = False
        
        # Update icon menu
        if self.icon:
            self.icon.menu = self.create_menu()
    
    def toggle_app(self, icon, item):
        """Toggle app start/stop"""
        if self.running:
            self.stop_app()
        else:
            self.start_app()
    
    def toggle_autostart(self, icon, item):
        """Toggle Windows startup"""
        if self.is_autostart_enabled():
            self.disable_autostart()
        else:
            self.enable_autostart()
        
        # Update menu
        self.icon.menu = self.create_menu()
    
    def quit_app(self, icon, item):
        """Quit application"""
        self.stop_app()
        self.cleanup_lock()
        icon.stop()
    
    def create_menu(self):
        """Create system tray menu"""
        return pystray.Menu(
            pystray.MenuItem(
                "Stop Listening" if self.running else "Start Listening",
                self.toggle_app,
                default=True
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Auto-start with Windows",
                self.toggle_autostart,
                checked=lambda item: self.is_autostart_enabled()
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit WriteForMe", self.quit_app)
        )
    
    def load_icon(self):
        """Load tray icon"""
        try:
            if ICON_PATH.exists():
                return Image.open(ICON_PATH)
            else:
                # Create simple fallback icon if file not found
                return Image.new('RGB', (64, 64), color='blue')
        except Exception as e:
            print(f"Failed to load icon: {e}")
            return Image.new('RGB', (64, 64), color='blue')
    
    def run(self):
        """Main entry point"""
        # Check single instance
        if not self.check_single_instance():
            sys.exit(1)
        
        # Load icon
        icon_image = self.load_icon()
        
        # Create system tray icon
        self.icon = pystray.Icon(
            "WriteForMe",
            icon_image,
            "WriteForMe - Speech to Text",
            menu=self.create_menu()
        )
        
        # Auto-start the app
        self.start_app()
        
        # Run tray icon (blocks until quit)
        self.icon.run()


def main():
    """Entry point"""
    launcher = WriteForMeLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
