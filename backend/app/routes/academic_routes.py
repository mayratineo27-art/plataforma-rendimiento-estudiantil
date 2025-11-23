from flask import Blueprint, request, jsonify
from app import db
from app.models.academic import AcademicCourse, AcademicTask
# Importamos los servicios de IA
from app.services.academic.syllabus_processor import SyllabusProcessor
from app.services.academic.study_tools import StudyToolsService 
from app.utils.file_handler import FileHandler 
import os

# Definimos el Blueprint
academic_bp = Blueprint('academic', __name__, url_prefix='/api/academic')

# --- 1. GESTIÓN DE CURSOS (Dashboard) ---

@academic_bp.route('/courses', methods=['POST'])
def create_course():
    try:
        data = request.json
        new_course = AcademicCourse(
            user_id=data['user_id'],
            name=data['name'],
            professor=data.get('professor'),
            schedule_info=data.get('schedule_info'),
            color=data.get('color', '#3B82F6')
        )
        db.session.add(new_course)
        db.session.commit()
        return jsonify({"message": "Curso creado", "id": new_course.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@academic_bp.route('/user/<int:user_id>/dashboard', methods=['GET'])
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

@academic_bp.route('/course/<int:course_id>/upload-syllabus', methods=['POST'])
def upload_syllabus(course_id):
    if 'file' not in request.files:
        return jsonify({"error": "No se envió ningún archivo"}), 400
    
    file = request.files['file']
    user_id = request.form.get('user_id')
    
    try:
        # Guardar archivo temporalmente
        file_path = FileHandler.save_file(file, subfolder="syllabi")
        
        # Procesar con IA
        result = SyllabusProcessor.process_syllabus(user_id, course_id, file_path)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 3. NUEVAS HERRAMIENTAS IA (Mapas y Resúmenes) ---

@academic_bp.route('/tools/mindmap', methods=['POST'])
def create_mindmap():
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
    """Genera una línea de tiempo para un proyecto/curso"""
    data = request.json
    topic = data.get('topic')
    timeline_type = data.get('type', 'academic')  # academic o course
    
    if not topic:
        return jsonify({"error": "El tema es obligatorio"}), 400
    
    try:
        result = StudyToolsService.generate_timeline(topic, timeline_type)
        return jsonify({"timeline": result})
    except Exception as e:
        print(f"Error generando línea de tiempo: {e}")
        return jsonify({"error": "Error interno en la IA"}), 500

@academic_bp.route('/tools/analyze-syllabus', methods=['POST'])
def analyze_syllabus():
    """Analiza un syllabus con IA y extrae información estructurada"""
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
        if 'professor' in data:
            course.professor = data['professor']
        if 'schedule_info' in data:
            course.schedule_info = data['schedule_info']
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
