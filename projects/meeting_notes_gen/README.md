# 📝 Meeting Notes Generator

Generates structured meeting notes and action items from transcripts or audio.

## 📋 Description

A Python tool that processes meeting transcripts or audio files and generates organized meeting notes with key points, decisions, and action items.

## 🚀 Features

- Extract key points from meetings
- Generate action items
- Identify decisions made
- Support for transcript and audio input
- Structured output format

## 🛠️ Installation

```bash
cd projects/meeting_notes_gen
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
python app.py --transcript meeting.txt
```

### Web Mode

```bash
python app.py --web
```

## 📝 Example

```bash
python app.py --transcript meeting_transcript.txt --output notes.md
```

## 🧪 Testing

```bash
pytest tests/
```

## 📄 License

MIT

