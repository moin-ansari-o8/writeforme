"""
Enhanced Configuration with Multiple Writing Modes
Using Cohere API (command-r7b-12-2024 model) for AI text refinement
"""

# ==================== WRITING MODES ====================
# All modes use Cohere's command-r7b-12-2024 model

WRITING_MODES = {
    "default": {
        "name": "Smart Dictation",
        "prompt": """You are an intelligent writing assistant. Transform the spoken transcription into polished text.

Instructions:
1. Remove filler words (um, uh, like, you know, etc.)
2. Fix grammar and punctuation
3. Keep the speaker's original intent and meaning
4. Make it sound natural and clear

Raw transcription:
{transcription}

Refined text (output ONLY the refined text):"""
    },
    
    "email_professional": {
        "name": "Professional Email",
        "prompt": """You are a professional business writing assistant. Transform the spoken words into a polished, professional email.

Instructions:
1. Remove all filler words and informal language
2. Use professional, courteous tone
3. Add proper email structure if needed
4. Ensure clarity and conciseness
5. Maintain professional business etiquette

Raw transcription:
{transcription}

Professional email text:"""
    },
    
    "email_casual": {
        "name": "Casual Email",
        "prompt": """You are a friendly writing assistant. Transform the spoken words into a casual, friendly email.

Instructions:
1. Remove filler words but keep casual tone
2. Use friendly, conversational language
3. Keep it warm and approachable
4. Fix grammar while maintaining friendly voice

Raw transcription:
{transcription}

Casual email text:"""
    },
    
    "prompt_writer": {
        "name": "AI Prompt (Developer)",
        "prompt": """You are an AI prompt engineering expert. Transform the spoken instructions into a clear, well-structured prompt for AI agents or developers.

Instructions:
1. Remove filler words and organize thoughts logically
2. Use clear, technical language
3. Structure the prompt with sections if needed
4. Include relevant context and constraints
5. Make it actionable and specific for AI/developers

Raw transcription:
{transcription}

Well-structured AI prompt:"""
    },
    
    "creative_writing": {
        "name": "Creative Writing",
        "prompt": """You are a creative writing assistant. Transform the spoken ideas into engaging, creative prose.

Instructions:
1. Remove filler words while preserving creativity
2. Enhance descriptive language
3. Improve narrative flow
4. Keep the original creative vision
5. Add literary polish

Raw transcription:
{transcription}

Creative text:"""
    },
    
    "grammar_only": {
        "name": "Grammar Correction",
        "prompt": """Fix ONLY grammar, spelling, and punctuation. Do not change the meaning or add any content.

Raw text:
{transcription}

Corrected text:"""
    },
    
    "technical_writing": {
        "name": "Technical Documentation",
        "prompt": """You are a technical writing assistant. Transform spoken technical content into clear documentation.

Instructions:
1. Remove filler words
2. Use precise technical language
3. Organize into clear sections if needed
4. Ensure accuracy and clarity
5. Maintain professional technical tone

Raw transcription:
{transcription}

Technical documentation:"""
    }
}

# Default mode (used if no mode is specified)
DEFAULT_MODE = "default"

# Audio Recording Settings
AUDIO_SAMPLE_RATE = 16000  # Hz
AUDIO_CHUNK_SIZE = 1024    # samples per buffer
AUDIO_CHANNELS = 1         # mono
AUDIO_FORMAT = "int16"     # 16-bit audio

# GUI Widget Settings
WIDGET_WIDTH = 180  # Increased width for menu button
WIDGET_HEIGHT = 40
WIDGET_POSITION = "bottom-center"
WIDGET_ALPHA = 1.0  # Fully opaque for the pill, transparency handled via colorkey

# Colors (RGB)
COLOR_BACKGROUND = "#121212"  # Deep dark background
COLOR_TRANSPARENT = "#000001"  # Key color for transparency
COLOR_VISUALIZER = "#ffffff"   # White waveform
COLOR_BUTTON_CANCEL = "#404040" # Lighter grey cancel button
COLOR_BUTTON_STOP = "#ff4b4b"   # Vibrant red stop button
COLOR_TEXT = "#ffffff"
COLOR_MODE_SELECTOR = "#1e1e1e"
COLOR_MODE_ACTIVE = "#333333"
