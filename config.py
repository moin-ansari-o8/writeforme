"""
Enhanced Configuration with Multiple Writing Modes
Using Cohere API (command-r7b-12-2024 model) for AI text refinement
"""

# ==================== WRITING MODES ====================
# All modes use Cohere's command-r7b-12-2024 model

WRITING_MODES = {
    "vibe_coder": {
        "name": "Vibe Coder",
        "prompt": """Clean and refine this developer dictation. Output ONLY the refined text, nothing else.

Rules:
- Remove duplicate words ("hello hello" → "hello")
- Remove filler words (um, uh, like, you know, I guess, so, etc.)
- Fix grammar and awkward phrasing
- Convert spoken symbols: "underscore" → "_", "dot py" → ".py", "equals" → "="
- Fix mishearings: "wipe code" → "vibe code", "deep seek order" → "deepseek coder"
- Keep ALL key information (names, numbers, technical terms, context)
- Make it natural and professional
- DO NOT add information not in original
- DO NOT over-summarize or remove important context

Raw transcription:
{transcription}

Refined text:"""
    },
    
    "casual_chatter": {
        "name": "Casual Chatter",
        "prompt": """You are a casual writing assistant. Keep it relaxed and natural.

RULES:
1. Remove filler words (um, uh, like, you know) ONLY
2. DO NOT fix grammar heavily
3. Keep the casual, conversational tone
4. Keep slang and informal language
5. DO NOT change the meaning at all
6. Keep it exactly as the person speaks, just cleaner

Raw transcription:
{transcription}

Casual text:"""
    }
}

# Default mode (used if no mode is specified)
DEFAULT_MODE = "vibe_coder"

# ==================== POST-PROCESSING ====================
def post_process_coding_text(text):
    """Post-process text to fix speech recognition errors and convert symbols (backup layer)"""
    
    # LAYER 1: Fix common speech recognition mishearings (phonetic corrections)
    phonetic_fixes = {
        # Remove "write" at start (likely "alright")
        'write so': 'so',
        'write this': 'this',
        'write the': 'the',
        
        # Technical terms
        'wipe code': 'vibe code',
        'wife code': 'vibe code',
        'vibe coat': 'vibe code',
        'deep seek order': 'deepseek coder',
        'deep sick order': 'deepseek coder',
        'deepseek order': 'deepseek coder',
        
        # File names with numbers (speech recognition confusion)
        'main road 55': 'main.py',
        'main road': 'main.py',
        'main wrote': 'main.py',
        'config Jason': 'config.json',
        'config dot Jason': 'config.json',
        
        # Common programming terms
        'pie charm': 'PyCharm',
        'pie game': 'pygame',
        'pie pie': 'PyPI',
        'react jazz': 'react.js',
        'no js': 'node.js',
        'import order': 'import error',
        'syntax order': 'syntax error',
    }
    
    result = text
    for misheard, correct in phonetic_fixes.items():
        result = result.replace(misheard, correct)
    
    # LAYER 2: Symbol conversions (ONLY if code context detected)
    # Detect if this is code-related text
    code_indicators = [
        'underscore', 'dot py', 'dot js', 'dot json', 'function', 'variable',
        'import', 'class', 'def', 'const', 'let', 'var', 'equals equals',
        'open paren', 'close paren', 'open bracket', 'close bracket'
    ]
    
    is_code_context = any(indicator in result.lower() for indicator in code_indicators)
    
    if is_code_context:
        # Only apply symbol conversions in code context
        replacements = {
            ' underscore ': '_',
            'underscore ': '_',
            ' underscore': '_',
            ' dot ': '.',
            ' double equals ': ' == ',
            ' not equals ': ' != ',
            ' colon ': ': ',
            ' semicolon ': '; ',
            ' open paren ': '(',
            ' close paren ': ')',
            ' left paren ': '(',
            ' right paren ': ')',
            ' open bracket ': '[',
            ' close bracket ': ']',
            ' left bracket ': '[',
            ' right bracket ': ']',
            ' open brace ': '{',
            ' close brace ': '}',
            ' left brace ': '{',
            ' right brace ': '}',
        }
        
        for spoken, symbol in replacements.items():
            result = result.replace(spoken, symbol)
    
    # LAYER 3: File extensions (always apply)
    import re
    # Pattern: word + "dot" + extension
    result = re.sub(r'(\w+) dot (py|js|json|html|css|txt|md|env)', r'\1.\2', result)
    result = re.sub(r'dot (env|gitignore)', r'.\1', result)
    
    return result

# ==================== STORAGE SETTINGS ====================
# Maximum number of transcription entries to keep in history
# Automatically removes oldest entries when limit is exceeded
MAX_HISTORY_ENTRIES = 1000  # Default: 1000 (~500 KB storage)
# Reduce to 500 for less disk space, increase to 2000 for longer history

# Audio Recording Settings
AUDIO_SAMPLE_RATE = 16000  # Hz
AUDIO_CHUNK_SIZE = 1024    # samples per buffer
AUDIO_CHANNELS = 1         # mono
AUDIO_FORMAT = "int16"     # 16-bit audio

# GUI Widget Settings
WIDGET_WIDTH = 140  # Reduced from 180 for compact design
WIDGET_HEIGHT = 36  # Reduced from 40 for sleeker look
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
