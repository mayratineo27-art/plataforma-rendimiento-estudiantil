"""
Script para crear la tabla writing_evaluations
"""
import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import text

def create_writing_evaluations_table():
    """Crea la tabla writing_evaluations en la base de datos"""
    app = create_app()
    
    with app.app_context():
        try:
            # SQL para crear la tabla
            sql = """
            CREATE TABLE IF NOT EXISTS writing_evaluations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                course_id INT,
                file_name VARCHAR(255) NOT NULL,
                file_type VARCHAR(50),
                file_size INT,
                word_count INT,
                sentence_count INT,
                
                -- Scores
                overall_score INT,
                grammar_score INT,
                coherence_score INT,
                vocabulary_score INT,
                structure_score INT,
                
                -- Análisis de estilo
                tone_analysis VARCHAR(100),
                formality_score INT,
                complexity_level VARCHAR(50),
                
                -- Comparación
                previous_evaluation_id INT,
                improvement_percentage DECIMAL(5,2),
                
                -- Resultados detallados (JSON)
                metrics_json TEXT,
                evaluation_json TEXT,
                specific_errors_json TEXT,
                suggestions_json TEXT,
                
                -- Metadata
                evaluated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                
                -- Foreign keys
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES academic_courses(id) ON DELETE SET NULL,
                FOREIGN KEY (previous_evaluation_id) REFERENCES writing_evaluations(id) ON DELETE SET NULL,
                
                -- Índices para mejorar rendimiento
                INDEX idx_user_id (user_id),
                INDEX idx_course_id (course_id),
                INDEX idx_evaluated_at (evaluated_at)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            print("🔨 Creando tabla writing_evaluations...")
            db.session.execute(text(sql))
            db.session.commit()
            print("✅ Tabla writing_evaluations creada exitosamente!")
            
            # Verificar que la tabla existe
            result = db.session.execute(text("SHOW TABLES LIKE 'writing_evaluations'"))
            if result.fetchone():
                print("✅ Verificación exitosa: La tabla existe en la base de datos")
                
                # Mostrar estructura
                print("\n📋 Estructura de la tabla:")
                columns = db.session.execute(text("DESCRIBE writing_evaluations"))
                for col in columns:
                    print(f"  • {col[0]}: {col[1]}")
            else:
                print("❌ Error: La tabla no se pudo verificar")
                
        except Exception as e:
            print(f"❌ Error al crear la tabla: {e}")
            db.session.rollback()
            return False
            
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("CREACIÓN DE TABLA WRITING_EVALUATIONS")
    print("=" * 60)
    
    if create_writing_evaluations_table():
        print("\n🎉 ¡Migración completada con éxito!")
    else:
        print("\n❌ La migración falló")
        sys.exit(1)
