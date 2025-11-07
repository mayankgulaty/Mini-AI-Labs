#!/usr/bin/env python3
"""
Code Review Assistant - Provides AI-powered code reviews
"""

import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class CodeReviewAssistant:
    def __init__(self):
        """Initialize the code review assistant."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key)

    def review(self, code: str, language: str = "auto") -> str:
        """Review code and provide suggestions."""
        prompt = f"""Review the following {language} code and provide a comprehensive code review.

Code:
```{language}
{code}
```

Please provide:
1. Overall Assessment
2. Bugs and Issues Found
3. Code Style Suggestions
4. Performance Improvements
5. Security Concerns (if any)
6. Best Practices Recommendations

Format your review clearly with sections:"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert code reviewer. Provide constructive, detailed code reviews."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description="Review code with AI assistance")
    parser.add_argument("--file", "-f", type=str, help="Code file to review")
    parser.add_argument("--code", "-c", type=str, help="Code string to review")
    parser.add_argument("--language", "-l", type=str, default="auto", help="Programming language")
    parser.add_argument("--web", action="store_true", help="Run as web server")
    
    args = parser.parse_args()
    
    if args.web:
        from flask import Flask, request, render_template_string
        
        app = Flask(__name__)
        reviewer = CodeReviewAssistant()
        
        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <head>
            <title>Code Review Assistant</title>
            <style>
                body { font-family: 'Courier New', monospace; max-width: 1000px; margin: 50px auto; padding: 20px; }
                textarea { width: 100%; height: 400px; margin: 10px 0; font-family: monospace; }
                select, button { padding: 10px; margin: 5px; }
                button { background: #007bff; color: white; border: none; cursor: pointer; }
                .result { margin-top: 20px; padding: 20px; background: #f8f9fa; border-radius: 5px; white-space: pre-wrap; }
            </style>
        </head>
        <body>
            <h1>🔍 Code Review Assistant</h1>
            <form method="POST">
                <textarea name="code" placeholder="Paste your code here..." required></textarea>
                <select name="language">
                    <option value="auto">Auto-detect</option>
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="java">Java</option>
                    <option value="cpp">C++</option>
                </select>
                <button type="submit">Review Code</button>
            </form>
            {% if review %}
            <div class="result">{{ review }}</div>
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
                    review = reviewer.review(code, language)
                    return render_template_string(HTML_TEMPLATE, review=review)
                except Exception as e:
                    return render_template_string(HTML_TEMPLATE, error=str(e))
            return render_template_string(HTML_TEMPLATE)
        
        print("🌐 Web server starting on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                code = f.read()
            reviewer = CodeReviewAssistant()
            review = reviewer.review(code, args.language)
            print("\n" + "="*50)
            print("CODE REVIEW:")
            print("="*50)
            print(review)
            print("="*50)
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
    elif args.code:
        try:
            reviewer = CodeReviewAssistant()
            review = reviewer.review(args.code, args.language)
            print("\n" + "="*50)
            print("CODE REVIEW:")
            print("="*50)
            print(review)
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

