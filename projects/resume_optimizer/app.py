#!/usr/bin/env python3
"""
Resume Optimizer - Analyzes and optimizes resumes for specific job roles
"""

import argparse
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pdfminer.high_level import extract_text

# Load environment variables
load_dotenv()


class ResumeOptimizer:
    def __init__(self):
        """Initialize the Resume Optimizer with LangChain."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set. Please set it in your environment or .env file.")
        
        self.llm = ChatOpenAI(temperature=0.7)
        
        # Create prompt template for resume optimization
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are an expert resume writer and career coach."),
            ("user", """Analyze the following resume and optimize it for the job role: {job_role}

Job Description (if provided): {job_description}

Current Resume:
{resume_text}

Please provide:
1. An analysis of the resume's strengths and weaknesses for this role
2. An optimized version of the resume that:
   - Highlights relevant skills and experiences
   - Uses keywords from the job description
   - Improves clarity and impact
   - Maintains authenticity

Format your response as:
ANALYSIS:
[Your analysis]

OPTIMIZED RESUME:
[Optimized resume content]""")
        ])

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from a PDF file."""
        try:
            text = extract_text(pdf_path)
            if not text.strip():
                raise ValueError("No text could be extracted from the PDF")
            return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {e}")

    def optimize_resume(self, resume_text: str, job_role: str, job_description: str = "") -> str:
        """Optimize the resume for the given job role."""
        try:
            chain = self.prompt_template | self.llm
            result = chain.invoke({
                "resume_text": resume_text,
                "job_role": job_role,
                "job_description": job_description or "Not provided"
            })
            return result.content if hasattr(result, 'content') else str(result)
        except Exception as e:
            raise Exception(f"Error optimizing resume: {e}")


def main():
    parser = argparse.ArgumentParser(description="Optimize resumes for specific job roles")
    parser.add_argument("--resume", "-r", type=str, help="Path to resume PDF file")
    parser.add_argument("--job", "-j", type=str, help="Target job role")
    parser.add_argument("--description", "-d", type=str, default="", help="Job description (optional)")
    parser.add_argument("--output", "-o", type=str, help="Output file path (optional)")
    parser.add_argument("--web", action="store_true", help="Run as web server")
    
    args = parser.parse_args()
    
    if args.web:
        from flask import Flask, request, render_template_string, jsonify
        import werkzeug
        
        app = Flask(__name__)
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
        
        optimizer = ResumeOptimizer()
        
        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Resume Optimizer</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 1000px; margin: 50px auto; padding: 20px; }
                form { display: flex; flex-direction: column; gap: 15px; }
                input, textarea { padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
                input[type="file"] { padding: 5px; }
                button { padding: 12px 24px; background: #007bff; color: white; border: none; cursor: pointer; }
                button:hover { background: #0056b3; }
                .result { margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 5px; white-space: pre-wrap; }
                .section { margin: 20px 0; padding: 15px; background: white; border-left: 4px solid #007bff; }
            </style>
        </head>
        <body>
            <h1>📄 Resume Optimizer</h1>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="resume" accept=".pdf" required>
                <input type="text" name="job_role" placeholder="Target Job Role (e.g., Software Engineer)" required>
                <textarea name="job_description" placeholder="Job Description (optional)" rows="5"></textarea>
                <button type="submit">Optimize Resume</button>
            </form>
            {% if result %}
            <div class="result">
                {{ result }}
            </div>
            {% endif %}
            {% if error %}
            <div class="result" style="background: #f8d7da; color: #721c24;">
                <strong>Error:</strong> {{ error }}
            </div>
            {% endif %}
        </body>
        </html>
        """
        
        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                if 'resume' not in request.files:
                    return render_template_string(HTML_TEMPLATE, error="No resume file provided")
                
                file = request.files['resume']
                job_role = request.form.get('job_role', '').strip()
                job_description = request.form.get('job_description', '').strip()
                
                if not job_role:
                    return render_template_string(HTML_TEMPLATE, error="Job role is required")
                
                if file.filename == '':
                    return render_template_string(HTML_TEMPLATE, error="No file selected")
                
                try:
                    # Save uploaded file temporarily
                    temp_path = f"/tmp/{file.filename}"
                    file.save(temp_path)
                    
                    # Extract text from PDF
                    resume_text = optimizer.extract_text_from_pdf(temp_path)
                    
                    # Optimize resume
                    result = optimizer.optimize_resume(resume_text, job_role, job_description)
                    
                    # Clean up
                    os.remove(temp_path)
                    
                    return render_template_string(HTML_TEMPLATE, result=result)
                except Exception as e:
                    return render_template_string(HTML_TEMPLATE, error=str(e))
            
            return render_template_string(HTML_TEMPLATE)
        
        print("🌐 Web server starting on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.resume and args.job:
        if not os.path.exists(args.resume):
            print(f"❌ Error: Resume file not found: {args.resume}")
            return 1
        
        try:
            optimizer = ResumeOptimizer()
            
            print("📄 Extracting text from resume...")
            resume_text = optimizer.extract_text_from_pdf(args.resume)
            
            print(f"🔧 Optimizing resume for: {args.job}")
            result = optimizer.optimize_resume(resume_text, args.job, args.description)
            
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"✅ Optimized resume saved to {args.output}")
            else:
                print("\n" + "="*50)
                print("OPTIMIZED RESUME:")
                print("="*50)
                print(result)
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

