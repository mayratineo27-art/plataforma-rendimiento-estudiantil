"""
Script para crear las tablas necesarias:
- timelines: líneas de tiempo guardadas
- Actualizar time_sessions: agregar campos para cronómetro inteligente
"""

from app import create_app, db
from app.models.timeline import Timeline
from app.models.project import Project, TimeSession

def create_tables():
    """Crea las tablas en la base de datos"""
    app = create_app()
    
    with app.app_context():
        try:
            print("📋 Creando/actualizando tablas...")
            
            # Crear todas las tablas
            db.create_all()
            
            print("✅ Tablas creadas/actualizadas correctamente:")
            print("   - timelines")
            print("   - time_sessions (actualizada)")
            print("   - projects")
            
            return True
            
        except Exception as e:
            print(f"❌ Error al crear tablas: {e}")
            return False

if __name__ == '__main__':
    success = create_tables()
    if success:
        print("\n🎉 ¡Migraciones completadas exitosamente!")
    else:
        print("\n⚠️  Hubo errores durante la migración")
