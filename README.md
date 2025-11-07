<div align="center">

# 🧪 Mini AI Labs

**A growing collection of AI-powered mini tools** — each designed to solve real-world problems

*Created, refactored, and maintained with the help of **Cursor Agent***

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Node.js](https://img.shields.io/badge/Node.js-18+-green.svg)](https://nodejs.org/)

</div>

---

## 🚀 About

**Mini AI Labs** is a playground where **AI builds software**. Each project in this repository is a standalone, production-ready tool that demonstrates practical AI applications.

### ✨ What Makes Each Project Special

- 📚 **Self-Documented** - Comprehensive READMEs with examples
- ✅ **Tested** - Unit tests included for reliability
- 🌐 **Deployable** - Both CLI and web interfaces available
- 🤖 **AI-Maintained** - Auto-updated via Cursor AI Agent
- 🎯 **Production-Ready** - Clean code, error handling, and best practices

---

## 🧩 Projects

<div align="center">

### 🧠 Chat Summary Bot

**Summarizes any chat or transcript using GPT**

```bash
Python • OpenAI API • Flask
```

[📖 Documentation](./projects/chat_summary_bot/README.md) • [💻 Code](./projects/chat_summary_bot/)

---

### 🖼️ Image Captioner

**Captions any uploaded image with a human-like summary**

```bash
Python • BLIP • HuggingFace • PyTorch
```

[📖 Documentation](./projects/image_captioner/README.md) • [💻 Code](./projects/image_captioner/)

---

### 💬 Sentiment Classifier

**Classifies text as Positive / Neutral / Negative**

```bash
Python • PyTorch • Transformers • Flask
```

[📖 Documentation](./projects/sentiment_classifier/README.md) • [💻 Code](./projects/sentiment_classifier/)

---

### 🌍 Travel Itinerary Generator

**Generates personalized trip plans from JSON input**

```bash
Node.js • OpenAI • Google Maps API • Express
```

[📖 Documentation](./projects/travel_itinerary_gen/README.md) • [💻 Code](./projects/travel_itinerary_gen/)

---

### 📄 Resume Optimizer

**Analyzes a resume and rewrites it for a given job role**

```bash
Python • LangChain • PDFminer • OpenAI
```

[📖 Documentation](./projects/resume_optimizer/README.md) • [💻 Code](./projects/resume_optimizer/)

</div>

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (for Python projects)
- **Node.js 18+** (for Node.js projects)
- **API Keys** (OpenAI, Google Maps - as needed per project)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mayankgulaty/Mini-AI-Labs.git
   cd Mini-AI-Labs
   ```

2. **Choose a project** and navigate to it
   ```bash
   cd projects/chat_summary_bot
   ```

3. **Install dependencies**
   ```bash
   # For Python projects
   pip install -r requirements.txt
   
   # For Node.js projects
   npm install
   ```

4. **Set up environment variables**
   ```bash
   # Create a .env file with your API keys
   OPENAI_API_KEY=your-key-here
   ```

5. **Run the project**
   ```bash
   # CLI mode
   python app.py --input sample.txt
   
   # Web mode
   python app.py --web
   ```

---

## 📊 Project Overview

| Project | Language | Framework | API/Model | Status |
|---------|----------|-----------|-----------|--------|
| 🧠 Chat Summary Bot | Python | Flask | OpenAI GPT | ✅ Ready |
| 🖼️ Image Captioner | Python | Flask | BLIP (HuggingFace) | ✅ Ready |
| 💬 Sentiment Classifier | Python | Flask | RoBERTa | ✅ Ready |
| 🌍 Travel Itinerary Gen | Node.js | Express | OpenAI + Google Maps | ✅ Ready |
| 📄 Resume Optimizer | Python | Flask | LangChain + OpenAI | ✅ Ready |

---

## 🛠️ Tech Stack

### Python Projects
- **OpenAI API** - GPT models for text generation
- **LangChain** - LLM orchestration framework
- **PyTorch** - Deep learning framework
- **Transformers** - HuggingFace model library
- **Flask** - Web framework
- **PDFminer** - PDF text extraction

### Node.js Projects
- **Express** - Web framework
- **OpenAI SDK** - GPT API integration
- **Google Maps API** - Location services

---

## 📝 Usage Examples

### Chat Summary Bot
```bash
python app.py --input meeting_transcript.txt --output summary.txt
```

### Image Captioner
```bash
python app.py --image photo.jpg
```

### Sentiment Classifier
```bash
python app.py --text "I love this product!"
# Output: POSITIVE (confidence: 95%)
```

### Travel Itinerary Generator
```bash
node app.js --input trip.json --output itinerary.json
```

### Resume Optimizer
```bash
python app.py --resume resume.pdf --job "Software Engineer"
```

---

## 🧪 Testing

Each project includes test suites. Run tests with:

```bash
# Python projects
pytest tests/

# Node.js projects
npm test
```

---

## 📚 Documentation

Each project has its own detailed README with:
- Installation instructions
- Usage examples
- API documentation
- Configuration options
- Troubleshooting tips

Visit individual project folders for specific documentation.

---

## 🤝 Contributing

Contributions are welcome! Each project is maintained independently:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with ❤️ using **Cursor Agent**
- Powered by **OpenAI**, **HuggingFace**, and **Google Maps**
- Inspired by the need for practical AI tools

---

<div align="center">

**Made with ❤️ by the AI community**

⭐ Star this repo if you find it useful!

</div>
