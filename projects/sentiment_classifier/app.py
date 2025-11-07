#!/usr/bin/env python3
"""
Sentiment Classifier - Classifies text as Positive/Neutral/Negative
"""

import argparse
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F


class SentimentClassifier:
    def __init__(self, model_name: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"):
        """Initialize the sentiment classification model."""
        print(f"🔄 Loading model: {model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        self.model.eval()
        
        # Map model labels to our labels
        self.label_map = {0: "NEGATIVE", 1: "NEUTRAL", 2: "POSITIVE"}
        print(f"✅ Model loaded on {self.device}")

    def classify(self, text: str) -> tuple:
        """Classify the sentiment of the given text."""
        # Tokenize and encode
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, 
                               max_length=512, padding=True).to(self.device)
        
        # Get predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = F.softmax(logits, dim=-1)
        
        # Get predicted class and confidence
        predicted_id = torch.argmax(probabilities, dim=-1).item()
        confidence = probabilities[0][predicted_id].item()
        label = self.label_map.get(predicted_id, "UNKNOWN")
        
        return label, confidence


def main():
    parser = argparse.ArgumentParser(description="Classify text sentiment as Positive/Neutral/Negative")
    parser.add_argument("--text", "-t", type=str, help="Text to classify")
    parser.add_argument("--file", "-f", type=str, help="File containing text to classify")
    parser.add_argument("--model", "-m", type=str, default="cardiffnlp/twitter-roberta-base-sentiment-latest",
                       help="Model to use for classification")
    parser.add_argument("--web", action="store_true", help="Run as web server")
    
    args = parser.parse_args()
    
    if args.web:
        from flask import Flask, request, render_template_string, jsonify
        
        app = Flask(__name__)
        classifier = SentimentClassifier(args.model)
        
        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sentiment Classifier</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                textarea { width: 100%; height: 200px; margin: 10px 0; }
                button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
                button:hover { background: #0056b3; }
                .result { margin-top: 20px; padding: 15px; border-radius: 5px; }
                .positive { background: #d4edda; color: #155724; }
                .negative { background: #f8d7da; color: #721c24; }
                .neutral { background: #fff3cd; color: #856404; }
            </style>
        </head>
        <body>
            <h1>💬 Sentiment Classifier</h1>
            <form method="POST">
                <textarea name="text" placeholder="Enter text to analyze..."></textarea>
                <br>
                <button type="submit">Classify Sentiment</button>
            </form>
            {% if sentiment %}
            <div class="result {{ sentiment.lower() }}">
                <h2>Sentiment: {{ sentiment }}</h2>
                <p>Confidence: {{ "%.2f"|format(confidence * 100) }}%</p>
            </div>
            {% endif %}
            {% if error %}
            <div class="result negative">
                <strong>Error:</strong> {{ error }}
            </div>
            {% endif %}
        </body>
        </html>
        """
        
        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                text = request.form.get('text', '').strip()
                if not text:
                    return render_template_string(HTML_TEMPLATE, error="Please enter some text")
                
                try:
                    sentiment, confidence = classifier.classify(text)
                    return render_template_string(HTML_TEMPLATE, 
                                                sentiment=sentiment, 
                                                confidence=confidence)
                except Exception as e:
                    return render_template_string(HTML_TEMPLATE, error=str(e))
            
            return render_template_string(HTML_TEMPLATE)
        
        @app.route('/api/classify', methods=['POST'])
        def api_classify():
            data = request.get_json()
            text = data.get('text', '')
            if not text:
                return jsonify({'error': 'Text is required'}), 400
            
            try:
                sentiment, confidence = classifier.classify(text)
                return jsonify({
                    'sentiment': sentiment,
                    'confidence': confidence,
                    'text': text
                })
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        print("🌐 Web server starting on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.text:
        try:
            classifier = SentimentClassifier(args.model)
            sentiment, confidence = classifier.classify(args.text)
            
            print("\n" + "="*50)
            print(f"Text: {args.text}")
            print(f"Sentiment: {sentiment}")
            print(f"Confidence: {confidence:.2%}")
            print("="*50)
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
    
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                texts = [line.strip() for line in f if line.strip()]
            
            classifier = SentimentClassifier(args.model)
            
            print("\n" + "="*50)
            for i, text in enumerate(texts, 1):
                sentiment, confidence = classifier.classify(text)
                print(f"{i}. {text}")
                print(f"   → {sentiment} ({confidence:.2%})")
                print()
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

