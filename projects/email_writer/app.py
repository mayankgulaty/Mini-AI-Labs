#!/usr/bin/env python3
"""
Email Writer - Generates professional emails using AI
"""

import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class EmailWriter:
    def __init__(self):
        """Initialize the email writer."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key)

    def write(self, purpose: str, recipient: str = "", tone: str = "professional", 
              context: str = "", length: str = "medium") -> str:
        """Generate an email."""
        prompt = f"""Write a {tone} email with the following details:
- Purpose: {purpose}
- Recipient: {recipient or 'General recipient'}
- Context: {context or 'No specific context'}
- Length: {length}

Generate a complete email with subject line and body. Make it professional and appropriate."""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert email writer. Write clear, professional emails."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description="Generate professional emails")
    parser.add_argument("--purpose", "-p", type=str, help="Email purpose")
    parser.add_argument("--recipient", "-r", type=str, default="", help="Recipient type/name")
    parser.add_argument("--tone", "-t", type=str, default="professional", help="Email tone")
    parser.add_argument("--context", "-c", type=str, default="", help="Additional context")
    parser.add_argument("--length", "-l", type=str, default="medium", help="Email length (short/medium/long)")
    parser.add_argument("--web", action="store_true", help="Run as web server")
    
    args = parser.parse_args()
    
    if args.web:
        from flask import Flask, request, render_template_string
        
        app = Flask(__name__)
        writer = EmailWriter()
        
        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Email Writer</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                input, textarea, select { width: 100%; padding: 10px; margin: 5px 0; }
                button { padding: 12px 24px; background: #007bff; color: white; border: none; cursor: pointer; }
                .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; white-space: pre-wrap; }
            </style>
        </head>
        <body>
            <h1>📧 Email Writer</h1>
            <form method="POST">
                <input type="text" name="purpose" placeholder="Email purpose (e.g., meeting request)" required>
                <input type="text" name="recipient" placeholder="Recipient (optional)">
                <textarea name="context" placeholder="Additional context (optional)" rows="3"></textarea>
                <select name="tone">
                    <option value="professional">Professional</option>
                    <option value="casual">Casual</option>
                    <option value="formal">Formal</option>
                    <option value="friendly">Friendly</option>
                </select>
                <select name="length">
                    <option value="short">Short</option>
                    <option value="medium" selected>Medium</option>
                    <option value="long">Long</option>
                </select>
                <button type="submit">Generate Email</button>
            </form>
            {% if email %}
            <div class="result">{{ email }}</div>
            {% endif %}
        </body>
        </html>
        """
        
        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                purpose = request.form.get('purpose', '')
                recipient = request.form.get('recipient', '')
                tone = request.form.get('tone', 'professional')
                context = request.form.get('context', '')
                length = request.form.get('length', 'medium')
                try:
                    email = writer.write(purpose, recipient, tone, context, length)
                    return render_template_string(HTML_TEMPLATE, email=email)
                except Exception as e:
                    return render_template_string(HTML_TEMPLATE, error=str(e))
            return render_template_string(HTML_TEMPLATE)
        
        print("🌐 Web server starting on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.purpose:
        try:
            writer = EmailWriter()
            email = writer.write(args.purpose, args.recipient, args.tone, args.context, args.length)
            print("\n" + "="*50)
            print("GENERATED EMAIL:")
            print("="*50)
            print(email)
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

