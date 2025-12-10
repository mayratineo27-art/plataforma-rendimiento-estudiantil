"""
Lista los modelos disponibles de Gemini
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY no configurada")
    sys.exit(1)

print(f"🔑 API Key: {api_key[:20]}...{api_key[-10:]}\n")

genai.configure(api_key=api_key)

print("📋 Modelos disponibles para generateContent:\n")
try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display: {model.display_name}")
            print(f"   Descripción: {model.description[:80]}...")
            print()
except Exception as e:
    print(f"❌ Error listando modelos: {e}")
