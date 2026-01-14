"""
AI Provider Manager - Unified interface for multiple AI services
Supports: Cohere, Gemini, Groq, and Ollama
"""
import os
from dotenv import load_dotenv
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Load environment variables
load_dotenv()


class AIProvider:
    """Base class for AI providers"""
    def __init__(self, name, is_online=True):
        self.name = name
        self.is_online = is_online
        self.client = None
        
    def test_connection(self):
        """Test if provider is available"""
        raise NotImplementedError
    
    def refine_text(self, raw_text, prompt_template):
        """Refine text using the provider"""
        raise NotImplementedError


class CohereProvider(AIProvider):
    def __init__(self):
        super().__init__("Cohere", is_online=True)
        api_key = os.getenv("CohereAPIKey")
        if not api_key:
            raise ValueError("CohereAPIKey not found in .env")
        
        import cohere
        self.client = cohere.ClientV2(api_key=api_key)
        self.model = "command-r7b-12-2024"
    
    def test_connection(self):
        try:
            response = self.client.chat(
                model=self.model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            print(f"{Fore.RED}Cohere error: {e}")
            return False
    
    def refine_text(self, raw_text, prompt_template):
        prompt = prompt_template.format(transcription=raw_text)
        response = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,  # Lower for more predictable, accurate output
            max_tokens=500
        )
        return response.message.content[0].text.strip()


class GeminiProvider(AIProvider):
    def __init__(self):
        super().__init__("Gemini", is_online=True)
        api_key = os.getenv("GeminiAPIKey")
        if not api_key:
            raise ValueError("GeminiAPIKey not found in .env")
        
        from google import genai
        from google.genai import types
        
        self.client = genai.Client(api_key=api_key)
        # Use stable model instead of experimental
        self.model = 'gemini-1.5-flash'
    
    def test_connection(self):
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents="Test"
            )
            return True
        except Exception as e:
            print(f"{Fore.RED}Gemini error: {e}")
            return False
    
    def refine_text(self, raw_text, prompt_template):
        prompt = prompt_template.format(transcription=raw_text)
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        return response.text.strip()


class GroqProvider(AIProvider):
    def __init__(self):
        super().__init__("Groq", is_online=True)
        api_key = os.getenv("GroqAPIKey")
        if not api_key:
            raise ValueError("GroqAPIKey not found in .env")
        
        from groq import Groq
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
    
    def test_connection(self):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            print(f"{Fore.RED}Groq error: {e}")
            return False
    
    def refine_text(self, raw_text, prompt_template):
        prompt = prompt_template.format(transcription=raw_text)
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # Lower for more predictable output
                max_tokens=500,
                timeout=30  # 30 second timeout
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"{Fore.YELLOW}[Groq] Timeout/Error, using raw text: {e}{Style.RESET_ALL}")
            # Return raw text if Groq fails
            return raw_text


class OllamaProvider(AIProvider):
    def __init__(self):
        super().__init__("Ollama (Local)", is_online=False)
        import ollama
        import subprocess
        import time
        
        self.client = ollama.Client(host="http://localhost:11434")
        self.model = None  # Will be selected by user
        
        # Auto-start Ollama if not running
        if not self._is_ollama_running():
            print(f"{Fore.YELLOW}[Ollama] Service not running, starting...{Style.RESET_ALL}")
            self._start_ollama_service()
            time.sleep(3)  # Wait for service to start
        
        # Let user select model
        self._select_model()
    
    def _select_model(self):
        """Let user select which Ollama model to use"""
        try:
            # Get list of installed models
            models_response = self.client.list()
            models = models_response.get('models', [])
            
            if not models:
                print(f"{Fore.RED}[Ollama] No models found. Please install a model first.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}Example: ollama pull deepseek-coder:6.7b{Style.RESET_ALL}")
                self.model = "deepseek-coder:6.7b"  # Fallback
                return
            
            # Display available models
            print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
            print(f"{Fore.CYAN}{Style.BRIGHT}{'📦  Select Ollama Model':^70}")
            print(f"{Fore.CYAN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}\n")
            
            for i, model in enumerate(models, 1):
                # Try different possible keys for model name
                model_name = model.get('model') or model.get('name') or 'Unknown'
                size = model.get('size', 0)
                size_gb = size / (1024**3)  # Convert to GB
                
                print(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {Fore.GREEN}{model_name}{Style.RESET_ALL} ({size_gb:.1f} GB)")
            
            print(f"\n{Fore.CYAN}Enter model number (default: 1):{Style.RESET_ALL} ", end="")
            choice = input().strip() or "1"
            
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(models):
                    self.model = models[idx].get('model') or models[idx].get('name')
                    print(f"{Fore.GREEN}✓ Selected: {self.model}{Style.RESET_ALL}\n")
                    # Update provider name
                    self.name = f"Ollama ({self.model})"
                else:
                    print(f"{Fore.RED}Invalid choice, using first model{Style.RESET_ALL}")
                    self.model = models[0].get('model') or models[0].get('name')
            except ValueError:
                print(f"{Fore.RED}Invalid input, using first model{Style.RESET_ALL}")
                self.model = models[0].get('model') or models[0].get('name')
                
        except Exception as e:
            print(f"{Fore.RED}[Ollama] Error selecting model: {e}{Style.RESET_ALL}")
            self.model = "deepseek-coder:6.7b"  # Fallback
    
    def _is_ollama_running(self):
        """Check if Ollama service is running"""
        try:
            self.client.list()
            return True
        except:
            return False
    
    def _start_ollama_service(self):
        """Start Ollama service in background"""
        import subprocess
        import sys
        
        try:
            if sys.platform == "win32":
                # Windows: Start Ollama in background
                subprocess.Popen(
                    ["ollama", "serve"],
                    creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                # Linux/Mac
                subprocess.Popen(
                    ["ollama", "serve"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            print(f"{Fore.GREEN}[Ollama] Service started successfully{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[Ollama] Failed to start service: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[Ollama] Please start Ollama manually or ensure it's installed{Style.RESET_ALL}")
    
    def test_connection(self):
        try:
            self.client.list()
            return True
        except Exception as e:
            print(f"{Fore.RED}Ollama error: {e}")
            return False
    
    def refine_text(self, raw_text, prompt_template):
        prompt = prompt_template.format(transcription=raw_text)
        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            options={
                'temperature': 0.3,  # Lower to reduce creativity
                'num_predict': 500
            }
        )
        return response['response'].strip()


class AIProviderManager:
    """Manages multiple AI providers with selection UI"""
    
    PROVIDERS = {
        '1': ('cohere', CohereProvider, '🌐 Cohere (Online - Fast)'),
        '2': ('gemini', GeminiProvider, '🌐 Gemini (Online - Google)'),
        '3': ('groq', GroqProvider, '🌐 Groq (Online - Ultra Fast)'),
        '4': ('ollama', OllamaProvider, '💻 Ollama (Offline - Local)')
    }
    
    def __init__(self):
        self.current_provider = None
        self.provider_name = None
    
    def print_banner(self):
        """Print beautiful banner"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'🎤  WriteForMe - AI-Powered Dictation Assistant':^70}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*70}{Style.RESET_ALL}\n")
    
    def select_provider(self):
        """Interactive provider selection"""
        self.print_banner()
        
        print(f"{Fore.YELLOW}{Style.BRIGHT}📡 Select AI Provider:{Style.RESET_ALL}\n")
        
        # Show available providers
        for key, (name, provider_class, display) in self.PROVIDERS.items():
            # Check if API key exists for online providers
            status = self._check_provider_availability(name)
            color = Fore.GREEN if status else Fore.RED
            status_text = "✓ Available" if status else "✗ No API Key"
            print(f"{Fore.CYAN}  [{key}] {display:<35} {color}{status_text}{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}Enter choice (1-4):{Style.RESET_ALL} ", end="")
        
        choice = input().strip()
        
        if choice not in self.PROVIDERS:
            print(f"{Fore.RED}Invalid choice! Defaulting to Cohere...{Style.RESET_ALL}")
            choice = '1'
        
        # Initialize selected provider
        provider_name, provider_class, display = self.PROVIDERS[choice]
        self.provider_name = provider_name
        
        print(f"\n{Fore.GREEN}⏳ Initializing {display}...{Style.RESET_ALL}")
        
        try:
            self.current_provider = provider_class()
            print(f"{Fore.GREEN}✓ {self.current_provider.name} initialized!{Style.RESET_ALL}")
            
            # Test connection
            print(f"{Fore.YELLOW}⏳ Testing connection...{Style.RESET_ALL}")
            if self.current_provider.test_connection():
                print(f"{Fore.GREEN}✓ Connection successful!{Style.RESET_ALL}\n")
                return True
            else:
                print(f"{Fore.RED}✗ Connection failed!{Style.RESET_ALL}\n")
                # Ask user to try another provider instead of crashing
                print(f"{Fore.YELLOW}Would you like to try another provider? (y/n):{Style.RESET_ALL} ", end="")
                retry = input().strip().lower()
                if retry == 'y':
                    return self.select_provider()
                else:
                    print(f"{Fore.YELLOW}Attempting fallback to Ollama...{Style.RESET_ALL}")
                    try:
                        self.current_provider = OllamaProvider()
                        self.provider_name = 'ollama'
                        if self.current_provider.test_connection():
                            print(f"{Fore.GREEN}✓ Ollama connected!{Style.RESET_ALL}\n")
                            return True
                        else:
                            print(f"{Fore.RED}✗ Ollama also failed{Style.RESET_ALL}")
                            return False
                    except Exception as e2:
                        print(f"{Fore.RED}✗ Ollama error: {e2}{Style.RESET_ALL}")
                        return False
                
        except Exception as e:
            print(f"{Fore.RED}✗ Error: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Would you like to try another provider? (y/n):{Style.RESET_ALL} ", end="")
            retry = input().strip().lower()
            if retry == 'y':
                return self.select_provider()
            else:
                print(f"{Fore.YELLOW}Attempting fallback to Ollama...{Style.RESET_ALL}")
                try:
                    self.current_provider = OllamaProvider()
                    self.provider_name = 'ollama'
                    if self.current_provider.test_connection():
                        print(f"{Fore.GREEN}✓ Ollama connected!{Style.RESET_ALL}\n")
                        return True
                    else:
                        return False
                except Exception as e2:
                    print(f"{Fore.RED}✗ Ollama error: {e2}{Style.RESET_ALL}")
                    return False
    
    def _check_provider_availability(self, provider_name):
        """Check if provider API key exists"""
        if provider_name == 'ollama':
            return True  # Ollama doesn't need API key
        
        key_map = {
            'cohere': 'CohereAPIKey',
            'gemini': 'GeminiAPIKey',
            'groq': 'GroqAPIKey'
        }
        
        key = os.getenv(key_map.get(provider_name, ''))
        return bool(key and key.strip())
    
    def refine_text(self, raw_text, prompt_template):
        """Refine text using current provider"""
        if not self.current_provider:
            return raw_text
        
        try:
            return self.current_provider.refine_text(raw_text, prompt_template)
        except Exception as e:
            print(f"{Fore.RED}[AI] Error: {e}{Style.RESET_ALL}")
            return raw_text
    
    def get_provider_name(self):
        """Get current provider name"""
        return self.current_provider.name if self.current_provider else "None"
