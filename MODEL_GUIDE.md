# Model Selection Guide

## Your Local Models - Analyzed & Optimized

Based on comprehensive research, here's the optimal model selection for each writing task in Wispr Flow Local.

## Available Models

You have **11 models** installed locally:

| Model | Size | Best For |
|-------|------|----------|
| **mistral:7b-instruct** | 7B | General text refinement, professional writing |
| **gemma3:latest** | ~3B | Creative writing, casual communication |
| **llama3.2:latest** | 2B | Grammar correction, summarization |
| **llama3.2:1b** | 1B | Fast, lightweight tasks |
| **deepseek-r1:8b** | 8B | Complex reasoning, technical writing, AI prompts |
| **deepseek-coder:6.7b** | 6.7B | Code generation, technical documentation |
| **phi3:mini** | 3.8B | Instruction following, general tasks |
| **phi3:3.8b-mini-4k-instruct-q6_K** | 3.8B | Text refinement (high quality quantization) |
| **codegemma:7b-instruct** | 7B | Code-related writing |
| **codellama:7b-instruct** | 7B | Code documentation |

## Writing Mode Configurations

### 1. Smart Dictation (Default)
**Model**: `mistral:7b-instruct`  
**Why**: Mistral 7B  is the most balanced model for general text refinement. It:
- Outperforms Llama2 13B in many tasks
- Excellent at removing filler words
- Strong instruction-following
- Less prone to hallucination

### 2. Professional Email
**Model**: `mistral:7b-instruct`  
**Why**: Professional tone requires:
- Consistent formal language
- Clear structure
- Business etiquette awareness  
Mistral excels in structured, professional output.

### 3. Casual Email
**Model**: `gemma3:latest`  
**Why**: Gemma3 is described as "super bubbly and upbeat":
- Natural, conversational tone
- Friendly personality
- Good at maintaining warmth while fixing grammar

### 4. AI Prompt (Developer)
**Model**: `deepseek-r1:8b`  
**Why**: DeepSeek R1 is a reasoning powerhouse:
- 90.8% on MMLU (advanced reasoning)
- Excellent at logical structuring
- Chain-of-thought reasoning
- Perfect for technical, step-by-step instructions

### 5. Creative Writing
**Model**: `gemma3:latest`  
**Why**: Gemma3 outperforms much larger models in creative writing:
- Beats Claude 3.7 Sonnet in creative tests
- Engaging story generation
- Good writing style and personality
- Excellent multilingual creative support

### 6. Grammar Correction Only
**Model**: `llama3.2:latest`  
**Why**: Llama 3.2 is described as "no-nonsense, just the facts":
- Concise, straightforward output
- Excellent at precision tasks
- No unnecessary embellishment
- High accuracy in NLP benchmarks

### 7. Technical Documentation
**Model**: `deepseek-r1:8b`  
**Why**: Technical docs need logical structure:
- Strong at structured creativity  
- Excellent for technical/legal documents
- 49.2% on SWE-bench Verified (coding tasks)
- Optimized for step-by-step explanations

## Research-Backed Insights

### Performance Benchmarks

**Mistral 7B Instruct:**
- Often outperforms Llama2 13B and competes with Llama1 34B
- Strong in code generation, math reasoning, summarization
- Grouped Query Attention (GQA) for faster inference

**Gemma3:**
- #1 on Creative Short Story Writing Benchmark
- Supports 140+ languages
- 128K token context window
- Greatly improved creative writing vs previous versions

**DeepSeek R1:**
- 97.3% on MATH-500 (vs OpenAI's o1: similar)
- 96.3% on Codeforces
- Generates chain-of-thought explanations
- Approaches OpenAI o3 performance

**Llama 3.2:**
- Surpasses GPT-4 in efficiency
- Optimized for summarization and rewriting
- Strong natural language understanding
- 63.4% on MMLU (vs Mistral 60.1%)

**Phi-3 Mini:**
- 3.8B parameters, Microsoft's efficient model
- Excellent instruction-following
- Good for grammar and spelling correction
- 128K token context (4k variant available)

## Switching Models

### In the Application
Simply select from the **Mode dropdown** in the widget:
1. Each mode automatically uses its optimal model
2. Change anytime between dictations
3. No need to restart the app

### Custom Configuration
Edit `config.py` to:
- Change default modes
- Add custom modes
- Experiment with different models
- Adjust AI prompts

## Model Comparison Tips

**For Speed:**  
llama3.2:1b > phi3:mini > gemma3 > llama3.2 > mistral

**For Quality:**  
deepseek-r1:8b > mistral:7b > gemma3 > llama3.2

**For Reasoning:**  
deepseek-r1:8b > phi3 > mistral > llama3.2

**For Creativity:**  
gemma3 > llama3.2 > mistral

**For Code:**  
deepseek-coder > codegemma > codellama

## Memory Requirements

| Model | RAM Needed | GPU VRAM |
|-------|-----------|----------|
| llama3.2:1b | ~2GB | Optional |
| phi3:mini | ~3GB | Optional |
| gemma3 | ~4GB | Optional |
| llama3.2 | ~4GB | Optional |
| deepseek-coder | ~5GB | Recommended |
| mistral:7b | ~5GB | Recommended |
| deepseek-r1:8b | ~6GB | Recommended |

*Note: All models can run on CPU, but GPU acceleration significantly improves speed*

## Recommendations

🏆 **Best All-Around**: `mistral:7b-instruct`  
⚡ **Fastest**: `llama3.2:1b`  
🎨 **Most Creative**: `gemma3:latest`  
🧠 **Smartest**: `deepseek-r1:8b`  
📧 **Best for Emails**: `mistral:7b-instruct` (professional) / `gemma3` (casual)  
💻 **Best for Code**: `deepseek-coder:6.7b`

## Testing Your Models

Run this command to test model performance:
```bash
python demo_ai.py
```

This will show you how each model handles different types of text refinement.
