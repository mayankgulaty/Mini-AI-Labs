#!/usr/bin/env python3
"""
Code Explainer - Explains code in plain English
"""

import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class CodeExplainer:
    def __init__(self):
        """Initialize the code explainer."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key)

    def explain(self, code: str, language: str = "auto") -> str:
        """Explain code in plain English."""
        prompt = f"""Explain the following code in plain English. Break down what it does step by step, explain the logic, and highlight any important patterns or concepts.

Code:
```{language}
{code}
```

Provide a clear, comprehensive explanation:"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert programming instructor. Explain code clearly and comprehensively."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description="Explain code in plain English")
    parser.add_argument("--file", "-f", type=str, help="Code file to explain")
    parser.add_argument("--code", "-c", type=str, help="Code string to explain")
    parser.add_argument("--language", "-l", type=str, default="auto", help="Programming language")
    parser.add_argument("--web", action="store_true", help="Run as web server")
    
    args = parser.parse_args()
    
    if args.web:
        from flask import Flask, request, render_template_string
        
        app = Flask(__name__)
        explainer = CodeExplainer()
        
        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Code Explainer</title>
            <style>
                body { font-family: 'Courier New', monospace; max-width: 1000px; margin: 50px auto; padding: 20px; }
                textarea { width: 100%; height: 300px; margin: 10px 0; font-family: monospace; }
                select, button { padding: 10px; margin: 5px; }
                button { background: #007bff; color: white; border: none; cursor: pointer; }
                .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; white-space: pre-wrap; }
            </style>
        </head>
        <body>
            <h1>💻 Code Explainer</h1>
            <form method="POST">
                <textarea name="code" placeholder="Paste your code here..." required></textarea>
                <select name="language">
                    <option value="auto">Auto-detect</option>
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="java">Java</option>
                    <option value="cpp">C++</option>
                    <option value="go">Go</option>
                </select>
                <button type="submit">Explain Code</button>
            </form>
            {% if explanation %}
            <div class="result">{{ explanation }}</div>
            {% endif %}
        </body>
        </html>
        """
        
        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                code = request.form.get('code', '')
                language = request.form.get('language', 'auto')
                try:
                    explanation = explainer.explain(code, language)
                    return render_template_string(HTML_TEMPLATE, explanation=explanation)
                except Exception as e:
                    return render_template_string(HTML_TEMPLATE, error=str(e))
            return render_template_string(HTML_TEMPLATE)
        
        print("🌐 Web server starting on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                code = f.read()
            explainer = CodeExplainer()
            explanation = explainer.explain(code, args.language)
            print("\n" + "="*50)
            print("CODE EXPLANATION:")
            print("="*50)
            print(explanation)
            print("="*50)
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
    elif args.code:
        try:
            explainer = CodeExplainer()
            explanation = explainer.explain(args.code, args.language)
            print("\n" + "="*50)
            print("CODE EXPLANATION:")
            print("="*50)
            print(explanation)
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

