# 🌐 Language Translator

Translates text between multiple languages using OpenAI's translation capabilities.

## 📋 Description

A Python tool that translates text between 100+ languages with high accuracy. Uses GPT models for context-aware translations.

## 🚀 Features

- Translate between 100+ languages
- Context-aware translations
- Batch translation support
- Preserve formatting and structure
- CLI and web interfaces

## 🛠️ Installation

```bash
cd projects/language_translator
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
python app.py --text "Hello" --from en --to es
```

### Web Mode

```bash
python app.py --web
```

## 📝 Example

```bash
python app.py --text "Good morning" --from en --to fr
# Output: Bonjour
```

## 🧪 Testing

```bash
pytest tests/
```

## 📄 License

MIT

