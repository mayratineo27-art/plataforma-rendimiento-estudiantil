"""
Script con SQLAlchemy para actualizar el ENUM timeline_type
"""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Cargar variables de entorno
load_dotenv()

def fix_timeline_type_enum():
    """Actualiza el enum timeline_type usando SQLAlchemy"""
    
    # Construir connection string
    db_host = os.getenv('DB_HOST', 'localhost')
    db_name = os.getenv('DB_NAME', 'estudiantes')
    db_user = os.getenv('DB_USER', 'sa')
    db_password = os.getenv('DB_PASSWORD', 'YourStrong@Passw0rd')
    
    connection_string = f"mssql+pyodbc://{db_user}:{db_password}@{db_host}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    
    print("=" * 60)
    print("🔧 Actualizando ENUM timeline_type")
    print("=" * 60)
    print(f"Conectando a: {db_host}/{db_name}")
    
    try:
        engine = create_engine(connection_string)
        
        with engine.connect() as conn:
            # Paso 1: Buscar y eliminar constraints CHECK existentes
            print("\n📋 Paso 1: Buscando constraints CHECK...")
            result = conn.execute(text("""
                SELECT CONSTRAINT_NAME
                FROM INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE
                WHERE TABLE_NAME = 'timelines' 
                AND COLUMN_NAME = 'timeline_type'
            """))
            
            constraints = result.fetchall()
            for constraint in constraints:
                constraint_name = constraint[0]
                print(f"  - Encontrado: {constraint_name}")
                try:
                    conn.execute(text(f"ALTER TABLE timelines DROP CONSTRAINT [{constraint_name}]"))
                    conn.commit()
                    print(f"  ✅ Constraint eliminado: {constraint_name}")
                except Exception as e:
                    print(f"  ⚠️  No se pudo eliminar: {e}")
            
            # Paso 2: Verificar tipo de columna
            print("\n📋 Paso 2: Verificando tipo de columna...")
            result = conn.execute(text("""
                SELECT DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'timelines' 
                AND COLUMN_NAME = 'timeline_type'
            """))
            
            col_info = result.fetchone()
            if col_info:
                print(f"  Tipo actual: {col_info[0]}, Longitud: {col_info[1]}")
                
                # Convertir a VARCHAR si es necesario
                if col_info[0] != 'varchar' or (col_info[1] and col_info[1] < 20):
                    print("\n📋 Paso 3: Convirtiendo columna a VARCHAR(20)...")
                    conn.execute(text("ALTER TABLE timelines ALTER COLUMN timeline_type VARCHAR(20) NULL"))
                    conn.commit()
                    print("  ✅ Columna convertida a VARCHAR(20)")
            
            # Paso 4: Agregar nuevo constraint CHECK
            print("\n📋 Paso 4: Agregando nuevo constraint CHECK...")
            conn.execute(text("""
                ALTER TABLE timelines
                ADD CONSTRAINT CK_timelines_timeline_type 
                CHECK (timeline_type IN ('academic', 'course', 'project', 'free'))
            """))
            conn.commit()
            print("  ✅ Constraint CHECK agregado")
            
            # Paso 5: Establecer valor por defecto
            print("\n📋 Paso 5: Estableciendo valor por defecto...")
            try:
                # Eliminar default existente
                conn.execute(text("""
                    DECLARE @ConstraintName nvarchar(200)
                    SELECT @ConstraintName = Name 
                    FROM sys.default_constraints 
                    WHERE parent_object_id = object_id('timelines')
                    AND col_name(parent_object_id, parent_column_id) = 'timeline_type'
                    
                    IF @ConstraintName IS NOT NULL
                        EXEC('ALTER TABLE timelines DROP CONSTRAINT ' + @ConstraintName)
                """))
                conn.commit()
                
                # Agregar nuevo default
                conn.execute(text("""
                    ALTER TABLE timelines
                    ADD CONSTRAINT DF_timelines_timeline_type DEFAULT 'project' FOR timeline_type
                """))
                conn.commit()
                print("  ✅ Valor por defecto establecido: 'project'")
            except Exception as e:
                print(f"  ⚠️  Advertencia al establecer default: {e}")
        
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
    print("SCRIPT: Actualizar ENUM timeline_type (SQLAlchemy)")
    print("=" * 60)
    
    if fix_timeline_type_enum():
        print("\n✅ Script ejecutado exitosamente")
        print("\n🎉 Ahora puedes crear líneas de tiempo tipo 'free'")
    else:
        print("\n❌ El script encontró errores")
