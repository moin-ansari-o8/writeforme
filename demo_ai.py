"""
Quick demo script to test basic AI refinement without GUI
"""
from ai_refiner import AIRefiner

def main():
    print("=" * 60)
    print("AI Refinement Demo")
    print("=" * 60)
    print()
    
    refiner = AIRefiner()
    
    # Test connection
    if not refiner.test_connection():
        print("\nPlease start Ollama: ollama serve")
        return
    
    print("\nTesting AI text refinement...\n")
    
    # Test cases
    test_inputs = [
        "um so I was thinking uh we should like maybe test this thing",
        "hey can you um like send me the uh report by tomorrow please",
        "I uh really appreciate your help with this project you know"
    ]
    
    for i, raw_text in enumerate(test_inputs, 1):
        print(f"Test {i}:")
        print(f"  Input:  {raw_text}")
        refined = refiner.refine_text(raw_text)
        print(f"  Output: {refined}")
        print()
    
    print("=" * 60)
    print("Demo complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
