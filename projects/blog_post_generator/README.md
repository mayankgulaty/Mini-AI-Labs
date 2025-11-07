# ✍️ Blog Post Generator

Generates well-structured blog posts on any topic using AI.

## 📋 Description

A Python tool that creates complete, SEO-friendly blog posts with titles, introductions, body content, and conclusions. Perfect for content creators and marketers.

## 🚀 Features

- Generate complete blog posts
- SEO-optimized content
- Multiple writing styles
- Customizable length and tone
- Topic research and structuring
- CLI and web interfaces

## 🛠️ Installation

```bash
cd projects/blog_post_generator
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
python app.py --topic "AI in Healthcare" --length "long" --style "professional"
```

### Web Mode

```bash
python app.py --web
```

## 📝 Example

```bash
python app.py --topic "Python Best Practices" --length medium
```

## 🧪 Testing

```bash
pytest tests/
```

## 📄 License

MIT

