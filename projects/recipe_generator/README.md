# 🍳 Recipe Generator

Generates personalized recipes based on available ingredients or dietary preferences.

## 📋 Description

A Python tool that creates custom recipes using AI. Input your ingredients or dietary requirements, and get detailed cooking instructions.

## 🚀 Features

- Generate recipes from ingredients
- Support for dietary restrictions
- Cuisine type selection
- Detailed cooking instructions
- Nutritional information

## 🛠️ Installation

```bash
cd projects/recipe_generator
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
python app.py --ingredients "chicken, tomatoes, onions" --cuisine "italian"
```

### Web Mode

```bash
python app.py --web
```

## 📝 Example

```bash
python app.py --ingredients "eggs, flour, milk" --dietary "vegetarian"
```

## 🧪 Testing

```bash
pytest tests/
```

## 📄 License

MIT

