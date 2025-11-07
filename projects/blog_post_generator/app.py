#!/usr/bin/env python3
"""
Blog Post Generator - Generates well-structured blog posts
"""

import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class BlogPostGenerator:
    def __init__(self):
        """Initialize the blog post generator."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key)

    def generate(self, topic: str, length: str = "medium", 
                 style: str = "professional", keywords: str = "") -> str:
        """Generate a blog post."""
        length_map = {"short": "500-700 words", "medium": "1000-1500 words", "long": "2000+ words"}
        word_count = length_map.get(length, "1000-1500 words")
        
        prompt = f"""Write a comprehensive, well-structured blog post on the topic: "{topic}"

Requirements:
- Length: {word_count}
- Style: {style}
- Keywords to include: {keywords or 'None specified'}
- Include: Engaging title, introduction, well-structured body with headings, and conclusion
- Make it SEO-friendly and engaging
- Use proper markdown formatting

Generate the complete blog post:"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert blog writer and content creator. Write engaging, well-structured blog posts."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=2000
        )
        
        return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description="Generate blog posts")
    parser.add_argument("--topic", "-t", type=str, help="Blog post topic")
    parser.add_argument("--length", "-l", type=str, default="medium", 
                       choices=["short", "medium", "long"], help="Post length")
    parser.add_argument("--style", "-s", type=str, default="professional",
                       help="Writing style")
    parser.add_argument("--keywords", "-k", type=str, default="", help="SEO keywords (comma-separated)")
    parser.add_argument("--output", "-o", type=str, help="Output file (optional)")
    parser.add_argument("--web", action="store_true", help="Run as web server")
    
    args = parser.parse_args()
    
    if args.web:
        from flask import Flask, request, render_template_string
        
        app = Flask(__name__)
        generator = BlogPostGenerator()
        
        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Blog Post Generator</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 1000px; margin: 50px auto; padding: 20px; }
                input, textarea, select { width: 100%; padding: 10px; margin: 5px 0; }
                button { padding: 12px 24px; background: #28a745; color: white; border: none; cursor: pointer; }
                .result { margin-top: 20px; padding: 20px; background: #f8f9fa; border-radius: 5px; white-space: pre-wrap; }
            </style>
        </head>
        <body>
            <h1>✍️ Blog Post Generator</h1>
            <form method="POST">
                <input type="text" name="topic" placeholder="Blog post topic" required>
                <select name="length">
                    <option value="short">Short (500-700 words)</option>
                    <option value="medium" selected>Medium (1000-1500 words)</option>
                    <option value="long">Long (2000+ words)</option>
                </select>
                <select name="style">
                    <option value="professional">Professional</option>
                    <option value="casual">Casual</option>
                    <option value="academic">Academic</option>
                    <option value="conversational">Conversational</option>
                </select>
                <input type="text" name="keywords" placeholder="SEO keywords (optional, comma-separated)">
                <button type="submit">Generate Blog Post</button>
            </form>
            {% if post %}
            <div class="result">{{ post }}</div>
            {% endif %}
        </body>
        </html>
        """
        
        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                topic = request.form.get('topic', '')
                length = request.form.get('length', 'medium')
                style = request.form.get('style', 'professional')
                keywords = request.form.get('keywords', '')
                try:
                    post = generator.generate(topic, length, style, keywords)
                    return render_template_string(HTML_TEMPLATE, post=post)
                except Exception as e:
                    return render_template_string(HTML_TEMPLATE, error=str(e))
            return render_template_string(HTML_TEMPLATE)
        
        print("🌐 Web server starting on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.topic:
        try:
            generator = BlogPostGenerator()
            post = generator.generate(args.topic, args.length, args.style, args.keywords)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(post)
                print(f"✅ Blog post saved to {args.output}")
            else:
                print("\n" + "="*50)
                print("BLOG POST:")
                print("="*50)
                print(post)
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

