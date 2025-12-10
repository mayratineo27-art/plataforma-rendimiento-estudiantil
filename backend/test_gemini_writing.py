"""
Prueba rápida de la API de Gemini para evaluación de escritura
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import google.generativeai as genai
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_gemini_api():
    """Prueba la conexión con Gemini"""
    print("=" * 60)
    print("🧪 PRUEBA DE GEMINI API PARA EVALUACIÓN DE ESCRITURA")
    print("=" * 60)
    
    # 1. Verificar API Key
    api_key = os.getenv('GEMINI_API_KEY')
    print(f"\n1️⃣ API Key configurada: {'✅ Sí' if api_key else '❌ No'}")
    if not api_key:
        print("   ❌ ERROR: GEMINI_API_KEY no encontrada en .env")
        return False
    
    print(f"   Key: {api_key[:20]}...{api_key[-10:]}")
    
    # 2. Configurar Gemini
    try:
        print("\n2️⃣ Configurando Gemini...")
        genai.configure(api_key=api_key)
        print("   ✅ Configuración exitosa")
    except Exception as e:
        print(f"   ❌ Error configurando: {e}")
        return False
    
    # 3. Obtener modelo
    try:
        print("\n3️⃣ Obteniendo modelo...")
        model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
        print(f"   Modelo solicitado: {model_name}")
        
        model = genai.GenerativeModel(model_name)
        print(f"   ✅ Modelo obtenido: {model_name}")
    except Exception as e:
        print(f"   ⚠️ Error con {model_name}: {e}")
        print("   Intentando con modelo alternativo...")
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            print("   ✅ Modelo alternativo: gemini-1.5-flash")
        except Exception as e2:
            print(f"   ❌ Error con modelo alternativo: {e2}")
            return False
    
    # 4. Prueba simple de generación
    try:
        print("\n4️⃣ Probando generación de contenido...")
        test_text = """
Este es un ejemplo de texto para evaluar. El estudiante escribio este parrafo 
como parte de un ensayo. Hay algunos errores de ortografia y gramática que 
necesitan ser corregidos. La estructura del texto es simple pero funcional.
"""
        
        prompt = f"""
Analiza el siguiente texto y proporciona:
1. Score general (0-100)
2. Un error específico que encuentres
3. Una sugerencia de mejora

Texto: {test_text}

Responde en formato JSON simple:
{{"score": 75, "error": "descripción", "sugerencia": "descripción"}}
"""
        
        print("   Enviando petición...")
        response = model.generate_content(prompt)
        print("   ✅ Respuesta recibida")
        print(f"\n   Respuesta:\n   {response.text[:200]}...")
        
    except Exception as e:
        print(f"   ❌ Error generando contenido: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        
        # Verificar si es error de cuota
        if "quota" in str(e).lower() or "resource_exhausted" in str(e).lower():
            print("\n   ⚠️⚠️⚠️  ERROR DE CUOTA  ⚠️⚠️⚠️")
            print("   La API Key ha excedido su límite de uso gratuito")
            print("   Soluciones:")
            print("   1. Esperar hasta que se reinicie la cuota (generalmente diaria)")
            print("   2. Usar otra API Key")
            print("   3. Habilitar facturación en Google Cloud")
        
        return False
    
    print("\n" + "=" * 60)
    print("✅ GEMINI API FUNCIONANDO CORRECTAMENTE")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success = test_gemini_api()
    if not success:
        print("\n❌ La API de Gemini NO está funcionando")
        print("El sistema usará evaluación de fallback (limitada)")
    sys.exit(0 if success else 1)
