"""
Servicio de Evaluación de Escritura
====================================

Este módulo evalúa documentos de escritura del estudiante y genera
reportes detallados sobre calidad, mejoras y comparaciones entre versiones.

Funcionalidades:
- Extrae texto de archivos TXT, PDF, DOCX
- Analiza gramática, ortografía, estructura, vocabulario
- Compara versiones anteriores para medir progreso
- Usa Gemini AI para análisis profundo
- Genera reportes con métricas y recomendaciones
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, Optional, Tuple
import google.generativeai as genai
from flask import current_app

# Importar extractores de texto existentes
try:
    from app.services.document_processing.pdf_extractor import PDFExtractor
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️  PDFExtractor no disponible")


class WritingEvaluator:
    """
    Evaluador de escritura con IA
    
    Extrae texto de documentos, analiza calidad de escritura,
    y genera reportes detallados con métricas y recomendaciones.
    """
    
    @staticmethod
    def _configure_gemini():
        """Configura la API de Gemini"""
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            api_key = current_app.config.get('GEMINI_API_KEY')
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY no configurada")
        
        genai.configure(api_key=api_key)
    
    @staticmethod
    def _get_model():
        """Obtiene el modelo de Gemini configurado"""
        preferred = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
        
        # Lista de modelos a intentar en orden (actualizados a versiones 2024-2025)
        models_to_try = [
            preferred,
            'gemini-2.5-flash',
            'gemini-2.5-pro',
            'gemini-2.0-flash',
            'gemini-flash-latest',
            'gemini-pro-latest',
            'gemini-exp-1206'
        ]
        
        # Eliminar duplicados manteniendo el orden
        models_to_try = list(dict.fromkeys(models_to_try))
        
        last_error = None
        for model_name in models_to_try:
            try:
                print(f"   Intentando modelo: {model_name}")
                model = genai.GenerativeModel(model_name)
                print(f"   ✅ Modelo seleccionado: {model_name}")
                return model
            except Exception as e:
                last_error = e
                print(f"   ⚠️ Modelo {model_name} no disponible: {e}")
                continue
        
        # Si ninguno funciona, lanzar el último error
        raise Exception(f"No se pudo cargar ningún modelo. Último error: {last_error}")
    
    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extrae texto de un archivo
        
        Soporta:
        - TXT: lectura directa
        - PDF: usa PDFExtractor si está disponible
        - DOCX: usa python-docx si está instalado
        
        Args:
            file_path: Ruta al archivo
            
        Returns:
            str: Texto extraído
        """
        ext = os.path.splitext(file_path)[1].lower()
        
        print(f"📄 Extrayendo texto de {os.path.basename(file_path)} ({ext})")
        
        # Archivo de texto plano
        if ext in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
                print(f"  ✅ Extraídos {len(text)} caracteres")
                return text
        
        # Archivo PDF
        elif ext == '.pdf':
            if not PDF_AVAILABLE:
                raise ValueError("PDFExtractor no disponible. Instala PyPDF2 o pdfplumber")
            
            extractor = PDFExtractor()
            text = extractor.extract_text(file_path)
            print(f"  ✅ Extraídos {len(text)} caracteres del PDF")
            return text
        
        # Archivo DOCX
        elif ext == '.docx':
            try:
                from docx import Document
                doc = Document(file_path)
                text = '\n'.join([para.text for para in doc.paragraphs])
                print(f"  ✅ Extraídos {len(text)} caracteres del DOCX")
                return text
            except ImportError:
                raise ValueError("python-docx no instalado. Usa: pip install python-docx")
        
        else:
            raise ValueError(f"Formato de archivo no soportado: {ext}")
    
    @staticmethod
    def calculate_basic_metrics(text: str) -> Dict:
        """
        Calcula métricas básicas de texto
        
        Métricas:
        - Palabras totales
        - Oraciones
        - Párrafos
        - Promedio de palabras por oración
        - Vocabulario único
        - Palabras largas (>7 caracteres)
        
        Args:
            text: Texto a analizar
            
        Returns:
            dict: Métricas calculadas
        """
        # Contar palabras
        words = re.findall(r'\b\w+\b', text.lower())
        word_count = len(words)
        
        # Contar oraciones (aproximado)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)
        
        # Contar párrafos
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        paragraph_count = len(paragraphs)
        
        # Vocabulario único
        unique_words = set(words)
        vocabulary_size = len(unique_words)
        
        # Palabras largas (complejidad léxica)
        long_words = [w for w in words if len(w) > 7]
        long_word_count = len(long_words)
        
        # Promedio de palabras por oración
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        
        # Índice de legibilidad (Flesch simplificado)
        # Menor = más difícil, Mayor = más fácil
        if sentence_count > 0 and word_count > 0:
            avg_syllables = sum(WritingEvaluator._count_syllables(w) for w in words) / word_count
            readability = 206.835 - 1.015 * avg_words_per_sentence - 84.6 * avg_syllables
            readability = max(0, min(100, readability))  # Clamp entre 0-100
        else:
            readability = 50
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'paragraph_count': paragraph_count,
            'vocabulary_size': vocabulary_size,
            'long_word_count': long_word_count,
            'avg_words_per_sentence': round(avg_words_per_sentence, 2),
            'vocabulary_richness': round(vocabulary_size / word_count * 100, 2) if word_count > 0 else 0,
            'readability_score': round(readability, 2)
        }
    
    @staticmethod
    def _count_syllables(word: str) -> int:
        """Cuenta sílabas en una palabra (aproximado para español)"""
        vowels = 'aeiouáéíóúü'
        word = word.lower()
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        return max(1, syllable_count)  # Mínimo 1 sílaba
    
    @staticmethod
    def evaluate_with_ai(text: str, previous_text: Optional[str] = None) -> Dict:
        """
        Evalúa el texto usando Gemini AI
        
        Análisis profundo:
        - Gramática y ortografía con errores específicos
        - Coherencia y cohesión
        - Vocabulario y estilo
        - Estructura y organización
        - Análisis de tono y formalidad
        - Nivel de complejidad
        - Sugerencias específicas de corrección
        - Comparación con versión anterior (si existe)
        
        Args:
            text: Texto actual a evaluar
            previous_text: Texto de versión anterior (opcional)
            
        Returns:
            dict: Reporte de evaluación con scores y recomendaciones detalladas
        """
        try:
            print("🤖 Evaluando con Gemini AI (Análisis Profundo)...")
            
            WritingEvaluator._configure_gemini()
            model = WritingEvaluator._get_model()
            
            # Construir prompt según si hay comparación o no
            if previous_text:
                prompt = f"""
Eres un profesor experto en redacción y escritura académica con enfoque en corrección detallada.

TAREA: Evalúa el progreso del estudiante comparando dos versiones de su escrito. Proporciona análisis EXHAUSTIVO.

VERSIÓN ANTERIOR:
{previous_text[:3000]}

VERSIÓN ACTUAL:
{text[:3000]}

FORMATO DE SALIDA (JSON):
{{
  "overall_score": 85,
  "grammar_score": 90,
  "coherence_score": 80,
  "vocabulary_score": 85,
  "structure_score": 88,
  "improvement_percentage": 15,
  
  "tone_analysis": "académico",
  "formality_score": 85,
  "complexity_level": "intermedio-avanzado",
  
  "specific_errors": [
    {{
      "type": "ortografía",
      "error": "havía",
      "correction": "había",
      "location": "párrafo 2",
      "explanation": "La 'h' es necesaria en el verbo haber"
    }},
    {{
      "type": "concordancia",
      "error": "los datos muestra",
      "correction": "los datos muestran",
      "location": "párrafo 3",
      "explanation": "El verbo debe concordar en plural con 'datos'"
    }}
  ],
  
  "suggestions": [
    {{
      "category": "estructura",
      "suggestion": "Conecta el párrafo 2 y 3 con una transición",
      "example": "Por otro lado, ...",
      "priority": "alta"
    }},
    {{
      "category": "vocabulario",
      "suggestion": "Reemplaza 'cosa' por término más específico",
      "example": "elemento, aspecto, característica",
      "priority": "media"
    }}
  ],
  
  "strengths": [
    "Mejor uso de conectores lógicos",
    "Vocabulario técnico más preciso",
    "Argumentación más sólida con ejemplos",
    "Estructura clara con introducción-desarrollo-conclusión"
  ],
  
  "weaknesses": [
    "Algunos errores de puntuación en oraciones largas",
    "Párrafos desbalanceados (algunos muy largos)",
    "Uso repetitivo de 'sin embargo'"
  ],
  
  "improvements_made": [
    "Corrigió 3 errores ortográficos previos",
    "Mejoró la introducción con contexto más claro",
    "Añadió 2 ejemplos concretos en el desarrollo",
    "Redujo uso de muletillas ('entonces', 'pues')"
  ],
  
  "recommendations": [
    "Revisar uso de comas en oraciones compuestas",
    "Dividir párrafo 4 en dos partes temáticas",
    "Variar conectores: 'no obstante', 'por el contrario'",
    "Agregar más datos o estadísticas para respaldar argumentos",
    "Revisar consistencia en tiempos verbales (presente vs pasado)"
  ],
  
  "summary": "El estudiante muestra una mejora significativa en su escritura. La estructura es más clara y los argumentos están mejor desarrollados. Los principales avances son en vocabulario y coherencia. Se recomienda enfocarse en la puntuación y en la variedad de conectores para alcanzar un nivel avanzado."
}}

REGLAS:
1. Responde ÚNICAMENTE con el objeto JSON (sin ```json ni texto adicional)
2. Scores del 0-100 (100 = excelente)
3. tone_analysis: formal/informal/académico/técnico/narrativo
4. formality_score: 0-100 (0=muy informal, 100=muy formal)
5. complexity_level: básico/intermedio/intermedio-avanzado/avanzado
6. specific_errors: mínimo 3, máximo 10 errores más relevantes
7. suggestions: mínimo 3 sugerencias prácticas con ejemplos
8. improvement_percentage: % de mejora respecto a versión anterior
9. Sé MUY ESPECÍFICO: localiza errores, da ejemplos concretos
10. Prioriza feedback ACCIONABLE que el estudiante pueda aplicar

GENERA LA EVALUACIÓN EXHAUSTIVA:
"""
            else:
                prompt = f"""
Eres un profesor experto en redacción y escritura académica con enfoque en corrección detallada.

TAREA: Evalúa la calidad del siguiente escrito del estudiante. Proporciona análisis EXHAUSTIVO con todos los detalles.

TEXTO A EVALUAR:
{text[:4000]}

FORMATO DE SALIDA (JSON):
{{
  "overall_score": 75,
  "grammar_score": 80,
  "coherence_score": 70,
  "vocabulary_score": 75,
  "structure_score": 78,
  
  "tone_analysis": "académico",
  "formality_score": 80,
  "complexity_level": "intermedio",
  
  "specific_errors": [
    {{
      "type": "ortografía",
      "error": "aver",
      "correction": "haber",
      "location": "párrafo 1, línea 3",
      "explanation": "'Haber' como verbo auxiliar siempre lleva 'h'"
    }},
    {{
      "type": "puntuación",
      "error": "...idea sin embargo...",
      "correction": "...idea. Sin embargo, ...",
      "location": "párrafo 2",
      "explanation": "Los conectores entre oraciones requieren punto antes y coma después"
    }},
    {{
      "type": "concordancia",
      "error": "el grupo de estudiantes participaron",
      "correction": "el grupo de estudiantes participó",
      "location": "párrafo 3",
      "explanation": "El núcleo del sujeto es 'grupo' (singular)"
    }}
  ],
  
  "suggestions": [
    {{
      "category": "estructura",
      "suggestion": "Agregar párrafo de introducción más desarrollado",
      "example": "Comenzar con contexto general antes de presentar la tesis",
      "priority": "alta"
    }},
    {{
      "category": "vocabulario",
      "suggestion": "Reemplazar palabras genéricas por términos específicos",
      "example": "'aspecto' → 'característica', 'dimensión', 'factor'",
      "priority": "alta"
    }},
    {{
      "category": "coherencia",
      "suggestion": "Usar más conectores entre párrafos",
      "example": "Agregar: 'Por consiguiente', 'En contraste', 'Adicionalmente'",
      "priority": "media"
    }},
    {{
      "category": "gramática",
      "suggestion": "Revisar uso de gerundios al inicio de oraciones",
      "example": "Evitar: 'Siendo importante...' → Mejor: 'Como es importante...'",
      "priority": "media"
    }}
  ],
  
  "strengths": [
    "Ideas bien fundamentadas con ejemplos concretos",
    "Uso correcto de vocabulario técnico en el tema",
    "Buena estructura de introducción con tesis clara",
    "Párrafos con longitud adecuada (5-7 oraciones)"
  ],
  
  "weaknesses": [
    "Faltan conectores entre párrafos 2 y 3",
    "3 errores de concordancia género-número",
    "Conclusión muy breve (solo 2 oraciones)",
    "Uso repetitivo de 'es importante' (aparece 5 veces)",
    "Falta de citas o referencias para respaldar afirmaciones"
  ],
  
  "recommendations": [
    "Usar más conectores lógicos: 'sin embargo', 'por lo tanto', 'además'",
    "Revisar concordancia de género y número en todos los párrafos",
    "Ampliar la conclusión: incluir implicaciones y reflexión final",
    "Agregar 2-3 ejemplos concretos en los argumentos principales",
    "Variar el vocabulario: evitar repetición de palabras clave",
    "Dividir oraciones muy largas (más de 25 palabras) en dos",
    "Incluir datos o estadísticas para fortalecer argumentos",
    "Revisar consistencia en tiempos verbales (presente/pasado)"
  ],
  
  "summary": "Un escrito sólido con ideas claras y bien fundamentadas. El autor demuestra conocimiento del tema y capacidad de argumentación. Los puntos fuertes son la estructura lógica y el uso de vocabulario técnico. Sin embargo, necesita trabajo en: 1) coherencia entre párrafos (más conectores), 2) revisión gramatical (concordancias), y 3) desarrollo de la conclusión. Con estas mejoras, el texto alcanzaría un nivel avanzado."
}}

REGLAS:
1. Responde ÚNICAMENTE con el objeto JSON (sin ```json ni texto adicional)
2. Scores del 0-100 (100 = excelente)
3. tone_analysis: formal/informal/académico/técnico/narrativo/persuasivo
4. formality_score: 0-100 (0=muy informal, 100=muy formal)
5. complexity_level: básico/intermedio/intermedio-avanzado/avanzado
6. specific_errors: mínimo 3, máximo 12 errores concretos con ubicación
7. suggestions: mínimo 4 sugerencias con ejemplos específicos
8. Sé MUY ESPECÍFICO: localiza errores, da ejemplos de corrección
9. En recommendations: mínimo 6 recomendaciones prácticas y accionables
10. En summary: análisis de 3-4 oraciones con fortalezas, debilidades y pasos a seguir

GENERA LA EVALUACIÓN EXHAUSTIVA:
"""
            
            print("  🚀 Enviando a Gemini...")
            response = model.generate_content(prompt)
            print(f"  ✅ Respuesta recibida: {len(response.text)} caracteres")
            
            # Limpiar respuesta de marcadores de código
            clean_text = response.text.strip()
            
            # Remover bloques de código markdown si existen
            if clean_text.startswith("```"):
                # Buscar el primer { y el último }
                start = clean_text.find("{")
                end = clean_text.rfind("}") + 1
                if start != -1 and end > start:
                    clean_text = clean_text[start:end]
            
            # Intentar parsear JSON
            try:
                evaluation = json.loads(clean_text)
            except json.JSONDecodeError as e:
                # Si falla, intentar reparar JSON común
                print(f"⚠️  Error JSON, intentando reparar: {e}")
                
                # Buscar el JSON válido más largo
                import re
                json_match = re.search(r'\{[^}]*(?:\{[^}]*\}[^}]*)*\}', clean_text, re.DOTALL)
                if json_match:
                    clean_text = json_match.group(0)
                    evaluation = json.loads(clean_text)
                else:
                    raise
            
            print(f"  ✅ Evaluación completada - Score: {evaluation.get('overall_score', 'N/A')}/100")
            print(f"  📊 Errores detectados: {len(evaluation.get('specific_errors', []))}")
            print(f"  💡 Sugerencias: {len(evaluation.get('suggestions', []))}")
            print(f"  🎯 Tono: {evaluation.get('tone_analysis', 'N/A')}")
            print(f"  📏 Formalidad: {evaluation.get('formality_score', 'N/A')}/100")
            
            return evaluation
        
        except json.JSONDecodeError as e:
            print(f"❌ Error parseando JSON de Gemini: {e}")
            print(f"Respuesta raw: {response.text[:500]}")
            return WritingEvaluator._fallback_evaluation(text, previous_text)
        
        except Exception as e:
            print(f"❌ Error en evaluación con IA: {e}")
            return WritingEvaluator._fallback_evaluation(text, previous_text)
    
    @staticmethod
    def _fallback_evaluation(text: str, previous_text: Optional[str] = None) -> Dict:
        """
        Evaluación básica de fallback si Gemini falla
        
        Usa métricas heurísticas simples.
        """
        print("⚠️  Usando evaluación heurística de fallback")
        
        metrics = WritingEvaluator.calculate_basic_metrics(text)
        
        # Calcular scores basados en métricas
        grammar_score = min(100, metrics['readability_score'] + 20)
        vocabulary_score = min(100, metrics['vocabulary_richness'] * 2)
        structure_score = 70 if metrics['paragraph_count'] >= 3 else 50
        coherence_score = 65
        overall_score = (grammar_score + vocabulary_score + structure_score + coherence_score) / 4
        
        evaluation = {
            'overall_score': round(overall_score),
            'grammar_score': round(grammar_score),
            'coherence_score': round(coherence_score),
            'vocabulary_score': round(vocabulary_score),
            'structure_score': round(structure_score),
            'tone_analysis': 'neutro',
            'formality_score': 50,
            'complexity_level': 'intermedio',
            'specific_errors': [
                {
                    'type': 'sistema',
                    'error': 'Análisis de IA no disponible',
                    'correction': 'Revisar manualmente',
                    'location': 'N/A',
                    'explanation': 'Se requiere revisión manual completa'
                }
            ],
            'suggestions': [
                {
                    'category': 'general',
                    'suggestion': 'Revisar gramática y ortografía con herramienta externa',
                    'example': 'Usar corrector ortográfico',
                    'priority': 'alta'
                },
                {
                    'category': 'coherencia',
                    'suggestion': 'Verificar coherencia entre párrafos',
                    'example': 'Agregar conectores lógicos',
                    'priority': 'alta'
                }
            ],
            'strengths': [
                f"Vocabulario rico con {metrics['vocabulary_size']} palabras únicas",
                f"Buena extensión: {metrics['word_count']} palabras",
                f"Legibilidad adecuada: {metrics['readability_score']}/100"
            ],
            'weaknesses': [
                "Evaluación limitada (IA no disponible)",
                "Se recomienda revisión manual completa",
                "No se pudieron detectar errores específicos"
            ],
            'recommendations': [
                "Revisar gramática y ortografía manualmente",
                "Verificar coherencia entre párrafos",
                "Usar herramientas de corrección adicionales",
                "Pedir retroalimentación a un profesor o tutor",
                "Leer en voz alta para detectar errores",
                "Revisar consistencia en tiempos verbales"
            ],
            'summary': f"Evaluación básica: {metrics['word_count']} palabras, {metrics['sentence_count']} oraciones, legibilidad {metrics['readability_score']}/100. Se requiere análisis más profundo con IA o revisión manual."
        }
        
        # Si hay versión previa, calcular mejora
        if previous_text:
            prev_metrics = WritingEvaluator.calculate_basic_metrics(previous_text)
            word_diff = metrics['word_count'] - prev_metrics['word_count']
            vocab_diff = metrics['vocabulary_size'] - prev_metrics['vocabulary_size']
            
            improvement = 0
            if word_diff > 0:
                improvement += 5
            if vocab_diff > 0:
                improvement += 10
            
            evaluation['improvement_percentage'] = improvement
            evaluation['improvements_made'] = [
                f"Palabras: {prev_metrics['word_count']} → {metrics['word_count']} ({'+' if word_diff > 0 else ''}{word_diff})",
                f"Vocabulario: {prev_metrics['vocabulary_size']} → {metrics['vocabulary_size']} ({'+' if vocab_diff > 0 else ''}{vocab_diff})"
            ]
        
        return evaluation
    
    @staticmethod
    def generate_report(
        current_file: str,
        previous_file: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Dict:
        """
        Genera reporte completo de evaluación
        
        Flujo:
        1. Extraer texto de archivo(s)
        2. Calcular métricas básicas
        3. Evaluar con IA
        4. Combinar resultados
        5. Generar reporte final
        
        Args:
            current_file: Ruta al archivo actual
            previous_file: Ruta al archivo anterior (opcional)
            metadata: Datos adicionales (user_id, course_id, etc.)
            
        Returns:
            dict: Reporte completo con métricas, evaluación y recomendaciones
        """
        print("=" * 80)
        print("📊 GENERANDO REPORTE DE EVALUACIÓN DE ESCRITURA")
        print("=" * 80)
        
        # 1. Extraer texto
        current_text = WritingEvaluator.extract_text(current_file)
        previous_text = None
        
        if previous_file and os.path.exists(previous_file):
            print(f"\n📄 Comparando con versión anterior...")
            previous_text = WritingEvaluator.extract_text(previous_file)
        
        # 2. Calcular métricas básicas
        print(f"\n📈 Calculando métricas básicas...")
        current_metrics = WritingEvaluator.calculate_basic_metrics(current_text)
        print(f"  ✅ Palabras: {current_metrics['word_count']}")
        print(f"  ✅ Oraciones: {current_metrics['sentence_count']}")
        print(f"  ✅ Vocabulario único: {current_metrics['vocabulary_size']}")
        print(f"  ✅ Legibilidad: {current_metrics['readability_score']}/100")
        
        previous_metrics = None
        if previous_text:
            previous_metrics = WritingEvaluator.calculate_basic_metrics(previous_text)
            print(f"\n📊 Comparación con versión anterior:")
            print(f"  Palabras: {previous_metrics['word_count']} → {current_metrics['word_count']}")
            print(f"  Vocabulario: {previous_metrics['vocabulary_size']} → {current_metrics['vocabulary_size']}")
        
        # 3. Evaluar con IA
        print(f"\n🤖 Evaluando calidad con IA...")
        ai_evaluation = WritingEvaluator.evaluate_with_ai(current_text, previous_text)
        
        # 4. Generar reporte final
        report = {
            'evaluated_at': datetime.utcnow().isoformat(),
            'file_name': os.path.basename(current_file),
            'metrics': {
                'current': current_metrics,
                'previous': previous_metrics
            },
            'evaluation': ai_evaluation,
            'metadata': metadata or {}
        }
        
        print("\n" + "=" * 80)
        print(f"✅ REPORTE GENERADO - Score General: {ai_evaluation.get('overall_score', 'N/A')}/100")
        print("=" * 80)
        
        return report
