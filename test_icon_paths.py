"""
Icon Load Test - Verify all icons load correctly in frozen EXE
Run from: W:\workplace-1\writeforme\dist\WriteForMe.exe
"""
import sys
import os
from pathlib import Path

def resource_path(relative_path):
    """Get absolute path to resource - works for dev and PyInstaller frozen EXE"""
    if hasattr(sys, '_MEIPASS'):
        # Running as frozen EXE
        base_path = sys._MEIPASS
        print(f"✅ Running as FROZEN EXE, _MEIPASS: {base_path}")
        return os.path.join(base_path, relative_path)
    # Running as script
    base_path = os.path.abspath(".")
    print(f"⚠️ Running as SCRIPT, base: {base_path}")
    return os.path.join(base_path, relative_path)


def test_icon_paths():
    """Test icon path resolution"""
    print("\n" + "="*70)
    print("ICON PATH RESOLUTION TEST")
    print("="*70)
    
    # Test ICO path
    ico_path = resource_path(os.path.join("assets", "wfm_logo.ico"))
    print(f"\n1. ICO Path: {ico_path}")
    print(f"   Exists: {'✅ YES' if os.path.exists(ico_path) else '❌ NO'}")
    if os.path.exists(ico_path):
        size = os.path.getsize(ico_path)
        print(f"   Size: {size:,} bytes")
    
    # Test PNG path
    png_path = resource_path(os.path.join("assets", "wfm main logo1.png"))
    print(f"\n2. PNG Path: {png_path}")
    print(f"   Exists: {'✅ YES' if os.path.exists(png_path) else '❌ NO'}")
    if os.path.exists(png_path):
        size = os.path.getsize(png_path)
        print(f"   Size: {size:,} bytes")
    
    # List all files in _MEIPASS/assets if frozen
    if hasattr(sys, '_MEIPASS'):
        assets_dir = os.path.join(sys._MEIPASS, "assets")
        print(f"\n3. Contents of {assets_dir}:")
        if os.path.exists(assets_dir):
            for item in os.listdir(assets_dir):
                item_path = os.path.join(assets_dir, item)
                is_dir = os.path.isdir(item_path)
                print(f"   {'📁' if is_dir else '📄'} {item}")
        else:
            print("   ❌ Assets directory not found!")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    test_icon_paths()
    input("\nPress Enter to exit...")
