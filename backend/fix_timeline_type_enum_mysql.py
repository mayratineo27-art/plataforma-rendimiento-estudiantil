"""
Script para actualizar el ENUM timeline_type en MySQL
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

def fix_timeline_type_enum():
    """Actualiza el enum timeline_type en MySQL"""
    
    # Construir connection string para MySQL
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME', 'rendimiento_estudiantil')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', 'ADMIN')
    
    connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    print("=" * 60)
    print("🔧 Actualizando ENUM timeline_type en MySQL")
    print("=" * 60)
    print(f"Conectando a: {db_host}:{db_port}/{db_name}")
    
    try:
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            # Paso 1: Verificar el ENUM actual
            print("\n📋 Paso 1: Verificando ENUM actual...")
            result = conn.execute(text("""
                SELECT COLUMN_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = :db_name
                AND TABLE_NAME = 'timelines'
                AND COLUMN_NAME = 'timeline_type'
            """), {"db_name": db_name})
            
            col_type = result.fetchone()
            if col_type:
                print(f"  Tipo actual: {col_type[0]}")
            
            # Paso 2: Modificar el ENUM para incluir 'free'
            print("\n📋 Paso 2: Modificando ENUM...")
            print("  Agregando valor 'free' al ENUM timeline_type...")
            
            conn.execute(text("""
                ALTER TABLE timelines 
                MODIFY COLUMN timeline_type 
                ENUM('academic', 'course', 'project', 'free') 
                DEFAULT 'project'
            """))
            conn.commit()
            
            print("  ✅ ENUM modificado exitosamente")
            
            # Paso 3: Verificar el cambio
            print("\n📋 Paso 3: Verificando cambio...")
            result = conn.execute(text("""
                SELECT COLUMN_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = :db_name
                AND TABLE_NAME = 'timelines'
                AND COLUMN_NAME = 'timeline_type'
            """), {"db_name": db_name})
            
            col_type = result.fetchone()
            if col_type:
                print(f"  Tipo final: {col_type[0]}")
        
        print("\n" + "=" * 60)
        print("✅ ENUM timeline_type actualizado exitosamente")
        print("=" * 60)
        print("\nValores permitidos:")
        print("  - academic")
        print("  - course")
        print("  - project")
        print("  - free ⭐")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("SCRIPT: Actualizar ENUM timeline_type (MySQL)")
    print("=" * 60)
    
    if fix_timeline_type_enum():
        print("\n✅ Script ejecutado exitosamente")
        print("\n🎉 Ahora puedes crear líneas de tiempo tipo 'free'")
        print("\n⚠️  IMPORTANTE: Reinicia el backend para aplicar los cambios")
    else:
        print("\n❌ El script encontró errores")
