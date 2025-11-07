#!/usr/bin/env python3
"""
Meeting Notes Generator - Generates structured meeting notes from transcripts
"""

import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class MeetingNotesGenerator:
    def __init__(self):
        """Initialize the meeting notes generator."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key)

    def generate(self, transcript: str) -> str:
        """Generate structured meeting notes."""
        prompt = f"""Analyze the following meeting transcript and generate structured meeting notes.

Transcript:
{transcript}

Please provide:
1. Meeting Summary (2-3 sentences)
2. Key Points Discussed (bullet points)
3. Decisions Made (bullet points)
4. Action Items (with assignees if mentioned)
5. Next Steps

Format the output clearly with headers:"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert at summarizing meetings and extracting key information."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description="Generate meeting notes from transcripts")
    parser.add_argument("--transcript", "-t", type=str, help="Meeting transcript file")
    parser.add_argument("--output", "-o", type=str, help="Output file (optional)")
    parser.add_argument("--web", action="store_true", help="Run as web server")
    
    args = parser.parse_args()
    
    if args.web:
        from flask import Flask, request, render_template_string
        
        app = Flask(__name__)
        generator = MeetingNotesGenerator()
        
        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Meeting Notes Generator</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; }
                textarea { width: 100%; height: 300px; margin: 10px 0; }
                button { padding: 12px 24px; background: #007bff; color: white; border: none; cursor: pointer; }
                .result { margin-top: 20px; padding: 20px; background: #f8f9fa; border-radius: 5px; white-space: pre-wrap; }
            </style>
        </head>
        <body>
            <h1>📝 Meeting Notes Generator</h1>
            <form method="POST">
                <textarea name="transcript" placeholder="Paste meeting transcript here..." required></textarea>
                <button type="submit">Generate Notes</button>
            </form>
            {% if notes %}
            <div class="result">{{ notes }}</div>
            {% endif %}
        </body>
        </html>
        """
        
        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                transcript = request.form.get('transcript', '')
                try:
                    notes = generator.generate(transcript)
                    return render_template_string(HTML_TEMPLATE, notes=notes)
                except Exception as e:
                    return render_template_string(HTML_TEMPLATE, error=str(e))
            return render_template_string(HTML_TEMPLATE)
        
        print("🌐 Web server starting on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.transcript:
        try:
            with open(args.transcript, 'r', encoding='utf-8') as f:
                transcript = f.read()
            
            generator = MeetingNotesGenerator()
            notes = generator.generate(transcript)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(notes)
                print(f"✅ Notes saved to {args.output}")
            else:
                print("\n" + "="*50)
                print("MEETING NOTES:")
                print("="*50)
                print(notes)
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

