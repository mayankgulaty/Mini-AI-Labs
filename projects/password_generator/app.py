#!/usr/bin/env python3
"""
Password Generator - Generates secure passwords with strength analysis
"""

import argparse
import secrets
import string
import re
from typing import Tuple

class PasswordGenerator:
    def __init__(self):
        """Initialize the password generator."""
        pass

    def generate(self, length: int = 12, include_uppercase: bool = True,
                 include_lowercase: bool = True, include_numbers: bool = True,
                 include_symbols: bool = False) -> str:
        """Generate a secure password."""
        chars = ""
        if include_lowercase:
            chars += string.ascii_lowercase
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_numbers:
            chars += string.digits
        if include_symbols:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not chars:
            raise ValueError("At least one character set must be enabled")
        
        return ''.join(secrets.choice(chars) for _ in range(length))

    def analyze_strength(self, password: str) -> Tuple[str, dict]:
        """Analyze password strength."""
        score = 0
        feedback = []
        
        length = len(password)
        if length >= 12:
            score += 2
        elif length >= 8:
            score += 1
        else:
            feedback.append("Password is too short (recommend at least 12 characters)")
        
        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Add lowercase letters")
        
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Add uppercase letters")
        
        if re.search(r'\d', password):
            score += 1
        else:
            feedback.append("Add numbers")
        
        if re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            score += 1
        else:
            feedback.append("Add special characters for better security")
        
        if len(set(password)) / len(password) > 0.7:
            score += 1
        else:
            feedback.append("Use more diverse characters")
        
        if score <= 2:
            strength = "Weak"
        elif score <= 4:
            strength = "Fair"
        elif score <= 5:
            strength = "Good"
        else:
            strength = "Strong"
        
        return strength, {"score": score, "feedback": feedback, "length": length}


def main():
    parser = argparse.ArgumentParser(description="Generate secure passwords")
    parser.add_argument("--length", "-l", type=int, default=12, help="Password length")
    parser.add_argument("--include-uppercase", action="store_true", default=True, help="Include uppercase letters")
    parser.add_argument("--include-lowercase", action="store_true", default=True, help="Include lowercase letters")
    parser.add_argument("--include-numbers", action="store_true", default=True, help="Include numbers")
    parser.add_argument("--include-symbols", action="store_true", help="Include symbols")
    parser.add_argument("--analyze", "-a", type=str, help="Analyze password strength")
    parser.add_argument("--web", action="store_true", help="Run as web server")
    
    args = parser.parse_args()
    
    if args.web:
        from flask import Flask, request, render_template_string
        
        app = Flask(__name__)
        generator = PasswordGenerator()
        
        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Password Generator</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                input, select { width: 100%; padding: 10px; margin: 5px 0; }
                button { padding: 12px 24px; background: #007bff; color: white; border: none; cursor: pointer; }
                .result { margin-top: 20px; padding: 20px; background: #f8f9fa; border-radius: 5px; }
                .strong { color: #28a745; }
                .good { color: #17a2b8; }
                .fair { color: #ffc107; }
                .weak { color: #dc3545; }
            </style>
        </head>
        <body>
            <h1>🔐 Password Generator</h1>
            <form method="POST">
                <input type="number" name="length" value="12" min="8" max="128" placeholder="Length">
                <label><input type="checkbox" name="uppercase" checked> Uppercase</label>
                <label><input type="checkbox" name="lowercase" checked> Lowercase</label>
                <label><input type="checkbox" name="numbers" checked> Numbers</label>
                <label><input type="checkbox" name="symbols"> Symbols</label>
                <button type="submit">Generate Password</button>
            </form>
            <hr>
            <h2>Analyze Password</h2>
            <form method="POST" action="/analyze">
                <input type="text" name="password" placeholder="Enter password to analyze">
                <button type="submit">Analyze</button>
            </form>
            {% if password %}
            <div class="result">
                <strong>Generated Password:</strong><br>
                <code style="font-size: 1.2em;">{{ password }}</code>
                {% if strength %}
                <p><strong>Strength:</strong> <span class="{{ strength.lower() }}">{{ strength }}</span></p>
                {% endif %}
            </div>
            {% endif %}
        </body>
        </html>
        """
        
        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                length = int(request.form.get('length', 12))
                uppercase = request.form.get('uppercase') == 'on'
                lowercase = request.form.get('lowercase') == 'on'
                numbers = request.form.get('numbers') == 'on'
                symbols = request.form.get('symbols') == 'on'
                try:
                    password = generator.generate(length, uppercase, lowercase, numbers, symbols)
                    strength, _ = generator.analyze_strength(password)
                    return render_template_string(HTML_TEMPLATE, password=password, strength=strength)
                except Exception as e:
                    return render_template_string(HTML_TEMPLATE, error=str(e))
            return render_template_string(HTML_TEMPLATE)
        
        @app.route('/analyze', methods=['POST'])
        def analyze():
            password = request.form.get('password', '')
            strength, analysis = generator.analyze_strength(password)
            return render_template_string(HTML_TEMPLATE, 
                                        password=password, 
                                        strength=strength,
                                        analysis=analysis)
        
        print("🌐 Web server starting on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.analyze:
        generator = PasswordGenerator()
        strength, analysis = generator.analyze_strength(args.analyze)
        print(f"\nPassword: {args.analyze}")
        print(f"Strength: {strength}")
        print(f"Score: {analysis['score']}/7")
        if analysis['feedback']:
            print("\nSuggestions:")
            for item in analysis['feedback']:
                print(f"  - {item}")
    else:
        try:
            generator = PasswordGenerator()
            password = generator.generate(
                args.length,
                args.include_uppercase,
                args.include_lowercase,
                args.include_numbers,
                args.include_symbols
            )
            strength, _ = generator.analyze_strength(password)
            print(f"\nGenerated Password: {password}")
            print(f"Strength: {strength}")
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

