"""
Test script to verify all dependencies and connections
"""
import sys

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    try:
        import pyaudio
        print("✓ pyaudio")
    except ImportError as e:
        print(f"✗ pyaudio: {e}")
        return False
    
    try:
        import speech_recognition as sr
        print("✓ speech_recognition")
    except ImportError as e:
        print(f"✗ speech_recognition: {e}")
        return False
    
    try:
        import numpy
        print("✓ numpy")
    except ImportError as e:
        print(f"✗ numpy: {e}")
        return False
    
    try:
        import ollama
        print("✓ ollama")
    except ImportError as e:
        print(f"✗ ollama: {e}")
        return False
    
    try:
        import pyperclip
        print("✓ pyperclip")
    except ImportError as e:
        print(f"✗ pyperclip: {e}")
        return False
    
    try:
        import pyautogui
        print("✓ pyautogui")
    except ImportError as e:
        print(f"✗ pyautogui: {e}")
        return False
    
    try:
        import tkinter
        print("✓ tkinter")
    except ImportError as e:
        print(f"✗ tkinter: {e}")
        return False
    
    return True

def test_ollama():
    """Test Ollama connection and available models"""
    print("\nTesting Ollama connection...")
    try:
        import ollama
        response = ollama.list()
        
        # Handle different response formats
        if isinstance(response, dict):
            models = response.get('models', [])
        else:
            models = response
        
        model_list = []
        for m in models:
            if isinstance(m, dict):
                model_list.append(m.get('name', m.get('model', 'unknown')))
            else:
                model_list.append(str(m))
        
        print(f"✓ Ollama is running")
        print(f"  Available models: {model_list}")
        
        if 'gemma3:latest' in model_list or any('gemma3' in m for m in model_list):
            print("✓ gemma3 is available")
            return True
        else:
            print("⚠ gemma3:latest not found in available models")
            print("  Run: ollama pull gemma3")
            return False
    except Exception as e:
        print(f"✗ Ollama connection failed: {e}")
        print("  Make sure Ollama is running: ollama serve")
        return False

def test_microphone():
    """Test if microphone is available"""
    print("\nTesting microphone...")
    try:
        import pyaudio
        audio = pyaudio.PyAudio()
        
        # Try to find default input device
        default_input = audio.get_default_input_device_info()
        print(f"✓ Default microphone: {default_input['name']}")
        
        audio.terminate()
        return True
    except Exception as e:
        print(f"✗ Microphone test failed: {e}")
        return False

def main():
    print("=" * 60)
    print("Wispr Flow Local - System Test")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test Ollama
    if not test_ollama():
        all_passed = False
    
    # Test microphone
    if not test_microphone():
        all_passed = False
    
    print()
    print("=" * 60)
    if all_passed:
        print("✓ All tests passed! You're ready to run the application.")
        print("  Run: python main.py")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        print("  Refer to README.md for installation instructions.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
