# 🔐 Password Generator

Generates secure passwords with strength analysis using AI.

## 📋 Description

A Python tool that generates strong, secure passwords and analyzes password strength. Includes options for different complexity levels and character sets.

## 🚀 Features

- Generate secure passwords
- Password strength analysis
- Customizable length and complexity
- Multiple character set options
- Password validation
- CLI and web interfaces

## 🛠️ Installation

```bash
cd projects/password_generator
pip install -r requirements.txt
```

## 💻 Usage

### CLI Mode

```bash
python app.py --length 16 --include-symbols
```

### Web Mode

```bash
python app.py --web
```

## 📝 Example

```bash
python app.py --length 20 --include-numbers --include-symbols
```

## 🧪 Testing

```bash
pytest tests/
```

## 📄 License

MIT

