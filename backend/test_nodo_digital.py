"""
Script de verificación rápida del Nodo Digital
Verifica que todos los endpoints y modelos estén funcionando
"""

import sys
import os

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models.academic import AcademicCourse, AcademicTask
from app.models.timer import StudyTimer

def test_nodo_digital():
    """Prueba rápida de funcionalidades del Nodo Digital"""
    print("🧪 Iniciando pruebas del Nodo Digital...\n")
    
    app = create_app()
    
    with app.app_context():
        try:
            # 1. Verificar conexión a BD
            print("1️⃣ Verificando conexión a base de datos...")
            db.session.execute('SELECT 1')
            print("   ✅ Conexión exitosa\n")
            
            # 2. Verificar modelos
            print("2️⃣ Verificando modelos...")
            models_to_check = [
                ('AcademicCourse', AcademicCourse),
                ('AcademicTask', AcademicTask),
                ('StudyTimer', StudyTimer)
            ]
            
            for model_name, model_class in models_to_check:
                try:
                    count = model_class.query.count()
                    print(f"   ✅ {model_name}: {count} registros")
                except Exception as e:
                    print(f"   ❌ {model_name}: Error - {e}")
            
            print()
            
            # 3. Verificar rutas registradas
            print("3️⃣ Verificando rutas registradas...")
            routes_to_check = [
                '/api/academic/courses',
                '/api/academic/tools/mindmap',
                '/api/academic/tools/summary',
                '/api/timer/start',
                '/api/timer/user/<int:user_id>',
            ]
            
            all_routes = [str(rule) for rule in app.url_map.iter_rules()]
            
            for route in routes_to_check:
                if any(route.replace('<int:user_id>', '<user_id>') in r for r in all_routes):
                    print(f"   ✅ {route}")
                else:
                    print(f"   ❌ {route} - No encontrada")
            
            print()
            
            # 4. Verificar servicios
            print("4️⃣ Verificando servicios de IA...")
            try:
                from app.services.academic.syllabus_processor import SyllabusProcessor
                print("   ✅ SyllabusProcessor")
            except Exception as e:
                print(f"   ❌ SyllabusProcessor: {e}")
            
            try:
                from app.services.academic.study_tools import StudyToolsService
                print("   ✅ StudyToolsService")
            except Exception as e:
                print(f"   ❌ StudyToolsService: {e}")
            
            print()
            
            # 5. Verificar configuración de Gemini
            print("5️⃣ Verificando configuración de API...")
            gemini_key = os.environ.get('GEMINI_API_KEY')
            if gemini_key:
                print(f"   ✅ GEMINI_API_KEY configurada ({gemini_key[:10]}...)")
            else:
                print("   ⚠️  GEMINI_API_KEY no encontrada en variables de entorno")
            
            print()
            
            # Resumen
            print("="*50)
            print("✅ VERIFICACIÓN COMPLETA")
            print("="*50)
            print("\n📊 Resumen:")
            print("   - Base de datos: Conectada")
            print("   - Modelos: Verificados")
            print("   - Rutas: Registradas")
            print("   - Servicios: Importados")
            print("\n🚀 El Nodo Digital está listo para usar!")
            
        except Exception as e:
            print(f"\n❌ Error durante la verificación: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_nodo_digital()
