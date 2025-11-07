# 🔊 Text to Speech Converter

Converts any text into natural-sounding speech using OpenAI's TTS API.

## 📋 Description

A Python tool that converts text to high-quality speech audio files. Perfect for creating voiceovers, audiobooks, or accessibility features.

## 🚀 Features

- Convert text to natural-sounding speech
- Multiple voice options
- Support for various output formats (MP3, WAV)
- Batch processing support
- CLI and web interfaces

## 🛠️ Installation

```bash
cd projects/text_to_speech
pip install -r requirements.txt
```

## ⚙️ Setup

Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 💻 Usage

### CLI Mode

```bash
python app.py --text "Hello, world!" --output speech.mp3
```

### Web Mode

```bash
python app.py --web
```

## 📝 Example

```bash
python app.py --text "Welcome to Mini AI Labs" --voice alloy
```

## 🧪 Testing

```bash
pytest tests/
```

## 📄 License

MIT

