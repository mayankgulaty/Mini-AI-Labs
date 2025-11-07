#!/usr/bin/env python3
"""
Text to Speech Converter - Converts text to natural-sounding speech
"""

import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class TextToSpeech:
    def __init__(self):
        """Initialize the TTS converter."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key)
        self.available_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    def convert(self, text: str, voice: str = "alloy", output_path: str = "output.mp3") -> str:
        """Convert text to speech."""
        if voice not in self.available_voices:
            raise ValueError(f"Voice must be one of: {', '.join(self.available_voices)}")
        
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        response.stream_to_file(output_path)
        return output_path


def main():
    parser = argparse.ArgumentParser(description="Convert text to speech")
    parser.add_argument("--text", "-t", type=str, help="Text to convert")
    parser.add_argument("--voice", "-v", type=str, default="alloy", 
                       help=f"Voice option: {', '.join(['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'])}")
    parser.add_argument("--output", "-o", type=str, default="output.mp3", help="Output file path")
    parser.add_argument("--web", action="store_true", help="Run as web server")
    
    args = parser.parse_args()
    
    if args.web:
        from flask import Flask, request, render_template_string, send_file
        
        app = Flask(__name__)
        tts = TextToSpeech()
        
        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Text to Speech Converter</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                textarea { width: 100%; height: 200px; margin: 10px 0; }
                select, button { padding: 10px; margin: 5px; }
                button { background: #007bff; color: white; border: none; cursor: pointer; }
            </style>
        </head>
        <body>
            <h1>🔊 Text to Speech Converter</h1>
            <form method="POST">
                <textarea name="text" placeholder="Enter text to convert..." required></textarea>
                <select name="voice">
                    <option value="alloy">Alloy</option>
                    <option value="echo">Echo</option>
                    <option value="fable">Fable</option>
                    <option value="onyx">Onyx</option>
                    <option value="nova">Nova</option>
                    <option value="shimmer">Shimmer</option>
                </select>
                <button type="submit">Convert to Speech</button>
            </form>
        </body>
        </html>
        """
        
        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                text = request.form.get('text', '')
                voice = request.form.get('voice', 'alloy')
                try:
                    output_path = tts.convert(text, voice, f"/tmp/output_{voice}.mp3")
                    return send_file(output_path, as_attachment=True, download_name="speech.mp3")
                except Exception as e:
                    return render_template_string(HTML_TEMPLATE + f"<p style='color:red;'>Error: {e}</p>")
            return render_template_string(HTML_TEMPLATE)
        
        print("🌐 Web server starting on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.text:
        try:
            tts = TextToSpeech()
            print(f"🔊 Converting text to speech...")
            output = tts.convert(args.text, args.voice, args.output)
            print(f"✅ Audio saved to {output}")
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

