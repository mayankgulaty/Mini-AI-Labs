# 🧠 Chat Summary Bot

Summarizes any chat or transcript using GPT.

## 📋 Description

A Python tool that takes chat logs, transcripts, or conversation files and generates concise, informative summaries using OpenAI's GPT API.

## 🚀 Features

- Summarize chat logs and transcripts
- Extract key points and action items
- Support for multiple input formats (text, JSON, CSV)
- Configurable summary length and detail level

## 🛠️ Installation

```bash
cd projects/chat_summary_bot
pip install -r requirements.txt
```

## ⚙️ Setup

1. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file:
```
OPENAI_API_KEY=your-api-key-here
```

## 💻 Usage

### CLI Mode

```bash
python app.py --input chat.txt --output summary.txt
```

### Web Mode

```bash
python app.py --web
```

Then visit `http://localhost:5000`

## 📝 Example

```bash
python app.py --input sample_chat.txt
```

## 🧪 Testing

```bash
pytest tests/
```

## 📄 License

MIT

