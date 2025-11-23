from flask import Blueprint, request, jsonify, send_file
from app import db
from app.models.academic import AcademicCourse, AcademicTask
from app.models.syllabus import SyllabusAnalysis
from app.models.user import User
from app.models.timeline import Timeline
import os
from io import BytesIO
import json
from datetime import datetime

# Importaciones de servicios de IA - ACTIVAS CON TODAS LAS DEPENDENCIAS INSTALADAS
try:
    from app.services.academic.syllabus_processor import SyllabusProcessor
    SYLLABUS_PROCESSOR_AVAILABLE = True
    print("✅ SyllabusProcessor disponible")
except Exception as e:
    print(f"⚠️  SyllabusProcessor no disponible: {e}")
    SYLLABUS_PROCESSOR_AVAILABLE = False

try:
    from app.services.academic.study_tools import StudyToolsService
    STUDY_TOOLS_AVAILABLE = True
    print("✅ StudyToolsService disponible")
except Exception as e:
    print(f"⚠️  StudyToolsService no disponible: {e}")
    STUDY_TOOLS_AVAILABLE = False

try:
    from app.services.pdf_generator import PDFGenerator
    PDF_GENERATOR_AVAILABLE = True
    print("✅ PDFGenerator disponible")
except Exception as e:
    print(f"⚠️  PDFGenerator no disponible: {e}")
    PDF_GENERATOR_AVAILABLE = False

try:
    from app.utils.file_handler import FileHandler
    FILE_HANDLER_AVAILABLE = True
    print("✅ FileHandler disponible")
except Exception as e:
    print(f"⚠️  FileHandler no disponible: {e}")
    FILE_HANDLER_AVAILABLE = False

# Definimos el Blueprint
academic_bp = Blueprint('academic', __name__, url_prefix='/api/academic')

# --- 1. GESTIÓN DE CURSOS (Dashboard) ---

@academic_bp.route('/courses', methods=['POST'])
@academic_bp.route('/course/create', methods=['POST'])
def create_course():
    try:
        data = request.json
        user_id = int(data['user_id'])

        # Verificar/crear usuario de desarrollo si no existe (evita error de FK)
        user = User.query.get(user_id)
        if not user:
            dev_email = f"dev{user_id}@example.com"
            dev_username = f"dev_user_{user_id}"
            user = User(
                email=dev_email,
                username=dev_username,
                password='dev1234',
                first_name='Dev',
                last_name='User'
            )
            try:
                user.id = user_id
            except Exception:
                pass
            db.session.add(user)
            db.session.flush()

        new_course = AcademicCourse(
            user_id=user.id,
            name=data['name'],
            code=data.get('code'),
            professor=data.get('professor'),
            schedule_info=data.get('schedule'),
            category=data.get('category', 'general'),
            icon=data.get('icon', 'BookOpen'),
            color=data.get('color', 'blue')
        )
        db.session.add(new_course)
        db.session.commit()
        return jsonify({"message": "Curso creado", "id": new_course.id, "course": new_course.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@academic_bp.route('/user/<int:user_id>/dashboard', methods=['GET'])
@academic_bp.route('/user/<int:user_id>/courses', methods=['GET'])
def get_academic_dashboard(user_id):
    try:
        courses = AcademicCourse.query.filter_by(user_id=user_id).all()
        # Tareas pendientes
        tasks = AcademicTask.query.filter_by(user_id=user_id, status='pendiente')\
                .order_by(AcademicTask.due_date.asc()).all()
        
        return jsonify({
            "courses": [c.to_dict() for c in courses],
            "pending_tasks": [t.to_dict() for t in tasks]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 2. SUBIDA DE SÍLABOS (PDF) ---

# --- 3. NUEVAS HERRAMIENTAS IA (Mapas y Resúmenes) ---

@academic_bp.route('/tools/mindmap', methods=['POST'])
def create_mindmap():
    if not STUDY_TOOLS_AVAILABLE:
        return jsonify({"error": "Servicio de herramientas de estudio no disponible"}), 503
    
    data = request.json
    text = data.get('text')
    context = data.get('context', 'General') 
    
    if not text:
        return jsonify({"error": "El texto es obligatorio"}), 400

    try:
        result = StudyToolsService.generate_mind_map(text, context)
        return jsonify({"mindmap": result})
    except Exception as e:
        print(f"Error generando mapa: {e}")
        return jsonify({"error": "Error interno en la IA"}), 500

@academic_bp.route('/tools/summary', methods=['POST'])
def create_summary():
    if not STUDY_TOOLS_AVAILABLE:
        return jsonify({"error": "Servicio de herramientas de estudio no disponible"}), 503
    
    data = request.json
    text = data.get('text')
    summary_type = data.get('type', 'general')  # general, ejecutivo, detallado
    
    if not text:
        return jsonify({"error": "El texto es obligatorio"}), 400

    try:
        result = StudyToolsService.generate_summary(text, summary_type)
        return jsonify({"summary": result})
    except Exception as e:
        return jsonify({"error": "Error interno en la IA"}), 500

@academic_bp.route('/tools/timeline', methods=['POST'])
def create_timeline():
    """Genera una línea de tiempo para un proyecto/curso y opcionalmente la guarda"""
    if not STUDY_TOOLS_AVAILABLE:
        return jsonify({"error": "Servicio de herramientas de estudio no disponible"}), 503
    
    data = request.json
    topic = data.get('topic')
    timeline_type = data.get('type', 'academic')  # academic o course
    user_id = data.get('user_id')
    project_id = data.get('project_id')
    course_id = data.get('course_id')
    save_timeline = data.get('save', False)  # Si debe guardarse en BD
    
    if not topic:
        return jsonify({"error": "El tema es obligatorio"}), 400
    
    try:
        # Generar la línea de tiempo con IA
        result = StudyToolsService.generate_timeline(topic, timeline_type)
        
        # Si se debe guardar y se proporciona user_id
        if save_timeline and user_id:
            # Preparar los pasos en el formato correcto
            steps = []
            if isinstance(result, dict) and 'steps' in result:
                steps = result['steps']
            elif isinstance(result, list):
                steps = result
            else:
                # Intentar parsear si es string
                try:
                    parsed = json.loads(result) if isinstance(result, str) else result
                    steps = parsed.get('steps', parsed) if isinstance(parsed, dict) else parsed
                except:
                    steps = []
            
            # Asegurar que cada paso tenga 'completed': false
            for step in steps:
                if 'completed' not in step:
                    step['completed'] = False
            
            # Crear el registro en la BD
            new_timeline = Timeline(
                user_id=user_id,
                project_id=project_id,
                course_id=course_id,
                title=topic,
                description=f"Línea de tiempo generada para {timeline_type}",
                timeline_type=timeline_type,
                steps_json=json.dumps(steps)
            )
            
            db.session.add(new_timeline)
            db.session.commit()
            
            return jsonify({
                "timeline": result,
                "saved": True,
                "timeline_id": new_timeline.id,
                "timeline_data": new_timeline.to_dict()
            })
        
        return jsonify({"timeline": result, "saved": False})
        
    except Exception as e:
        db.session.rollback()
        print(f"Error generando línea de tiempo: {e}")
        return jsonify({"error": "Error interno en la IA"}), 500

@academic_bp.route('/tools/analyze-syllabus', methods=['POST'])
def analyze_syllabus():
    """Analiza un syllabus con IA y extrae información estructurada"""
    if not STUDY_TOOLS_AVAILABLE:
        return jsonify({"error": "Servicio de herramientas de estudio no disponible"}), 503
    
    data = request.json
    syllabus_text = data.get('text')
    course_name = data.get('course_name', '')
    
    if not syllabus_text:
        return jsonify({"error": "El texto del syllabus es obligatorio"}), 400
    
    try:
        result = StudyToolsService.analyze_syllabus(syllabus_text, course_name)
        
        # Si hay error en el análisis, retornar 400
        if 'error' in result:
            return jsonify(result), 400
            
        return jsonify({"analysis": result})
    except Exception as e:
        print(f"Error analizando syllabus: {e}")
        return jsonify({"error": "Error interno en la IA"}), 500
    
    # ... (código anterior) ...

# --- 4. GESTIÓN DE TAREAS (NUEVO: Completar y Borrar) ---

@academic_bp.route('/task/<int:task_id>/toggle', methods=['PUT'])
def toggle_task_status(task_id):
    try:
        task = AcademicTask.query.get(task_id)
        if not task:
            return jsonify({"error": "Tarea no encontrada"}), 404
        
        # Cambiar estado
        if task.status == 'completada':
            task.status = 'pendiente'
            task.is_completed = False # Si tienes este campo booleano
        else:
            task.status = 'completada'
            task.is_completed = True
            
        db.session.commit()
        return jsonify(task.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@academic_bp.route('/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = AcademicTask.query.get(task_id)
        if not task:
            return jsonify({"error": "Tarea no encontrada"}), 404
            
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Tarea eliminada"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 5. GESTIÓN DE CURSOS (Actualizar y Eliminar) ---

@academic_bp.route('/course/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """Actualiza información de un curso"""
    try:
        course = AcademicCourse.query.get(course_id)
        if not course:
            return jsonify({"error": "Curso no encontrado"}), 404
        
        data = request.json
        if 'name' in data:
            course.name = data['name']
        if 'code' in data:
            course.code = data['code']
        if 'professor' in data:
            course.professor = data['professor']
        if 'schedule' in data or 'schedule_info' in data:
            course.schedule_info = data.get('schedule') or data.get('schedule_info')
        if 'category' in data:
            course.category = data['category']
        if 'icon' in data:
            course.icon = data['icon']
        if 'color' in data:
            course.color = data['color']
        
        db.session.commit()
        return jsonify({"message": "Curso actualizado", "course": course.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@academic_bp.route('/course/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """Elimina un curso y todas sus tareas asociadas"""
    try:
        course = AcademicCourse.query.get(course_id)
        if not course:
            return jsonify({"error": "Curso no encontrado"}), 404
        
        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": "Curso eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# --- 6. ESTADÍSTICAS ---

@academic_bp.route('/user/<int:user_id>/stats', methods=['GET'])
def get_user_stats(user_id):
    """Obtiene estadísticas generales del usuario"""
    try:
        total_courses = AcademicCourse.query.filter_by(user_id=user_id).count()
        total_tasks = AcademicTask.query.filter_by(user_id=user_id).count()
        completed_tasks = AcademicTask.query.filter_by(user_id=user_id, status='completada').count()
        pending_tasks = AcademicTask.query.filter_by(user_id=user_id, status='pendiente').count()
        
        # Tareas por prioridad
        critical_tasks = AcademicTask.query.filter_by(user_id=user_id, priority='critica', status='pendiente').count()
        high_tasks = AcademicTask.query.filter_by(user_id=user_id, priority='alta', status='pendiente').count()
        
        return jsonify({
            "total_courses": total_courses,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "critical_tasks": critical_tasks,
            "high_priority_tasks": high_tasks,
            "completion_rate": round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 2)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 7. EXPORTACIÓN A PDF ---

@academic_bp.route('/export-syllabus-pdf', methods=['POST'])
def export_syllabus_pdf():
    """Genera y descarga un PDF con el análisis del syllabus"""
    if not PDF_GENERATOR_AVAILABLE:
        return jsonify({"error": "Servicio de generación de PDF no disponible"}), 503
    
    try:
        data = request.json
        analysis = data.get('analysis')
        course_name = data.get('course_name', 'Análisis de Syllabus')
        
        if not analysis:
            return jsonify({"error": "Análisis no proporcionado"}), 400
        
        # Generar PDF
        pdf_content = PDFGenerator.generate_syllabus_analysis_pdf(analysis, course_name)
        
        # Crear BytesIO para enviar
        pdf_buffer = BytesIO(pdf_content)
        pdf_buffer.seek(0)
        
        # Enviar archivo
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'analisis_syllabus_{course_name.replace(" ", "_")}.pdf'
        )
        
    except Exception as e:
        print(f"Error exportando PDF: {e}")
        return jsonify({"error": str(e)}), 500

# --- 8. GESTIÓN DE ANÁLISIS DE SÍLABOS (NUEVO) ---

@academic_bp.route('/user/<int:user_id>/syllabus-history', methods=['GET'])
def get_syllabus_history(user_id):
    """Obtiene el historial de análisis de sílabos del usuario"""
    try:
        analyses = SyllabusAnalysis.query.filter_by(user_id=user_id)\
                    .order_by(SyllabusAnalysis.uploaded_at.desc()).all()
        
        return jsonify({
            "syllabus_list": [analysis.to_dict() for analysis in analyses]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@academic_bp.route('/syllabus/<int:syllabus_id>', methods=['GET'])
def get_syllabus_details(syllabus_id):
    """Obtiene los detalles completos de un análisis de sílabo"""
    try:
        analysis = SyllabusAnalysis.query.get(syllabus_id)
        if not analysis:
            return jsonify({"error": "Análisis no encontrado"}), 404
        
        return jsonify(analysis.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@academic_bp.route('/syllabus/<int:syllabus_id>/topic/<int:topic_index>/toggle', methods=['PUT'])
def toggle_syllabus_topic(syllabus_id, topic_index):
    """Marca/desmarca un tema del sílabo como completado"""
    try:
        analysis = SyllabusAnalysis.query.get(syllabus_id)
        if not analysis:
            return jsonify({"error": "Análisis no encontrado"}), 404
        
        if analysis.toggle_topic_complete(topic_index):
            db.session.commit()
            return jsonify({
                "message": "Tema actualizado",
                "syllabus": analysis.to_dict()
            }), 200
        else:
            return jsonify({"error": "Índice de tema inválido"}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@academic_bp.route('/syllabus/<int:syllabus_id>', methods=['DELETE'])
def delete_syllabus(syllabus_id):
    """Elimina un análisis de sílabo"""
    try:
        analysis = SyllabusAnalysis.query.get(syllabus_id)
        if not analysis:
            return jsonify({"error": "Análisis no encontrado"}), 404
        
        # Opcionalmente eliminar el archivo físico
        if analysis.file_path and os.path.exists(analysis.file_path):
            try:
                os.remove(analysis.file_path)
            except:
                pass
        
        db.session.delete(analysis)
        db.session.commit()
        return jsonify({"message": "Análisis eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@academic_bp.route('/course/<int:course_id>/upload-syllabus', methods=['POST'])
def upload_syllabus_improved(course_id):
    """
    Versión mejorada de upload-syllabus que siempre guarda el análisis en la BD
    Aunque SyllabusProcessor no esté disponible, guarda información básica
    """
    if 'file' not in request.files:
        return jsonify({"error": "No se envió ningún archivo"}), 400
    
    file = request.files['file']
    user_id = request.form.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id es requerido"}), 400
    
    try:
        # Guardar archivo
        if FILE_HANDLER_AVAILABLE:
            upload_folder = FileHandler.get_upload_path('syllabi')
            saved_info = FileHandler.save_file(file, upload_folder, prefix=f"syllabus_{course_id}")
            file_path = saved_info['filepath']
            file_name = saved_info['filename']
        else:
            # Fallback manual
            upload_folder = os.path.join('uploads', 'syllabi')
            os.makedirs(upload_folder, exist_ok=True)
            file_name = f"syllabus_{course_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            file_path = os.path.join(upload_folder, file_name)
            file.save(file_path)
        
        # Intentar procesar con IA si está disponible
        analysis_result = {}
        topics = []
        course_info = {}
        tasks_created = 0
        
        if SYLLABUS_PROCESSOR_AVAILABLE:
            try:
                result = SyllabusProcessor.process_syllabus(user_id, course_id, file_path)
                analysis_result = result.get('syllabus_analysis', {})
                topics = analysis_result.get('topics', [])
                course_info = analysis_result.get('course_info', {})
                tasks_created = result.get('tasks_created', 0)
            except Exception as e:
                print(f"Error procesando con IA: {e}")
                # Continuar sin análisis de IA
        
        # Crear registro en la BD
        new_analysis = SyllabusAnalysis(
            user_id=int(user_id),
            course_id=course_id,
            file_path=file_path,
            file_name=file_name
        )
        
        # Guardar información si fue analizada
        if course_info:
            new_analysis.set_course_info(course_info)
        if topics:
            # Asegurar que cada tema tenga el campo 'completed'
            for topic in topics:
                if 'completed' not in topic:
                    topic['completed'] = False
            new_analysis.set_topics(topics)
        
        db.session.add(new_analysis)
        db.session.commit()
        
        return jsonify({
            "message": "Sílabo cargado exitosamente",
            "syllabus_id": new_analysis.id,
            "syllabus_analysis": analysis_result,
            "tasks_created": tasks_created,
            "ai_processed": SYLLABUS_PROCESSOR_AVAILABLE
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error en upload_syllabus_improved: {e}")
        return jsonify({"error": str(e)}), 500
