"""
AI text refinement using local Ollama LLaMA model with multiple writing modes
"""
import ollama
import config


class AIRefiner:
    def __init__(self, mode="default"):
        """
        Initialize AI refiner with specific writing mode
        
        Args:
            mode: Writing mode from config.WRITING_MODES (default, email_professional, etc.)
        """
        self.set_mode(mode)
        self.client = None
        
    def set_mode(self, mode):
        """Change the writing mode"""
        if mode not in config.WRITING_MODES:
            print(f"[AIRefiner] Warning: Mode '{mode}' not found, using default")
            mode = config.DEFAULT_MODE
        
        self.mode = mode
        self.mode_config = config.WRITING_MODES[mode]
        self.model = self.mode_config["model"]
        self.prompt_template = self.mode_config["prompt"]
        
        print(f"[AIRefiner] Mode set to: {self.mode_config['name']} (using {self.model})")
        
    def refine_text(self, raw_text):
        """
        Refine raw transcription using local LLaMA model with current mode
        
        Args:
            raw_text: Raw transcribed text with potential errors and filler words
            
        Returns:
            str: Refined, polished text
        """
        if not raw_text or raw_text.strip() == "":
            print("[AIRefiner] No text to refine")
            return ""
        
        try:
            print(f"[AIRefiner] Refining text with {self.model} ({self.mode_config['name']})...")
            print(f"[AIRefiner] Input: {raw_text}")
            
            # Create prompt with the raw transcription
            prompt = self.prompt_template.format(transcription=raw_text)
            
            # Call Ollama API
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    'temperature': 0.3,  # Lower temperature for more consistent output
                    'top_p': 0.9,
                    'max_tokens': 500
                }
            )
            
            refined_text = response['response'].strip()
            print(f"[AIRefiner] Output: {refined_text}")
            
            return refined_text
            
        except Exception as e:
            print(f"[AIRefiner] Error refining text: {e}")
            print("[AIRefiner] Returning original text")
            # Return original text if AI refinement fails
            return raw_text
    
    def test_connection(self):
        """Test if Ollama is running and model is available"""
        try:
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
            
            if self.model in model_list or any(self.model.split(':')[0] in m for m in model_list):
                print(f"[AIRefiner] Model {self.model} is available")
                return True
            else:
                print(f"[AIRefiner] Warning: Model {self.model} not found")
                print(f"[AIRefiner] Available models: {model_list[:5]}...")  # Show first 5
                return False
                
        except Exception as e:
            print(f"[AIRefiner] Error connecting to Ollama: {e}")
            print("[AIRefiner] Make sure Ollama is running (ollama serve)")
            return False
    
    def get_available_modes(self):
        """Get list of all available writing modes"""
        return {
            mode: config.WRITING_MODES[mode]["name"] 
            for mode in config.WRITING_MODES
        }
