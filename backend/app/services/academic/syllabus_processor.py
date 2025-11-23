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
    def process_syllabus(user_id, course_id, file_path):
        """
        Procesa un sílabo PDF y extrae:
        - Tareas y proyectos
        - Fechas de entrega
        - Estructura del curso
        """
        try:
            # 1. Extraer texto del PDF
            syllabus_text = PDFExtractor.extract_text(file_path)
            
            if not syllabus_text or len(syllabus_text) < 50:
                return {"error": "El PDF no contiene texto legible", "tasks_created": 0}

            # 2. Analizar con IA
            SyllabusProcessor._configure_gemini()
            model_name = os.environ.get('GEMINI_MODEL', 'gemini-pro')
            model = genai.GenerativeModel(model_name)
            
            prompt = f"""
            Eres un asistente académico experto. Analiza este sílabo y extrae TODAS las tareas, exámenes, proyectos y entregas mencionadas.
            
            SÍLABO:
            {syllabus_text[:8000]}
            
            INSTRUCCIONES:
            1. Devuelve ÚNICAMENTE un array JSON válido (sin bloques de código Markdown).
            2. Cada elemento debe tener: "title", "type", "date", "priority"
            3. type puede ser: "tarea", "examen", "proyecto", "presentacion", "lectura"
            4. date en formato YYYY-MM-DD (si no hay fecha exacta, usa fecha aproximada futura)
            5. priority: "baja", "media", "alta", "critica"
            
            EJEMPLO DE SALIDA:
            [
                {{"title": "Ensayo sobre IA", "type": "tarea", "date": "2025-12-15", "priority": "alta"}},
                {{"title": "Examen Parcial 1", "type": "examen", "date": "2025-12-20", "priority": "critica"}}
            ]
            """

            response = model.generate_content(prompt)
            
            # Limpieza de respuesta
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            tasks_data = json.loads(clean_text)

            # 3. Guardar en base de datos
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

            return {
                "message": "Sílabo procesado exitosamente",
                "tasks_created": tasks_created,
                "summary": f"Se extrajeron {tasks_created} tareas del sílabo"
            }

        except json.JSONDecodeError as e:
            print(f"Error de JSON: {e}")
            return {"error": "La IA no devolvió un formato válido", "tasks_created": 0}
        except Exception as e:
            print(f"Error procesando sílabo: {e}")
            db.session.rollback()
            return {"error": str(e), "tasks_created": 0}
