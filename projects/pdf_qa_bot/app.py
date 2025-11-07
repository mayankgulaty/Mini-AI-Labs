#!/usr/bin/env python3
"""
PDF Q&A Bot - Answers questions about PDF documents
"""

import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
from pdfminer.high_level import extract_text

load_dotenv()

class PDFQABot:
    def __init__(self):
        """Initialize the PDF Q&A bot."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key)

    def extract_text(self, pdf_path: str) -> str:
        """Extract text from PDF."""
        try:
            text = extract_text(pdf_path)
            if not text.strip():
                raise ValueError("No text could be extracted from the PDF")
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {e}")

    def answer_question(self, pdf_text: str, question: str) -> str:
        """Answer a question about the PDF content."""
        # Truncate text if too long (to fit in context window)
        max_chars = 12000
        if len(pdf_text) > max_chars:
            pdf_text = pdf_text[:max_chars] + "... [truncated]"
        
        prompt = f"""Based on the following document content, answer the question. If the answer is not in the document, say so.

Document Content:
{pdf_text}

Question: {question}

Answer:"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided documents."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description="Answer questions about PDF documents")
    parser.add_argument("--pdf", "-p", type=str, help="PDF file path")
    parser.add_argument("--question", "-q", type=str, help="Question to ask")
    parser.add_argument("--web", action="store_true", help="Run as web server")
    
    args = parser.parse_args()
    
    if args.web:
        from flask import Flask, request, render_template_string, send_file
        import werkzeug
        
        app = Flask(__name__)
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
        bot = PDFQABot()
        
        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>PDF Q&A Bot</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; }
                input, textarea { width: 100%; padding: 10px; margin: 5px 0; }
                button { padding: 12px 24px; background: #007bff; color: white; border: none; cursor: pointer; }
                .result { margin-top: 20px; padding: 20px; background: #f8f9fa; border-radius: 5px; }
            </style>
        </head>
        <body>
            <h1>📄 PDF Q&A Bot</h1>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="pdf" accept=".pdf" required>
                <textarea name="question" placeholder="Ask a question about the PDF..." required></textarea>
                <button type="submit">Get Answer</button>
            </form>
            {% if answer %}
            <div class="result">
                <strong>Answer:</strong><br>{{ answer }}
            </div>
            {% endif %}
        </body>
        </html>
        """
        
        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                if 'pdf' not in request.files:
                    return render_template_string(HTML_TEMPLATE, error="No PDF file provided")
                
                file = request.files['pdf']
                question = request.form.get('question', '').strip()
                
                if not question:
                    return render_template_string(HTML_TEMPLATE, error="Question is required")
                
                try:
                    temp_path = f"/tmp/{file.filename}"
                    file.save(temp_path)
                    pdf_text = bot.extract_text(temp_path)
                    answer = bot.answer_question(pdf_text, question)
                    os.remove(temp_path)
                    return render_template_string(HTML_TEMPLATE, answer=answer)
                except Exception as e:
                    return render_template_string(HTML_TEMPLATE, error=str(e))
            return render_template_string(HTML_TEMPLATE)
        
        print("🌐 Web server starting on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.pdf and args.question:
        if not os.path.exists(args.pdf):
            print(f"❌ Error: PDF file not found: {args.pdf}")
            return 1
        
        try:
            bot = PDFQABot()
            print("📄 Extracting text from PDF...")
            pdf_text = bot.extract_text(args.pdf)
            print(f"❓ Answering question: {args.question}")
            answer = bot.answer_question(pdf_text, args.question)
            
            print("\n" + "="*50)
            print("ANSWER:")
            print("="*50)
            print(answer)
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

