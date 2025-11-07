# 💬 Sentiment Classifier

Classifies text as Positive / Neutral / Negative using PyTorch and Transformers.

## 📋 Description

A text sentiment analysis tool that classifies input text into three categories: Positive, Neutral, or Negative. Built with PyTorch and HuggingFace Transformers for accurate sentiment detection.

## 🚀 Features

- Three-class sentiment classification (Positive/Neutral/Negative)
- Fast inference using pre-trained transformer models
- CLI and web interface options
- Batch processing support

## 🛠️ Installation

```bash
cd projects/sentiment_classifier
pip install -r requirements.txt
```

## 💻 Usage

### CLI Mode

```bash
python app.py --text "I love this product!"
```

### Batch Mode

```bash
python app.py --file input.txt
```

### Web Mode

```bash
python app.py --web
```

Then visit `http://localhost:5000`

## 📝 Example

```bash
python app.py --text "This is amazing!"
# Output: POSITIVE (confidence: 0.95)
```

## 🧪 Testing

```bash
pytest tests/
```

## 📄 License

MIT

