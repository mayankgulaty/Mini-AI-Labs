#!/usr/bin/env python3
"""
Recipe Generator - Generates personalized recipes using AI
"""

import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class RecipeGenerator:
    def __init__(self):
        """Initialize the recipe generator."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        self.client = OpenAI(api_key=api_key)

    def generate(self, ingredients: str, cuisine: str = "any", 
                dietary: str = "", servings: int = 4) -> str:
        """Generate a recipe."""
        prompt = f"""Create a detailed recipe with the following requirements:
- Ingredients available: {ingredients}
- Cuisine type: {cuisine}
- Dietary restrictions: {dietary or 'None'}
- Servings: {servings}

Include:
1. Recipe name
2. Ingredients list with quantities
3. Step-by-step cooking instructions
4. Cooking time
5. Difficulty level
6. Optional: Nutritional information"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert chef and recipe creator. Create detailed, practical recipes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        
        return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser(description="Generate personalized recipes")
    parser.add_argument("--ingredients", "-i", type=str, help="Available ingredients (comma-separated)")
    parser.add_argument("--cuisine", "-c", type=str, default="any", help="Cuisine type")
    parser.add_argument("--dietary", "-d", type=str, default="", help="Dietary restrictions")
    parser.add_argument("--servings", "-s", type=int, default=4, help="Number of servings")
    parser.add_argument("--web", action="store_true", help="Run as web server")
    
    args = parser.parse_args()
    
    if args.web:
        from flask import Flask, request, render_template_string
        
        app = Flask(__name__)
        generator = RecipeGenerator()
        
        HTML_TEMPLATE = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Recipe Generator</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; }
                input, textarea, select { width: 100%; padding: 10px; margin: 5px 0; }
                button { padding: 12px 24px; background: #28a745; color: white; border: none; cursor: pointer; }
                .result { margin-top: 20px; padding: 20px; background: #f8f9fa; border-radius: 5px; white-space: pre-wrap; }
            </style>
        </head>
        <body>
            <h1>🍳 Recipe Generator</h1>
            <form method="POST">
                <input type="text" name="ingredients" placeholder="Ingredients (comma-separated)" required>
                <select name="cuisine">
                    <option value="any">Any Cuisine</option>
                    <option value="italian">Italian</option>
                    <option value="chinese">Chinese</option>
                    <option value="mexican">Mexican</option>
                    <option value="indian">Indian</option>
                    <option value="french">French</option>
                </select>
                <input type="text" name="dietary" placeholder="Dietary restrictions (optional)">
                <input type="number" name="servings" value="4" min="1" placeholder="Servings">
                <button type="submit">Generate Recipe</button>
            </form>
            {% if recipe %}
            <div class="result">{{ recipe }}</div>
            {% endif %}
        </body>
        </html>
        """
        
        @app.route('/', methods=['GET', 'POST'])
        def index():
            if request.method == 'POST':
                ingredients = request.form.get('ingredients', '')
                cuisine = request.form.get('cuisine', 'any')
                dietary = request.form.get('dietary', '')
                servings = int(request.form.get('servings', 4))
                try:
                    recipe = generator.generate(ingredients, cuisine, dietary, servings)
                    return render_template_string(HTML_TEMPLATE, recipe=recipe)
                except Exception as e:
                    return render_template_string(HTML_TEMPLATE, error=str(e))
            return render_template_string(HTML_TEMPLATE)
        
        print("🌐 Web server starting on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif args.ingredients:
        try:
            generator = RecipeGenerator()
            recipe = generator.generate(args.ingredients, args.cuisine, args.dietary, args.servings)
            print("\n" + "="*50)
            print("GENERATED RECIPE:")
            print("="*50)
            print(recipe)
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

