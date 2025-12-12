#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test de evaluación con Gemini AI"""

from app.services.academic.writing_evaluator import WritingEvaluator

def main():
    evaluator = WritingEvaluator()
    
    text = """La inteligencia artificial está transformando nuestra sociedad de manera profunda. 
    Sus aplicaciones van desde el reconocimiento de voz hasta la conducción autónoma de vehículos. 
    Sin embargo, también plantea importantes desafíos éticos que debemos abordar con responsabilidad. 
    Es fundamental desarrollar estas tecnologías de forma transparente y regulada."""
    
    print("🧪 Probando evaluación con IA Gemini...")
    print(f"📝 Texto: {len(text)} caracteres\n")
    
    result = evaluator.evaluate_with_ai(text, 'Ensayo sobre IA')
    
    print("\n" + "="*60)
    print("✅ EVALUACIÓN COMPLETADA")
    print("="*60)
    print(f"📊 Score General: {result.get('overall_score', 'N/A')}/100")
    print(f"📚 Gramática: {result.get('grammar_score', 'N/A')}/100")
    print(f"🔗 Coherencia: {result.get('coherence_score', 'N/A')}/100")
    print(f"📖 Vocabulario: {result.get('vocabulary_score', 'N/A')}/100")
    print(f"🏗️ Estructura: {result.get('structure_score', 'N/A')}/100")
    print(f"\n📋 Resumen:")
    print(result.get('summary', 'N/A'))
    print(f"\n💡 Sugerencias:")
    for i, sug in enumerate(result.get('suggestions', [])[:3], 1):
        print(f"  {i}. {sug.get('suggestion', 'N/A')}")
    print("\n")

if __name__ == '__main__':
    main()
