"""
Script para verificar y corregir la tabla timelines
"""

from app import create_app, db
from sqlalchemy import inspect, text

def fix_timeline_table():
    """Verifica y corrige la tabla timelines"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔍 Verificando tabla timelines...")
            
            inspector = inspect(db.engine)
            
            # Verificar si la tabla existe
            if 'timelines' not in inspector.get_table_names():
                print("❌ La tabla timelines NO existe")
                print("📋 Creando tabla timelines...")
                
                # Crear la tabla directamente con SQL
                db.session.execute(text("""
                    CREATE TABLE IF NOT EXISTS timelines (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        project_id INT NULL,
                        course_id INT NULL,
                        title VARCHAR(200) NOT NULL,
                        description TEXT,
                        timeline_type ENUM('academic', 'course', 'project') DEFAULT 'project',
                        end_date DATETIME NULL,
                        steps_json TEXT NULL,
                        is_visible BOOLEAN DEFAULT TRUE,
                        is_completed BOOLEAN DEFAULT FALSE,
                        completed_date DATETIME NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                        FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
                        FOREIGN KEY (course_id) REFERENCES academic_courses(id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """))
                
                print("✅ Tabla timelines creada")
            else:
                print("✅ La tabla timelines existe")
                
                # Mostrar columnas
                columns = inspector.get_columns('timelines')
                print("\n📊 Columnas de la tabla:")
                for col in columns:
                    nullable = "NULL" if col['nullable'] else "NOT NULL"
                    default = f"DEFAULT {col['default']}" if col['default'] else ""
                    print(f"  - {col['name']}: {col['type']} {nullable} {default}")
            
            # Verificar si tabla timeline_steps existe
            if 'timeline_steps' not in inspector.get_table_names():
                print("\n📋 Creando tabla timeline_steps...")
                
                db.session.execute(text("""
                    CREATE TABLE IF NOT EXISTS timeline_steps (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        timeline_id INT NOT NULL,
                        title VARCHAR(200) NOT NULL,
                        description TEXT,
                        `order` INT NOT NULL DEFAULT 1,
                        duration VARCHAR(50),
                        completed BOOLEAN DEFAULT FALSE,
                        completed_at DATETIME NULL,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (timeline_id) REFERENCES timelines(id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """))
                
                print("✅ Tabla timeline_steps creada")
            else:
                print("✅ La tabla timeline_steps existe")
            
            db.session.commit()
            print("\n🎉 ¡Verificación completada!")
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == '__main__':
    fix_timeline_table()
