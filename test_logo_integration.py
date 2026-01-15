"""
Logo Integration Test - Verify all logo placements

This script checks that the logo files exist and are properly configured
in the dashboard_v2.py file.
"""

import os
from pathlib import Path

def check_logo_files():
    """Check if logo files exist"""
    print("🔍 Checking logo files...")
    
    logo_path = Path("assets/wfm main logo1.png")
    
    if logo_path.exists():
        print(f"  ✅ Logo found: {logo_path}")
        print(f"     Size: {logo_path.stat().st_size / 1024:.2f} KB")
    else:
        print(f"  ❌ Logo NOT found: {logo_path}")
        return False
    
    return True

def check_dashboard_code():
    """Check if dashboard_v2.py has logo integration"""
    print("\n🔍 Checking dashboard code...")
    
    dashboard_path = Path("frontend/dashboard_v2.py")
    
    if not dashboard_path.exists():
        print("  ❌ dashboard_v2.py not found")
        return False
    
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = {
        "Sidebar logo": 'QPixmap("assets/wfm main logo1.png")' in content,
        "Window icon": 'QIcon("assets/wfm main logo1.png")' in content,
        "System tray": 'class SystemTrayIcon(QSystemTrayIcon)' in content,
        "Tray setup": 'def setup_tray_icon(self)' in content,
    }
    
    for check_name, passed in checks.items():
        status = "✅" if passed else "❌"
        print(f"  {status} {check_name}: {'Found' if passed else 'NOT found'}")
    
    return all(checks.values())

def main():
    print("=" * 50)
    print("WriteForMe - Logo Integration Verification")
    print("=" * 50)
    print()
    
    logo_ok = check_logo_files()
    code_ok = check_dashboard_code()
    
    print("\n" + "=" * 50)
    if logo_ok and code_ok:
        print("✅ All logo integrations are configured correctly!")
        print("\nLogo will appear in:")
        print("  1. Sidebar (above 'WriteForMe' text)")
        print("  2. Windows Taskbar")
        print("  3. System Tray (notification area)")
    else:
        print("❌ Some issues found. Please check the errors above.")
    print("=" * 50)

if __name__ == "__main__":
    main()
