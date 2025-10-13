"""
list_models.py - Listar modelos disponibles de Gemini
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()

# Configurar API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY no está configurada")
    exit(1)

genai.configure(api_key=api_key)

print("\n" + "="*60)
print("📋 MODELOS DISPONIBLES EN TU API KEY")
print("="*60 + "\n")

try:
    # Listar todos los modelos
    for model in genai.list_models():
        # Solo mostrar modelos que soporten generateContent
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Descripción: {model.display_name}")
            print(f"   Métodos: {', '.join(model.supported_generation_methods)}")
            print()
    
    print("="*60)
    print("💡 Usa uno de estos nombres en tu .env")
    print("="*60)
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    print("\nPosibles causas:")
    print("1. API Key inválida")
    print("2. API Key sin permisos")
    print("3. Problema de conexión")