"""
AI text refinement using Cohere API with multiple writing modes
"""
import cohere
import os
from dotenv import load_dotenv
import config

# Load environment variables
load_dotenv()


class AIRefiner:
    def __init__(self, mode="default"):
        """
        Initialize AI refiner with specific writing mode
        
        Args:
            mode: Writing mode from config.WRITING_MODES (default, email_professional, etc.)
        """
        self.set_mode(mode)
        
        # Initialize Cohere client with API key from .env
        api_key = os.getenv("CohereAPIKey")
        if not api_key:
            raise ValueError("CohereAPIKey not found in .env file")
        
        self.client = cohere.ClientV2(api_key=api_key)
        print(f"[AIRefiner] Initialized with Cohere API")
        
    def set_mode(self, mode):
        """Change the writing mode"""
        if mode not in config.WRITING_MODES:
            print(f"[AIRefiner] Warning: Mode '{mode}' not found, using default")
            mode = config.DEFAULT_MODE
        
        self.mode = mode
        self.mode_config = config.WRITING_MODES[mode]
        self.prompt_template = self.mode_config["prompt"]
        
        print(f"[AIRefiner] Mode set to: {self.mode_config['name']}")
        
    def refine_text(self, raw_text):
        """
        Refine raw transcription using Cohere API with current mode
        
        Args:
            raw_text: Raw transcribed text with potential errors and filler words
            
        Returns:
            str: Refined, polished text
        """
        if not raw_text or raw_text.strip() == "":
            print("[AIRefiner] No text to refine")
            return ""
        
        try:
            print(f"[AIRefiner] Refining text with Cohere ({self.mode_config['name']})...")
            
            # Create prompt with the raw transcription
            prompt = self.prompt_template.format(transcription=raw_text)
            
            # Call Cohere API
            response = self.client.chat(
                model="command-r7b-12-2024",  # Latest available model
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            refined_text = response.message.content[0].text.strip()
            return refined_text
            
        except Exception as e:
            print(f"[AIRefiner] Error refining text: {e}")
            print("[AIRefiner] Returning original text")
            return raw_text
    
    def test_connection(self):
        """Test if Cohere API is accessible"""
        try:
            # Simple test with a minimal request
            response = self.client.chat(
                model="command-r7b-12-2024",
                messages=[
                    {
                        "role": "user",
                        "content": "Test connection. Reply with 'OK'."
                    }
                ],
                max_tokens=10
            )
            
            if response.message.content:
                print(f"[AIRefiner] Cohere API connection successful")
                return True
            else:
                print(f"[AIRefiner] Warning: Unexpected response from Cohere")
                return False
                
        except Exception as e:
            print(f"[AIRefiner] Error connecting to Cohere API: {e}")
            return False
    
    def get_available_modes(self):
        """Get list of all available writing modes"""
        return {
            mode: config.WRITING_MODES[mode]["name"] 
            for mode in config.WRITING_MODES
        }
