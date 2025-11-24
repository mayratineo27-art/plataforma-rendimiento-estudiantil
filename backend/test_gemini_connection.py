"""
Test rápido de conexión con Gemini API
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()

def test_gemini_connection():
    """Prueba la conexión con Gemini API"""
    
    print("=" * 60)
    print("🧪 Test de Conexión con Gemini API")
    print("=" * 60)
    
    # 1. Verificar API Key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY no encontrada en .env")
        return False
    
    print(f"✅ API Key encontrada: {api_key[:10]}...{api_key[-4:]}")
    
    # 2. Configurar Gemini
    try:
        genai.configure(api_key=api_key)
        print("✅ Gemini configurado correctamente")
    except Exception as e:
        print(f"❌ Error configurando Gemini: {e}")
        return False
    
    # 3. Obtener modelo
    model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    print(f"📦 Intentando usar modelo: {model_name}")
    
    try:
        model = genai.GenerativeModel(model_name)
        print(f"✅ Modelo {model_name} cargado")
    except Exception as e:
        print(f"⚠️  Modelo {model_name} no disponible: {e}")
        print("   Intentando con modelos alternativos...")
        
        for alt_model in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']:
            try:
                model = genai.GenerativeModel(alt_model)
                print(f"✅ Modelo alternativo {alt_model} cargado")
                break
            except Exception as e2:
                print(f"   ❌ {alt_model} tampoco disponible: {e2}")
        else:
            print("❌ Ningún modelo de Gemini está disponible")
            return False
    
    # 4. Hacer una solicitud de prueba
    print("\n🔄 Haciendo solicitud de prueba...")
    try:
        response = model.generate_content("Di 'conexión exitosa' si recibes este mensaje")
        print(f"✅ Respuesta recibida: {response.text[:100]}")
        print("\n" + "=" * 60)
        print("✅ TODO FUNCIONA CORRECTAMENTE")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"❌ Error en solicitud de prueba: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        print("\n" + "=" * 60)
        print("❌ LA API DE GEMINI NO ESTÁ RESPONDIENDO")
        print("=" * 60)
        print("\nPosibles causas:")
        print("1. API Key inválida o expirada")
        print("2. Cuota de API excedida")
        print("3. Problemas de red/firewall")
        print("4. Servicio de Google temporalmente no disponible")
        return False

if __name__ == '__main__':
    test_gemini_connection()
