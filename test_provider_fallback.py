# Quick Test Script for WriteForMe Providers
import sys
import os
sys.path.insert(0, r'W:\workplace-1\writeforme')
os.chdir(r'W:\workplace-1\writeforme')

from ai_provider_manager import AIProviderManager

print("Testing Gemini with stable model...")
manager = AIProviderManager()

# Simulate selecting Gemini (option 2)
import unittest.mock as mock
with mock.patch('builtins.input', side_effect=['2', 'n']):
    result = manager.select_provider()
    print(f"\nProvider selection result: {result}")
    if manager.current_provider:
        print(f"Current provider: {manager.get_provider_name()}")
    else:
        print("No provider initialized")
