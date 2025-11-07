#!/usr/bin/env python3
"""
Language Translator - Translates text between multiple languages
"""

import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class LanguageTranslator:
    def __init__(self):
        """Initialize the translator."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key)

    def translate(self, text: str, from_lang: str = "auto", to_lang: str = "en") -> str:
        """Translate text from one language to another."""
        prompt = f"Translate the following text from {from_lang} to {to_lang}. Only return the translation, no explanations:\n\n{text}"
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional translator. Translate accurately and naturally."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description="Translate text between languages")
    parser.add_argument("--text", "-t", type=str, help="Text to translate")
    parser.add_argument("--from", "-f", dest="from_lang", type=str, default="auto", help="Source language (auto-detect if 'auto')")
    parser.add_argument("--to", "-o", dest="to_lang", type=str, default="en", help="Target language")
    parser.add_argument("--web", action="store_true", help="Run as web server")
    
    args = parser.parse_args()
    
    if args.web:
        from flask import Flask, request, render_template_string
        
        app = Flask(__name__)
        translator = LanguageTranslator()
        
        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Language Translator</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                textarea { width: 100%; height: 150px; margin: 10px 0; }
                select, button { padding: 10px; margin: 5px; }
                button { background: #007bff; color: white; border: none; cursor: pointer; }
                .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>🌐 Language Translator</h1>
            <form method="POST">
                <textarea name="text" placeholder="Enter text to translate..." required></textarea>
                <select name="from_lang">
                    <option value="auto">Auto-detect</option>
                    <option value="en">English</option>
                    <option value="es">Spanish</option>
                    <option value="fr">French</option>
                    <option value="de">German</option>
                    <option value="zh">Chinese</option>
                    <option value="ja">Japanese</option>
                </select>
                <select name="to_lang">
                    <option value="en">English</option>
                    <option value="es">Spanish</option>
                    <option value="fr">French</option>
                    <option value="de">German</option>
                    <option value="zh">Chinese</option>
                    <option value="ja">Japanese</option>
                </select>
                <button type="submit">Translate</button>
            </form>
            {% if translation %}
            <div class="result">
                <strong>Translation:</strong><br>{{ translation }}
            </div>
            {% endif %}
        </body>
        </html>
        """
        
        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                text = request.form.get('text', '')
                from_lang = request.form.get('from_lang', 'auto')
                to_lang = request.form.get('to_lang', 'en')
                try:
                    translation = translator.translate(text, from_lang, to_lang)
                    return render_template_string(HTML_TEMPLATE, translation=translation)
                except Exception as e:
                    return render_template_string(HTML_TEMPLATE, error=str(e))
            return render_template_string(HTML_TEMPLATE)
        
        print("🌐 Web server starting on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.text:
        try:
            translator = LanguageTranslator()
            translation = translator.translate(args.text, args.from_lang, args.to_lang)
            print(f"\nOriginal: {args.text}")
            print(f"Translation ({args.from_lang} → {args.to_lang}): {translation}")
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

