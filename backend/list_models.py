"""
Script para listar todos los modelos disponibles de Gemini
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

if not api_key:
    print("❌ GEMINI_API_KEY no encontrada")
    exit(1)

print("🔍 Listando modelos disponibles de Gemini...\n")

genai.configure(api_key=api_key)

models = genai.list_models()

print("Modelos disponibles:")
print("="*60)

for model in models:
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Descripción: {model.display_name}")
        print(f"   Métodos: {', '.join(model.supported_generation_methods)}")
        print()
