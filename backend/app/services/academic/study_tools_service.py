import google.generativeai as genai
import os
import json
import re
from flask import current_app

class StudyToolsService:
    """Servicio unificado para todas las herramientas de estudio con IA (Gemini)"""
    
    @staticmethod
    def _configure_gemini():
        """Configura la API de Gemini con la clave del entorno"""
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            api_key = current_app.config.get('GEMINI_API_KEY')
        
        if not api_key:
            print("❌ Error: GEMINI_API_KEY no encontrada en variables de entorno.")
            raise ValueError("La API Key de Gemini no está configurada.")
            
        genai.configure(api_key=api_key)

    @staticmethod
    def _get_model():
      """Obtiene el modelo configurado de Gemini con fallback seguro"""
      preferred = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
      try:
        return genai.GenerativeModel(preferred)
      except Exception as _:
        # Fallbacks por compatibilidad de librería
        for candidate in ['gemini-1.5-flash', 'gemini-pro']:
          try:
            return genai.GenerativeModel(candidate)
          except Exception:
            continue
        # Último recurso: relanzar
        return genai.GenerativeModel(preferred)

    @staticmethod
    def generate_mind_map(topic_text, context="General"):
        """
        Genera un mapa mental jerárquico usando Gemini AI
        
        Args:
            topic_text: Texto o tema para generar el mapa
            context: Contexto académico (nombre del curso)
            
        Returns:
            dict: Estructura JSON del mapa mental
        """
        try:
            print(f"🧠 Generando mapa mental...")
            print(f"  📝 Tema: {topic_text[:100]}")
            print(f"  📚 Contexto: {context}")
            
            StudyToolsService._configure_gemini()
            print(f"  ✅ Gemini configurado")
            
            model = StudyToolsService._get_model()
            print(f"  ✅ Modelo obtenido: {model}")
            
            prompt = f"""
Eres un experto en pedagogía visual y mapas mentales académicos.

CONTEXTO: {context}
TEMA: "{topic_text[:3000]}"

TAREA: Crea un mapa mental estructurado y completo sobre este tema.

FORMATO DE SALIDA (JSON):
{{
  "root": "Concepto Principal",
  "children": [
    {{
      "name": "Subtema 1",
      "children": [
        {{"name": "Detalle 1.1"}},
        {{"name": "Detalle 1.2"}}
      ]
    }},
    {{
      "name": "Subtema 2",
      "children": [...]
    }}
  ]
}}

REGLAS CRÍTICAS:
1. Responde ÚNICAMENTE con el objeto JSON (sin ```json ni texto adicional)
2. Mínimo 3 niveles de profundidad
3. Cada nodo máximo 5 palabras
4. Entre 3-6 ramas principales
5. Estructura lógica y pedagógica

GENERA EL MAPA MENTAL:
"""
            
            print(f"  🚀 Enviando a Gemini...")
            response = model.generate_content(prompt)
            print(f"  ✅ Respuesta recibida: {len(response.text)} caracteres")
            
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            print(f"  🔧 Texto limpio: {clean_text[:200]}...")
            
            # Intenta parsear el JSON
            mind_map_data = json.loads(clean_text)
            print(f"  ✅ JSON parseado correctamente")
            
            # Validar estructura mínima
            if 'root' not in mind_map_data:
                raise ValueError("El mapa mental no tiene nodo raíz")
            
            print(f"  ✅ Mapa mental generado con raíz: {mind_map_data.get('root')}")
                
            return mind_map_data

        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON del mapa mental: {e}")
            print(f"Respuesta recibida: {response.text[:500]}")
            # Retornar un mapa de error estructurado
            return {
                "root": "Error de Formato",
                "children": [
                    {"name": "La IA no generó un formato válido"},
                    {"name": "Intenta reformular el tema"}
                ]
            }
        except Exception as e:
            print(f"❌ Error generando mapa mental: {e}")
            return {
                "root": "Error de Conexión",
                "children": [{"name": "Verifica tu conexión y API Key"}]
            }

    @staticmethod
    def generate_summary(text, summary_type="general"):
        """
        Genera un resumen inteligente usando Gemini AI
        
        Args:
            text: Texto a resumir
            summary_type: Tipo de resumen (general, ejecutivo, detallado)
            
        Returns:
            str: Resumen en formato Markdown
        """
        try:
            StudyToolsService._configure_gemini()
            model = StudyToolsService._get_model()
            
            prompts = {
                "general": "Resume el siguiente texto de manera clara y concisa:",
                "ejecutivo": "Crea un resumen ejecutivo (máximo 3 párrafos) del siguiente texto:",
                "detallado": "Crea un resumen detallado con puntos clave del siguiente texto:"
            }
            
            prompt_base = prompts.get(summary_type, prompts["general"])
            
            prompt = f"""
Eres un asistente académico experto en síntesis de información.

{prompt_base}

TEXTO A RESUMIR:
{text[:6000]}

FORMATO DE SALIDA (Markdown):
- Usa viñetas (•) para puntos principales
- Usa **negritas** para conceptos clave
- Estructura clara con subtítulos si es necesario
- Máximo 500 palabras
- Lenguaje claro y académico

GENERA EL RESUMEN:
"""

            response = model.generate_content(prompt)
            return response.text.strip()

        except Exception as e:
            print(f"❌ Error generando resumen: {e}")
            return f"Error al generar el resumen: {str(e)}"

    @staticmethod
    def generate_timeline(topic, timeline_type="academic"):
        """
        Genera una línea de tiempo interactiva usando Gemini AI
        
        Args:
            topic: Tema para generar la línea de tiempo
            timeline_type: Tipo (academic=trabajo académico, course=cronología de curso)
            
        Returns:
            dict: Estructura JSON de la línea de tiempo
        """
        try:
            print(f"⏱️ Generando timeline...")
            print(f"  📝 Tema: {topic[:100]}")
            print(f"  📋 Tipo: {timeline_type}")
            
            StudyToolsService._configure_gemini()
            print(f"  ✅ Gemini configurado")
            
            model = StudyToolsService._get_model()
            print(f"  ✅ Modelo obtenido")
            
            if timeline_type == "academic":
                instruction = """
TIPO: Línea de tiempo para un TRABAJO ACADÉMICO
Genera las FASES/PASOS que un estudiante debe seguir para completar este trabajo.
Incluye: investigación, planificación, desarrollo, revisión, entrega.
"""
            else:  # course
                instruction = """
TIPO: Línea de tiempo para un CURSO/MATERIA
Genera la CRONOLOGÍA DE TEMAS a estudiar durante el curso.
Incluye: temas secuenciales, dependencias, períodos sugeridos.
"""

            prompt = f"""
Eres un experto en planificación académica y organización del estudio.

TEMA/CURSO: "{topic}"

{instruction}

FORMATO DE SALIDA (JSON):
{{
  "title": "Nombre del proyecto/curso",
  "type": "{timeline_type}",
  "milestones": [
    {{
      "id": 1,
      "title": "Nombre de la fase/tema",
      "description": "Descripción breve",
      "duration": "Duración sugerida (ej: 1 semana, 2 días)",
      "dependencies": [],
      "tasks": [
        "Tarea específica 1",
        "Tarea específica 2"
      ],
      "order": 1
    }}
  ],
  "estimated_total_time": "Tiempo total estimado",
  "recommendations": [
    "Recomendación 1",
    "Recomendación 2"
  ]
}}

REGLAS:
1. Responde ÚNICAMENTE con el objeto JSON válido
2. Incluye entre 4-8 milestones/fases
3. Cada milestone debe tener 2-5 tareas específicas
4. Las duraciones deben ser realistas
5. Indica dependencias entre fases cuando existan
6. Recomendaciones prácticas y accionables

GENERA LA LÍNEA DE TIEMPO:
"""
            
            print(f"  🚀 Enviando a Gemini...")
            response = model.generate_content(prompt)
            print(f"  ✅ Respuesta recibida: {len(response.text)} caracteres")
            
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            print(f"  🔧 Texto limpio: {clean_text[:200]}...")
            
            timeline_data = json.loads(clean_text)
            print(f"  ✅ JSON parseado correctamente")
            
            # Validar estructura
            if 'milestones' not in timeline_data:
                raise ValueError("La línea de tiempo no tiene milestones")
            
            print(f"  ✅ Timeline generado con {len(timeline_data['milestones'])} milestones")
                
            return timeline_data

        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON de línea de tiempo: {e}")
            print(f"Respuesta: {response.text[:500]}")
            return {
                "title": "Error",
                "type": timeline_type,
                "milestones": [],
                "error": "No se pudo generar la línea de tiempo"
            }
        except Exception as e:
            print(f"❌ Error generando línea de tiempo: {e}")
            import traceback
            traceback.print_exc()
            return {
                "title": "Error",
                "type": timeline_type,
                "milestones": [],
                "error": str(e)
            }

    @staticmethod
    def analyze_syllabus(syllabus_text, course_name=""):
        """
        Analiza un syllabus usando Gemini AI y extrae información estructurada
        
        Args:
            syllabus_text: Contenido del syllabus
            course_name: Nombre del curso (opcional)
            
        Returns:
            dict: Análisis estructurado del syllabus
        """
        try:
            StudyToolsService._configure_gemini()
            model = StudyToolsService._get_model()
            
            prompt = f"""
Eres un asistente académico experto en análisis de syllabus universitarios.

CURSO: {course_name if course_name else "No especificado"}

SYLLABUS A ANALIZAR:
{syllabus_text[:8000]}

TAREA: Analiza este syllabus y extrae información estructurada.

FORMATO DE SALIDA (JSON):
{{
  "course_info": {{
    "name": "Nombre del curso",
    "description": "Descripción breve",
    "credits": "Número de créditos",
    "prerequisites": ["Prerequisito 1", "Prerequisito 2"]
  }},
  "topics": [
    {{
      "id": 1,
      "name": "Nombre del tema",
      "week": "Semana 1-2",
      "description": "Descripción del tema",
      "subtopics": ["Subtema 1", "Subtema 2"],
      "dependencies": [],
      "difficulty": "Baja|Media|Alta"
    }}
  ],
  "learning_path": {{
    "foundational_topics": ["Tema base 1", "Tema base 2"],
    "intermediate_topics": ["Tema intermedio 1"],
    "advanced_topics": ["Tema avanzado 1"]
  }},
  "dependencies_map": [
    {{
      "topic": "Tema avanzado",
      "requires": ["Tema base 1", "Tema base 2"],
      "reason": "Explicación de por qué es necesario"
    }}
  ],
  "study_recommendations": [
    "Recomendación 1",
    "Recomendación 2",
    "Recomendación 3"
  ],
  "estimated_weekly_hours": "Horas estimadas por semana",
  "assessment_methods": ["Método 1", "Método 2"],
  "key_dates": [
    {{
      "date": "Fecha aproximada",
      "event": "Examen/Entrega",
      "description": "Detalles"
    }}
  ]
}}

REGLAS:
1. Responde ÚNICAMENTE con JSON válido
2. Extrae TODOS los temas mencionados
3. Identifica dependencias entre temas lógicamente
4. Clasifica temas por dificultad
5. Proporciona recomendaciones específicas y prácticas
6. Si falta información, usa "No especificado"

GENERA EL ANÁLISIS:
"""

            response = model.generate_content(prompt)
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            
            analysis = json.loads(clean_text)
            
            # Validar estructura mínima
            if 'topics' not in analysis:
                raise ValueError("El análisis no incluye temas")
                
            return analysis

        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON del análisis: {e}")
            return {
                "error": "Error al parsear el análisis",
                "message": "La IA no generó un formato válido"
            }
        except Exception as e:
            print(f"❌ Error analizando syllabus: {e}")
            return {
                "error": "Error en el análisis",
                "message": str(e)
            }
