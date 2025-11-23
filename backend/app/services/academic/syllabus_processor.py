"""
Servicio para procesamiento inteligente de sílabos con IA
Extrae tareas, fechas y estructura académica
"""
import google.generativeai as genai
import os
import json
import re
from datetime import datetime, timedelta
from flask import current_app
from app import db
from app.models.academic import AcademicTask
from app.services.document_processing.pdf_extractor import PDFExtractor

class SyllabusProcessor:
    @staticmethod
    def _configure_gemini():
        """Configura la API de Gemini"""
        api_key = os.environ.get('GEMINI_API_KEY') or current_app.config.get('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("La API Key de Gemini no está configurada.")
        genai.configure(api_key=api_key)

    @staticmethod
    def _get_model():
        """Obtiene el modelo de Gemini con fallback seguro"""
        preferred = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
        try:
            return genai.GenerativeModel(preferred)
        except Exception:
            for candidate in ['gemini-1.5-flash', 'gemini-pro']:
                try:
                    return genai.GenerativeModel(candidate)
                except Exception:
                    continue
            # Último intento: levantar el error original del preferred
            return genai.GenerativeModel(preferred)

    @staticmethod
    def process_syllabus(user_id, course_id, file_path):
        """
        Procesa un sílabo PDF y extrae:
        - Información del curso (profesor, créditos, horario)
        - Temas/módulos del curso
        - Tareas y proyectos
        - Fechas de entrega
        """
        try:
            # 1. Extraer texto del PDF
            syllabus_text = PDFExtractor.extract_text(file_path)
            
            if not syllabus_text or len(syllabus_text) < 50:
                return {
                    "error": "El PDF no contiene texto legible", 
                    "tasks_created": 0,
                    "syllabus_analysis": {"topics": [], "course_info": {}}
                }

            # 2. Analizar con IA
            SyllabusProcessor._configure_gemini()
            model = SyllabusProcessor._get_model()
            
            # Prompt para extraer información completa del sílabo
            analysis_prompt = f"""
            Analiza este sílabo académico y extrae la siguiente información en formato JSON:
            
            SÍLABO:
            {syllabus_text[:8000]}
            
            Devuelve ÚNICAMENTE un JSON válido (sin bloques de código Markdown) con esta estructura:
            {{
                "course_info": {{
                    "professor": "Nombre del profesor",
                    "credits": "Número de créditos",
                    "schedule": "Horario de clases",
                    "department": "Departamento/Facultad"
                }},
                "topics": [
                    {{"name": "Tema 1", "description": "Descripción breve"}},
                    {{"name": "Tema 2", "description": "Descripción breve"}}
                ],
                "tasks": [
                    {{"title": "Tarea 1", "type": "tarea", "date": "2025-12-15", "priority": "alta"}},
                    {{"title": "Examen Parcial", "type": "examen", "date": "2025-12-20", "priority": "critica"}}
                ]
            }}
            
            IMPORTANTE:
            - Si no encuentras algún dato, usa un string vacío o array vacío
            - Fechas en formato YYYY-MM-DD
            - type puede ser: "tarea", "examen", "proyecto", "presentacion", "lectura"
            - priority: "baja", "media", "alta", "critica"
            """

            response = model.generate_content(analysis_prompt)
            
            # Limpieza de respuesta
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            analysis_data = json.loads(clean_text)

            # 3. Guardar tareas en base de datos
            tasks_data = analysis_data.get('tasks', [])
            tasks_created = 0
            
            for task_info in tasks_data:
                try:
                    # Validar fecha
                    due_date_str = task_info.get('date', '')
                    try:
                        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
                    except:
                        # Si falla, usar fecha futura aproximada
                        due_date = datetime.now() + timedelta(days=30)

                    new_task = AcademicTask(
                        user_id=user_id,
                        course_id=course_id,
                        title=task_info.get('title', 'Tarea sin título'),
                        description=f"Tipo: {task_info.get('type', 'tarea')}",
                        due_date=due_date,
                        priority=task_info.get('priority', 'media'),
                        status='pendiente',
                        origin='syllabus_ai'
                    )
                    db.session.add(new_task)
                    tasks_created += 1
                except Exception as e:
                    print(f"Error guardando tarea individual: {e}")
                    continue

            db.session.commit()

            # 4. Retornar análisis completo
            return {
                "message": "Sílabo procesado exitosamente",
                "tasks_created": tasks_created,
                "syllabus_analysis": {
                    "course_info": analysis_data.get('course_info', {}),
                    "topics": analysis_data.get('topics', [])
                },
                "summary": f"Se extrajeron {tasks_created} tareas y {len(analysis_data.get('topics', []))} temas del sílabo"
            }

        except json.JSONDecodeError as e:
            print(f"Error de JSON: {e}")
            return {
                "error": "La IA no devolvió un formato válido", 
                "tasks_created": 0,
                "syllabus_analysis": {"topics": [], "course_info": {}}
            }
        except Exception as e:
            print(f"Error procesando sílabo: {e}")
            db.session.rollback()
            return {
                "error": str(e), 
                "tasks_created": 0,
                "syllabus_analysis": {"topics": [], "course_info": {}}
            }
