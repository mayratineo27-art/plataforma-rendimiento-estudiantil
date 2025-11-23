# test_registro_backend.py
# Script para probar directamente el endpoint de registro

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_health():
    """Verificar que el backend está corriendo"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        print(f"✅ Backend responde: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Backend no responde: {e}")
        return False

def test_registro():
    """Probar el endpoint de registro"""
    print("\n" + "="*50)
    print("PROBANDO REGISTRO DE USUARIO")
    print("="*50)
    
    # Datos de prueba
    usuario = {
        "nombre": "Test Usuario",
        "email": f"test.{int(datetime.now().timestamp())}@universidad.edu",
        "password": "TestPassword123!",
        "carrera": "Ingeniería de Sistemas"  # Ajusta según tu esquema
    }
    
    print(f"\n📤 Enviando datos:")
    print(json.dumps(usuario, indent=2))
    
    try:
        # Intentar POST al endpoint de registro
        response = requests.post(
            f"{BASE_URL}/api/auth/register",  # Ajusta la ruta si es diferente
            json=usuario,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"\n📥 Respuesta del servidor:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        try:
            data = response.json()
            print(f"Body: {json.dumps(data, indent=2)}")
        except:
            print(f"Body (text): {response.text}")
        
        # Verificar resultado
        if response.status_code == 200 or response.status_code == 201:
            print("\n✅ Registro exitoso según HTTP status")
            return True
        else:
            print(f"\n⚠️ Registro falló con status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error de conexión: {e}")
        return False

def test_login(email, password):
    """Probar el endpoint de login"""
    print("\n" + "="*50)
    print("PROBANDO LOGIN")
    print("="*50)
    
    datos_login = {
        "email": email,
        "password": password
    }
    
    print(f"\n📤 Intentando login con: {email}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",  # Ajusta la ruta si es diferente
            json=datos_login,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"\n📥 Respuesta:")
        print(f"Status Code: {response.status_code}")
        
        try:
            data = response.json()
            print(f"Body: {json.dumps(data, indent=2)}")
            
            if 'user_id' in data:
                print(f"\n⚠️ PROBLEMA DETECTADO: user_id = {data['user_id']}")
                if data['user_id'] == 1:
                    print("❌ Siempre retorna user_id=1 (test@test.com)")
                    print("Esto indica que el backend NO está autenticando correctamente")
        except:
            print(f"Body (text): {response.text}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verificar_base_datos():
    """Verificar conexión a MySQL"""
    print("\n" + "="*50)
    print("VERIFICANDO BASE DE DATOS")
    print("="*50)
    
    try:
        import mysql.connector
        
        # Ajusta estos valores según tu configuración
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # Ajusta
            password='',  # Ajusta
            database='plataforma_rendimiento'  # Ajusta
        )
        
        cursor = conn.cursor()
        
        # Contar usuarios
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"✅ Conexión exitosa a MySQL")
        print(f"📊 Total de usuarios en DB: {count}")
        
        # Mostrar últimos 3 usuarios
        cursor.execute("SELECT id, email, nombre, created_at FROM users ORDER BY id DESC LIMIT 3")
        users = cursor.fetchall()
        
        print("\n📋 Últimos 3 usuarios registrados:")
        for user in users:
            print(f"  ID: {user[0]} | Email: {user[1]} | Nombre: {user[2]} | Creado: {user[3]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except ImportError:
        print("⚠️ mysql-connector-python no instalado")
        print("Instala con: pip install mysql-connector-python")
        return False
    except Exception as e:
        print(f"❌ Error de conexión a MySQL: {e}")
        return False

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO DEL SISTEMA DE AUTENTICACIÓN\n")
    
    # 1. Verificar backend
    if not test_health():
        print("\n❌ El backend no está corriendo. Inicia el servidor Flask primero.")
        exit(1)
    
    # 2. Verificar base de datos
    verificar_base_datos()
    
    # 3. Probar registro
    if test_registro():
        print("\n✅ El endpoint de registro responde")
    else:
        print("\n❌ El endpoint de registro tiene problemas")
    
    # 4. Probar login con test@test.com
    test_login("test@test.com", "password123")
    
    print("\n" + "="*50)
    print("RESUMEN DE DIAGNÓSTICO")
    print("="*50)
    print("1. Revisa los logs arriba para identificar el problema")
    print("2. Verifica que los datos se están guardando en MySQL")
    print("3. Verifica que el login no siempre retorna user_id=1")
    print("="*50)
