#!/usr/bin/env python3
"""
Chat Summary Bot - Summarizes chat logs and transcripts using GPT
"""

import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def read_chat_file(file_path: str) -> str:
    """Read chat content from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def summarize_chat(chat_content: str, model: str = "gpt-3.5-turbo") -> str:
    """Generate a summary of the chat using GPT."""
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY not set. Please set it in your environment or .env file.")
    
    prompt = f"""Please provide a concise summary of the following chat/transcript. 
    Include key points, main topics discussed, and any action items or decisions made.
    
    Chat content:
    {chat_content}
    
    Summary:"""
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes conversations and transcripts."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description="Summarize chat logs and transcripts using GPT")
    parser.add_argument("--input", "-i", type=str, help="Input chat file path")
    parser.add_argument("--output", "-o", type=str, help="Output summary file path (optional)")
    parser.add_argument("--model", "-m", type=str, default="gpt-3.5-turbo", help="OpenAI model to use")
    parser.add_argument("--web", action="store_true", help="Run as web server")
    
    args = parser.parse_args()
    
    if args.web:
        from flask import Flask, request, render_template_string, jsonify
        app = Flask(__name__)
        
        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Chat Summary Bot</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                textarea { width: 100%; height: 300px; margin: 10px 0; }
                button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
                button:hover { background: #0056b3; }
                .summary { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>🧠 Chat Summary Bot</h1>
            <form method="POST">
                <textarea name="chat_content" placeholder="Paste your chat or transcript here..."></textarea>
                <br>
                <button type="submit">Generate Summary</button>
            </form>
            {% if summary %}
            <div class="summary">
                <h2>Summary:</h2>
                <p>{{ summary }}</p>
            </div>
            {% endif %}
        </body>
        </html>
        """
        
        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                chat_content = request.form.get('chat_content', '')
                try:
                    summary = summarize_chat(chat_content, args.model)
                    return render_template_string(HTML_TEMPLATE, summary=summary)
                except Exception as e:
                    return render_template_string(HTML_TEMPLATE, error=str(e))
            return render_template_string(HTML_TEMPLATE)
        
        print("🌐 Web server starting on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.input:
        try:
            chat_content = read_chat_file(args.input)
            print("📝 Generating summary...")
            summary = summarize_chat(chat_content, args.model)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(summary)
                print(f"✅ Summary saved to {args.output}")
            else:
                print("\n" + "="*50)
                print("SUMMARY:")
                print("="*50)
                print(summary)
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

