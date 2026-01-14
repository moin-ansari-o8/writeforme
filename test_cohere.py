"""
Test Cohere API Connection
"""
import cohere
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("CohereAPIKey")
print(f"API Key found: {'Yes' if api_key else 'No'}")

if api_key:
    print(f"API Key (first 10 chars): {api_key[:10]}...")
    
    try:
        client = cohere.ClientV2(api_key=api_key)
        
        print("\nTesting API connection...")
        response = client.chat(
            model="command-r7b-12-2024",  # Latest model Dec 2024
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Connection successful!' and nothing else."
                }
            ],
            max_tokens=20
        )
        
        result = response.message.content[0].text
        print(f"\n✓ Response: {result}")
        print("✓ Cohere API is working!")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
else:
    print("✗ API key not found in .env file")
