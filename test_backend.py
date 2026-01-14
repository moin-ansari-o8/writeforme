"""
Quick test to start backend server directly
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("Testing backend server startup...")
print(f"Project root: {project_root}")
print(f"Python path: {sys.path[:3]}")

try:
    print("\n1. Importing FastAPI...")
    from fastapi import FastAPI
    print("   ✓ FastAPI imported")
    
    print("\n2. Importing backend modules...")
    from backend.api import audio_routes
    print("   ✓ audio_routes imported")
    
    from backend.api import ai_routes
    print("   ✓ ai_routes imported")
    
    from backend.api import settings_routes
    print("   ✓ settings_routes imported")
    
    from backend.api import history_routes
    print("   ✓ history_routes imported")
    
    print("\n3. Starting server...")
    from backend.server import app, start_server
    print("   ✓ Server module loaded")
    
    print("\n✓ All imports successful!")
    print("\nStarting server on http://127.0.0.1:8765...")
    start_server()
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
