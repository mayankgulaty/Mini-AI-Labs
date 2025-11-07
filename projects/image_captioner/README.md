# 🖼️ Image Captioner

Captions any uploaded image with a human-like summary using BLIP model from HuggingFace.

## 📋 Description

A Python tool that generates natural language captions for images using the BLIP (Bootstrapping Language-Image Pre-training) model. Perfect for accessibility, content management, or automated image description.

## 🚀 Features

- Generate human-like image captions
- Support for multiple image formats (JPG, PNG, WebP)
- CLI and web interface options
- Uses state-of-the-art BLIP model

## 🛠️ Installation

```bash
cd projects/image_captioner
pip install -r requirements.txt
```

## 💻 Usage

### CLI Mode

```bash
python app.py --image path/to/image.jpg
```

### Web Mode

```bash
python app.py --web
```

Then visit `http://localhost:5000` and upload an image.

## 📝 Example

```bash
python app.py --image sample.jpg
# Output: A beautiful sunset over the ocean with orange and pink clouds
```

## 🧪 Testing

```bash
pytest tests/
```

## 📄 License

MIT

