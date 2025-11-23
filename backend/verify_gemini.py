"""
Script para verificar la configuración de Gemini API
Ejecutar: python backend/verify_gemini.py
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("="*60)
print("🔍 VERIFICACIÓN DE CONFIGURACIÓN GEMINI API")
print("="*60)

# 1. Verificar que existe la variable
gemini_key = os.getenv('GEMINI_API_KEY')

if not gemini_key:
    print("\n❌ ERROR: GEMINI_API_KEY no encontrada en .env")
    print("\n📝 Solución:")
    print("1. Abre el archivo backend/.env")
    print("2. Agrega o verifica la línea:")
    print("   GEMINI_API_KEY=tu_api_key_aqui")
    print("3. Obtén una API key en: https://aistudio.google.com/app/apikey")
    sys.exit(1)

print(f"\n✅ GEMINI_API_KEY encontrada: {gemini_key[:15]}...{gemini_key[-5:]}")

# 2. Verificar otras configuraciones
gemini_model = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
gemini_tokens = os.getenv('GEMINI_MAX_TOKENS', '8192')
gemini_temp = os.getenv('GEMINI_TEMPERATURE', '0.7')

print(f"✅ GEMINI_MODEL: {gemini_model}")
print(f"✅ GEMINI_MAX_TOKENS: {gemini_tokens}")
print(f"✅ GEMINI_TEMPERATURE: {gemini_temp}")

# 3. Intentar conectar con la API
print("\n🔄 Probando conexión con Gemini API...")

try:
    import google.generativeai as genai
    print("✅ Módulo google.generativeai importado")
    
    # Configurar API
    genai.configure(api_key=gemini_key)
    print("✅ API Key configurada")
    
    # Crear modelo
    model = genai.GenerativeModel(gemini_model)
    print(f"✅ Modelo '{gemini_model}' inicializado")
    
    # Hacer una prueba simple
    print("\n🧪 Enviando petición de prueba...")
    response = model.generate_content("Di solo 'OK' si funciona")
    
    print(f"✅ Respuesta recibida: {response.text[:50]}")
    
    print("\n" + "="*60)
    print("🎉 ¡TODO FUNCIONA CORRECTAMENTE!")
    print("="*60)
    print("\n✨ Gemini API está lista para usar en:")
    print("   - Generación de mapas mentales")
    print("   - Creación de resúmenes")
    print("   - Procesamiento de sílabos")
    
except ImportError:
    print("\n❌ ERROR: Módulo 'google-generativeai' no instalado")
    print("\n📝 Solución:")
    print("   pip install google-generativeai")
    sys.exit(1)
    
except Exception as e:
    print(f"\n❌ ERROR al conectar con Gemini API:")
    print(f"   {str(e)}")
    print("\n📝 Posibles causas:")
    print("   1. API Key inválida o expirada")
    print("   2. Límite de uso excedido")
    print("   3. Problemas de conexión a internet")
    print("\n💡 Soluciones:")
    print("   1. Verifica tu API key en: https://aistudio.google.com/app/apikey")
    print("   2. Genera una nueva API key si es necesario")
    print("   3. Actualiza GEMINI_API_KEY en el archivo .env")
    sys.exit(1)
