"""
Script para configurar MySQL y crear archivo .env
"""

import os
from pathlib import Path
import getpass

def create_env_file():
    """Crea el archivo .env con configuración interactiva"""
    print("="*80)
    print("CONFIGURACIÓN DEL ARCHIVO .ENV")
    print("="*80)
    print()
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Error: No existe la carpeta backend")
        return False
    
    env_file = backend_dir / ".env"
    
    # Si ya existe, preguntar si sobrescribir
    if env_file.exists():
        print("⚠️ El archivo .env ya existe")
        respuesta = input("¿Deseas sobrescribirlo? (s/n): ").strip().lower()
        if respuesta != 's':
            print("❌ Operación cancelada")
            return False
        
        # Hacer backup
        backup_file = backend_dir / ".env.backup"
        print(f"📋 Creando backup: {backup_file}")
        with open(env_file, 'r') as f:
            with open(backup_file, 'w') as bf:
                bf.write(f.read())
    
    print()
    print("Configura las variables de entorno:")
    print("(Presiona Enter para usar el valor por defecto)")
    print()
    
    # Recopilar información
    secret_key = input("SECRET_KEY [generado automáticamente]: ").strip()
    if not secret_key:
        import secrets
        secret_key = secrets.token_hex(32)
        print(f"  → Usando: {secret_key[:20]}...")
    
    db_user = input("Usuario MySQL [root]: ").strip() or "root"
    db_password = getpass.getpass("Contraseña MySQL [password]: ") or "password"
    db_host = input("Host MySQL [localhost]: ").strip() or "localhost"
    db_port = input("Puerto MySQL [3306]: ").strip() or "3306"
    db_name = input("Nombre de BD [plataforma_estudiantil]: ").strip() or "plataforma_estudiantil"
    
    print()
    gemini_key = input("API Key de Gemini (opcional, presiona Enter para omitir): ").strip()
    if not gemini_key:
        gemini_key = "your-gemini-api-key-here"
        print("  ⚠️ Recuerda configurar tu API Key de Gemini después")
    
    # Construir DATABASE_URL
    database_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    # Crear contenido del .env
    env_content = f"""# Configuración de la aplicación
SECRET_KEY={secret_key}
FLASK_DEBUG=True
PORT=5000

# Base de datos
DATABASE_URL={database_url}

# API Keys
GEMINI_API_KEY={gemini_key}
OPENAI_API_KEY=your-openai-api-key-here

# Configuración de archivos
MAX_FILE_SIZE=100
ALLOWED_EXTENSIONS=pdf,docx,doc,txt

# Configuración de video/audio
MAX_VIDEO_LENGTH=3600
MAX_AUDIO_LENGTH=3600
"""
    
    # Escribir archivo
    print()
    print(f"✏️ Creando archivo: {env_file}")
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Archivo .env creado exitosamente")
    print()
    print("Configuración guardada:")
    print(f"  • Usuario MySQL: {db_user}")
    print(f"  • Host: {db_host}:{db_port}")
    print(f"  • Base de datos: {db_name}")
    print(f"  • Gemini API Key: {'Configurada' if gemini_key != 'your-gemini-api-key-here' else 'Pendiente'}")
    print()
    
    return True

def test_mysql_connection():
    """Intenta conectarse a MySQL con las credenciales proporcionadas"""
    print("="*80)
    print("VERIFICANDO CONEXIÓN A MYSQL")
    print("="*80)
    print()
    
    try:
        import mysql.connector
        print("✅ mysql-connector-python está instalado")
    except ImportError:
        print("❌ mysql-connector-python NO está instalado")
        print("   Instálalo con: pip install mysql-connector-python")
        return False
    
    # Leer configuración del .env
    env_file = Path("backend/.env")
    if not env_file.exists():
        print("❌ Archivo .env no existe")
        print("   Ejecuta primero la configuración del .env")
        return False
    
    # Extraer credenciales (simplificado)
    db_config = {}
    with open(env_file, 'r') as f:
        for line in f:
            if line.startswith('DATABASE_URL='):
                url = line.split('=', 1)[1].strip()
                # Parsear URL: mysql+mysqlconnector://user:pass@host:port/db
                try:
                    # Remover protocolo
                    url = url.replace('mysql+mysqlconnector://', '')
                    # Extraer user:pass
                    auth, rest = url.split('@')
                    user, password = auth.split(':')
                    # Extraer host:port/db
                    host_port, db = rest.split('/')
                    if ':' in host_port:
                        host, port = host_port.split(':')
                    else:
                        host = host_port
                        port = '3306'
                    
                    db_config = {
                        'user': user,
                        'password': password,
                        'host': host,
                        'port': int(port),
                        'database': db
                    }
                except Exception as e:
                    print(f"❌ Error al parsear DATABASE_URL: {e}")
                    return False
    
    if not db_config:
        print("❌ No se pudo extraer configuración de MySQL")
        return False
    
    print(f"Intentando conectar a MySQL:")
    print(f"  • Usuario: {db_config['user']}")
    print(f"  • Host: {db_config['host']}:{db_config['port']}")
    print(f"  • Base de datos: {db_config['database']}")
    print()
    
    try:
        # Intentar conexión sin especificar base de datos
        connection = mysql.connector.connect(
            user=db_config['user'],
            password=db_config['password'],
            host=db_config['host'],
            port=db_config['port']
        )
        print("✅ Conexión a MySQL exitosa")
        
        # Verificar si la base de datos existe
        cursor = connection.cursor()
        cursor.execute(f"SHOW DATABASES LIKE '{db_config['database']}'")
        result = cursor.fetchone()
        
        if result:
            print(f"✅ Base de datos '{db_config['database']}' existe")
        else:
            print(f"⚠️ Base de datos '{db_config['database']}' NO existe")
            print()
            respuesta = input("¿Deseas crearla ahora? (s/n): ").strip().lower()
            if respuesta == 's':
                cursor.execute(f"CREATE DATABASE {db_config['database']}")
                print(f"✅ Base de datos '{db_config['database']}' creada exitosamente")
            else:
                print("❌ Necesitas crear la base de datos manualmente:")
                print(f"   mysql -u {db_config['user']} -p")
                print(f"   CREATE DATABASE {db_config['database']};")
        
        cursor.close()
        connection.close()
        return True
        
    except mysql.connector.Error as err:
        print(f"❌ Error de conexión a MySQL: {err}")
        print()
        print("Soluciones:")
        print("  1. Verifica que MySQL esté corriendo:")
        print("     Windows: Servicios → MySQL")
        print("     Linux: sudo systemctl status mysql")
        print("  2. Verifica usuario y contraseña")
        print("  3. Verifica que el puerto 3306 esté disponible")
        return False

def main():
    """Función principal"""
    print()
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║        CONFIGURACIÓN DE MYSQL Y ARCHIVO .ENV                  ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    print()
    
    # Paso 1: Crear .env
    print("PASO 1: Crear archivo .env")
    print("-" * 80)
    if not create_env_file():
        print("❌ No se pudo crear el archivo .env")
        return
    
    print()
    input("Presiona Enter para continuar con la verificación de MySQL...")
    print()
    
    # Paso 2: Verificar MySQL
    print("PASO 2: Verificar conexión a MySQL")
    print("-" * 80)
    if test_mysql_connection():
        print()
        print("="*80)
        print("✅ ¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!")
        print("="*80)
        print()
        print("Próximos pasos:")
        print("  1. Verifica que todas las dependencias estén instaladas")
        print("  2. Ejecuta los tests: python test_backend_diagnostics.py")
        print("  3. Inicia el servidor: cd backend && python run.py")
        print()
    else:
        print()
        print("="*80)
        print("⚠️ CONFIGURACIÓN PARCIALMENTE COMPLETADA")
        print("="*80)
        print()
        print("El archivo .env fue creado, pero hay problemas con MySQL.")
        print("Revisa los mensajes de error arriba y soluciónalos antes de continuar.")
        print()

if __name__ == "__main__":
    main()
