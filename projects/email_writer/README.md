# 📧 Email Writer

Generates professional emails for various purposes using AI.

## 📋 Description

A Python tool that generates well-written, professional emails for business, personal, or marketing purposes. Customize tone, length, and purpose.

## 🚀 Features

- Generate professional emails
- Multiple email types (business, personal, marketing)
- Customizable tone and length
- Context-aware content generation
- CLI and web interfaces

## 🛠️ Installation

```bash
cd projects/email_writer
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
python app.py --purpose "follow-up" --recipient "client" --tone "professional"
```

### Web Mode

```bash
python app.py --web
```

## 📝 Example

```bash
python app.py --purpose "meeting request" --context "Discuss project timeline"
```

## 🧪 Testing

```bash
pytest tests/
```

## 📄 License

MIT

