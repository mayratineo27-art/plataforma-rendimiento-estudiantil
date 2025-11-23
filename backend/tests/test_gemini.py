"""
test_gemini.py - Script para probar integración con Gemini
Ejecutar: python test_gemini.py
"""

import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from app.services.ai.gemini_service import gemini_service


def test_basic_generation():
    """Test 1: Generación básica de contenido"""
    print("\n" + "="*60)
    print("TEST 1: Generación básica de contenido")
    print("="*60)
    
    result = gemini_service.generate_content(
        prompt="Explica en 2 oraciones qué es la inteligencia artificial",
        user_id=None,
        interaction_type='test'
    )
    
    if result['success']:
        print("✅ SUCCESS")
        print(f"📝 Contenido generado: {result['content']}")
        print(f"🔢 Tokens usados: {result['tokens_used']}")
        print(f"⏱️  Tiempo: {result['processing_time_ms']}ms")
    else:
        print("❌ ERROR")
        print(f"Error: {result.get('error')}")


def test_text_analysis():
    """Test 2: Análisis de texto académico"""
    print("\n" + "="*60)
    print("TEST 2: Análisis de texto académico")
    print("="*60)
    
    sample_text = """
    La inteligencia artificial es una rama de la ciencia de la computación
    que se enfoca en crear sistemas capaces de realizar tareas que normalmente
    requieren inteligencia humana. Estos sistemas utilizan algoritmos de
    aprendizaje automático para mejorar su rendimiento con la experiencia.
    """
    
    result = gemini_service.analyze_text(
        text=sample_text,
        user_id=None,
        analysis_type='comprehensive'
    )
    
    if result['success'] and result.get('analysis'):
        print("✅ SUCCESS")
        analysis = result['analysis']
        print(f"📊 Calidad de escritura: {analysis.get('writing_quality_score')}/100")
        print(f"📚 Nivel académico: {analysis.get('academic_level')}")
        print(f"🔑 Conceptos clave: {', '.join(analysis.get('key_concepts', []))}")
        print(f"💡 Recomendaciones: {len(analysis.get('recommendations', []))}")
    else:
        print("❌ ERROR")
        print(f"Error: {result.get('error') or result.get('parse_error')}")


def test_sentiment_analysis():
    """Test 3: Análisis de sentimiento"""
    print("\n" + "="*60)
    print("TEST 3: Análisis de sentimiento")
    print("="*60)
    
    sample_text = """
    Me siento muy motivado con este proyecto. Estoy aprendiendo mucho
    y me entusiasma ver los resultados. Es desafiante pero gratificante.
    """
    
    result = gemini_service.analyze_sentiment(
        text=sample_text,
        user_id=None
    )
    
    if result['success'] and result.get('sentiment'):
        print("✅ SUCCESS")
        sentiment = result['sentiment']
        print(f"😊 Sentimiento: {sentiment.get('sentiment')}")
        print(f"📈 Score: {sentiment.get('sentiment_score')}/100")
        print(f"💯 Confianza: {sentiment.get('confidence')}%")
        print(f"🎭 Emociones: {', '.join(sentiment.get('emotions_detected', []))}")
    else:
        print("❌ ERROR")
        print(f"Error: {result.get('error')}")


def main():
    """Ejecutar todos los tests"""
    print("\n" + "="*60)
    print("🚀 INICIANDO TESTS DE GEMINI SERVICE")
    print("="*60)
    
    # Crear contexto de aplicación
    app = create_app()
    
    with app.app_context():
        try:
            # Ejecutar tests
            test_basic_generation()
            test_text_analysis()
            test_sentiment_analysis()
            
            print("\n" + "="*60)
            print("✅ TODOS LOS TESTS COMPLETADOS")
            print("="*60)
            print("\n💡 TIP: Revisa la tabla 'ai_interactions' en MySQL")
            print("   para ver el registro de todas las llamadas a Gemini\n")
            
        except Exception as e:
            print("\n" + "="*60)
            print("❌ ERROR GENERAL")
            print("="*60)
            print(f"Error: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    main()