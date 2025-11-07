# 📄 PDF Q&A Bot

Answers questions about PDF documents using AI-powered document understanding.

## 📋 Description

A Python tool that extracts text from PDFs and answers questions about the content using AI. Perfect for quickly finding information in long documents.

## 🚀 Features

- Extract text from PDF documents
- Answer questions about PDF content
- Context-aware responses
- Support for multiple PDF formats
- CLI and web interfaces

## 🛠️ Installation

```bash
cd projects/pdf_qa_bot
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
python app.py --pdf document.pdf --question "What is the main topic?"
```

### Web Mode

```bash
python app.py --web
```

## 📝 Example

```bash
python app.py --pdf research_paper.pdf --question "What are the key findings?"
```

## 🧪 Testing

```bash
pytest tests/
```

## 📄 License

MIT

