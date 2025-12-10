"""
Script para actualizar el ENUM de timeline_type en la base de datos
Agrega el valor 'free' al tipo timeline_type
"""
from app import create_app, db
from sqlalchemy import text

def fix_timeline_type_enum():
    """Actualiza el enum timeline_type para incluir 'free'"""
    app = create_app()
    
    with app.app_context():
        try:
            print("=" * 60)
            print("🔧 Actualizando ENUM timeline_type")
            print("=" * 60)
            
            # En SQL Server, no hay ENUMs nativos, se usan CHECKs
            # Primero, eliminar el constraint CHECK existente
            print("\n📋 Paso 1: Buscando constraint CHECK existente...")
            
            result = db.session.execute(text("""
                SELECT 
                    CONSTRAINT_NAME
                FROM INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE
                WHERE TABLE_NAME = 'timelines' 
                AND COLUMN_NAME = 'timeline_type'
            """))
            
            constraints = result.fetchall()
            
            for constraint in constraints:
                constraint_name = constraint[0]
                print(f"  - Encontrado: {constraint_name}")
                
                try:
                    print(f"  - Eliminando constraint: {constraint_name}")
                    db.session.execute(text(f"ALTER TABLE timelines DROP CONSTRAINT [{constraint_name}]"))
                    print(f"  ✅ Constraint eliminado")
                except Exception as e:
                    print(f"  ⚠️  No se pudo eliminar {constraint_name}: {e}")
            
            # Verificar el tipo de la columna
            print("\n📋 Paso 2: Verificando tipo de columna...")
            result = db.session.execute(text("""
                SELECT 
                    DATA_TYPE,
                    CHARACTER_MAXIMUM_LENGTH
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'timelines' 
                AND COLUMN_NAME = 'timeline_type'
            """))
            
            col_info = result.fetchone()
            if col_info:
                print(f"  Tipo actual: {col_info[0]}, Longitud: {col_info[1]}")
                
                # Si la columna no es VARCHAR o es muy corta, convertirla
                if col_info[0] != 'varchar' or (col_info[1] and col_info[1] < 20):
                    print("\n📋 Paso 3: Convirtiendo columna a VARCHAR(20)...")
                    db.session.execute(text("""
                        ALTER TABLE timelines 
                        ALTER COLUMN timeline_type VARCHAR(20) NULL
                    """))
                    print("  ✅ Columna convertida a VARCHAR(20)")
            
            # Agregar nuevo constraint CHECK con todos los valores
            print("\n📋 Paso 4: Agregando nuevo constraint CHECK...")
            db.session.execute(text("""
                ALTER TABLE timelines
                ADD CONSTRAINT CK_timelines_timeline_type 
                CHECK (timeline_type IN ('academic', 'course', 'project', 'free'))
            """))
            print("  ✅ Constraint CHECK agregado con valores: academic, course, project, free")
            
            # Establecer valor por defecto
            print("\n📋 Paso 5: Estableciendo valor por defecto...")
            try:
                # Primero eliminar default existente si hay
                db.session.execute(text("""
                    DECLARE @ConstraintName nvarchar(200)
                    SELECT @ConstraintName = Name 
                    FROM sys.default_constraints 
                    WHERE parent_object_id = object_id('timelines')
                    AND col_name(parent_object_id, parent_column_id) = 'timeline_type'
                    
                    IF @ConstraintName IS NOT NULL
                        EXEC('ALTER TABLE timelines DROP CONSTRAINT ' + @ConstraintName)
                """))
                
                # Agregar nuevo default
                db.session.execute(text("""
                    ALTER TABLE timelines
                    ADD CONSTRAINT DF_timelines_timeline_type DEFAULT 'project' FOR timeline_type
                """))
                print("  ✅ Valor por defecto establecido: 'project'")
            except Exception as e:
                print(f"  ⚠️  Advertencia al establecer default: {e}")
            
            db.session.commit()
            
            print("\n" + "=" * 60)
            print("✅ ENUM timeline_type actualizado exitosamente")
            print("=" * 60)
            print("\nValores permitidos:")
            print("  - academic")
            print("  - course")
            print("  - project")
            print("  - free")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error actualizando ENUM: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("SCRIPT: Actualizar ENUM timeline_type")
    print("=" * 60)
    
    if fix_timeline_type_enum():
        print("\n✅ Script ejecutado exitosamente")
    else:
        print("\n❌ El script encontró errores")
