#!/usr/bin/env python3
"""
Image Captioner - Generates human-like captions for images using BLIP
"""

import argparse
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import os


class ImageCaptioner:
    def __init__(self, model_name: str = "Salesforce/blip-image-captioning-base"):
        """Initialize the BLIP model for image captioning."""
        print(f"🔄 Loading model: {model_name}...")
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        print(f"✅ Model loaded on {self.device}")

    def caption_image(self, image_path: str) -> str:
        """Generate a caption for the given image."""
        try:
            # Load and process image
            image = Image.open(image_path).convert('RGB')
            
            # Process image and generate caption
            inputs = self.processor(image, return_tensors="pt").to(self.device)
            
            # Generate caption
            out = self.model.generate(**inputs, max_length=50)
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            
            return caption
        except Exception as e:
            raise Exception(f"Error processing image: {e}")


def main():
    parser = argparse.ArgumentParser(description="Generate captions for images using BLIP")
    parser.add_argument("--image", "-i", type=str, help="Path to input image")
    parser.add_argument("--model", "-m", type=str, default="Salesforce/blip-image-captioning-base", 
                       help="BLIP model to use")
    parser.add_argument("--web", action="store_true", help="Run as web server")
    
    args = parser.parse_args()
    
    if args.web:
        from flask import Flask, request, render_template_string, jsonify, send_from_directory
        import werkzeug
        
        app = Flask(__name__)
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
        
        captioner = ImageCaptioner(args.model)
        
        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Image Captioner</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                input[type="file"] { margin: 20px 0; }
                button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
                button:hover { background: #0056b3; }
                .caption { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }
                img { max-width: 100%; height: auto; margin: 20px 0; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>🖼️ Image Captioner</h1>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="image" accept="image/*" required>
                <br>
                <button type="submit">Generate Caption</button>
            </form>
            {% if caption %}
            <div class="caption">
                <h2>Caption:</h2>
                <p>{{ caption }}</p>
            </div>
            {% endif %}
            {% if error %}
            <div class="caption" style="background: #f8d7da; color: #721c24;">
                <strong>Error:</strong> {{ error }}
            </div>
            {% endif %}
        </body>
        </html>
        """
        
        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                if 'image' not in request.files:
                    return render_template_string(HTML_TEMPLATE, error="No image file provided")
                
                file = request.files['image']
                if file.filename == '':
                    return render_template_string(HTML_TEMPLATE, error="No file selected")
                
                try:
                    # Save uploaded file temporarily
                    temp_path = f"/tmp/{file.filename}"
                    file.save(temp_path)
                    
                    # Generate caption
                    caption = captioner.caption_image(temp_path)
                    
                    # Clean up
                    os.remove(temp_path)
                    
                    return render_template_string(HTML_TEMPLATE, caption=caption)
                except Exception as e:
                    return render_template_string(HTML_TEMPLATE, error=str(e))
            
            return render_template_string(HTML_TEMPLATE)
        
        print("🌐 Web server starting on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.image:
        if not os.path.exists(args.image):
            print(f"❌ Error: Image file not found: {args.image}")
            return 1
        
        try:
            captioner = ImageCaptioner(args.model)
            print(f"📷 Processing image: {args.image}")
            caption = captioner.caption_image(args.image)
            
            print("\n" + "="*50)
            print("CAPTION:")
            print("="*50)
            print(caption)
            print("="*50)
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

