# 📄 Resume Optimizer

Analyzes a resume and rewrites it for a given job role using LangChain and PDFminer.

## 📋 Description

A Python tool that analyzes your resume (PDF format) and optimizes it for a specific job role. Uses LangChain for intelligent text processing and PDFminer for extracting text from PDF resumes.

## 🚀 Features

- Extract text from PDF resumes
- Analyze resume content and structure
- Optimize resume for specific job roles
- Generate improved versions with AI suggestions
- Support for multiple resume formats

## 🛠️ Installation

```bash
cd projects/resume_optimizer
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
python app.py --resume resume.pdf --job "Software Engineer" --output optimized_resume.txt
```

### Web Mode

```bash
python app.py --web
```

Then visit `http://localhost:5000`

## 📝 Example

```bash
python app.py --resume my_resume.pdf --job "Senior Data Scientist"
```

## 🧪 Testing

```bash
pytest tests/
```

## 📄 License

MIT

