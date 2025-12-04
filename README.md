# Audio Transcription and Summarization Tool

A Python tool that transcribes audio files, performs speaker diarization, and generates AI-powered summaries. Built with WhisperX for transcription and Google's Gemini for summarization.

> **Note:** This is a personal side project developed for learning purposes and a specific use case. It may not be production-ready and is provided as-is.

## Features

- **High-quality transcription** using Fast WhisperX (large-v3 model)
- **Speaker diarization** to identify different speakers in the audio
- **Word-level alignment** for accurate timestamps
- **AI-powered summarization** using Google Gemini 2.0 Flash
- **Batch processing** support for multiple audio files
- **DOCX export** for both transcriptions and summaries
- **Customizable prompts** via environment variables

## Requirements

### Hardware

- **GPU with CUDA support** (recommended for faster processing)
  - NVIDIA GPU with CUDA 12.x support
  - At least 8GB VRAM recommended for large-v3 model
- **CPU mode** is possible but significantly slower

### Software

- Python 3.8 or higher
- CUDA toolkit (if using GPU)
- NVIDIA drivers compatible with CUDA 12.x

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd summarize_audio
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install NVIDIA CUDA libraries (Linux only)

For Linux systems, install the NVIDIA CUDA libraries:

```bash
pip install nvidia-cublas-cu12 nvidia-cudnn-cu12==9.*
```

**Important:** On Linux, you may need to set `LD_LIBRARY_PATH` before running Python. See the [Configuration](#configuration) section for details.

### 5. Set up environment variables


Create a `.env` and add your API keys:

```env
GEMINI_KEY=your_gemini_api_key_here
HF_TOKEN=your_huggingface_token_here
```

**Getting API Keys:**
- **Gemini API Key**: Get it from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Hugging Face Token**: Get it from [Hugging Face Settings](https://huggingface.co/settings/tokens) (required for speaker diarization models)

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_KEY` | Google Gemini API key for summarization | Yes |
| `HF_TOKEN` | Hugging Face token for speaker diarization models | Yes |
| `SUMMARIZATION_PROMPT` | Custom prompt template for summarization (optional) | No |

### Custom Summarization Prompts

By default, the tool uses a generic summarization prompt. You can customize it by setting the `SUMMARIZATION_PROMPT` environment variable in your `.env` file:

```env
SUMMARIZATION_PROMPT="Your custom prompt here. The transcription text will be automatically appended."
```

The transcription text will be automatically appended to your prompt. See `.env.example` for an example.

### CUDA Library Path (Linux/WSL)

If you encounter CUDA library errors on Linux or WSL, you may need to set `LD_LIBRARY_PATH` before running the script. The recommended approach is to set it in your shell:

```bash
export LD_LIBRARY_PATH=$(python3 -c 'import os; import nvidia.cublas.lib; import nvidia.cudnn.lib; print(os.path.dirname(nvidia.cublas.lib.__file__) + ":" + os.path.dirname(nvidia.cudnn.lib.__file__))')
```

Alternatively, you can add this to your `.bashrc` or `.zshrc` for persistence.

## Usage

### Single Audio File

Process a single audio file:

```bash
python summarize.py <audio_file> <output_directory>
```

**Example:**
```bash
python summarize.py audio.mp3 ./outputs
```

This will generate:
- `transcription_audio.docx` - Full transcription with speaker labels
- `summary_audio.docx` - AI-generated summary

### Batch Processing

Process all audio files in a directory:

```bash
python batch_summary.py <input_directory> <output_directory>
```

**Example:**
```bash
python batch_summary.py ./audios ./outputs
```

Supported audio formats: `.mp3`, `.wav`, `.m4a`, `.flac`, `.aac`

### Output Format

**Transcription files** contain:
- Speaker labels: `[SPEAKER_00]: text`
- Full conversation transcript

**Summary files** contain:
- Structured summary based on your prompt template
- Markdown formatting (headings, bold text, bullet points) preserved in DOCX

## Project Structure

```
summarize_audio/
├── src/
│   ├── audio_handler.py    # Transcription, alignment, and diarization
│   ├── doc_write.py         # DOCX file writing utilities
│   └── prompts.py           # Prompt management
├── summarize.py             # Main script for single file processing
├── batch_summary.py         # Batch processing script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Performance Tips

- **GPU Memory**: If you encounter out-of-memory errors, reduce `batch_size` in `summarize.py` (default: 16)
- **Compute Type**: Change `compute_type` from `"float16"` to `"int8"` for lower memory usage (may reduce accuracy)
- **Model Size**: The default model is `large-v3`. For faster processing, you can modify `audio_handler.py` to use smaller models (`medium`, `small`, etc.)

## Privacy and Security

⚠️ **Important Privacy Notice:**

- This tool sends audio transcriptions to Google's Gemini API for summarization
- Audio files and transcriptions may contain sensitive information
- Ensure compliance with relevant privacy regulations (HIPAA, GDPR, etc.) if handling sensitive data
- Consider anonymizing or using synthetic data for testing


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [WhisperX](https://github.com/m-bain/whisperX) for transcription and diarization
- [Google Gemini](https://deepmind.google/technologies/gemini/) for AI summarization
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) for efficient Whisper inference

