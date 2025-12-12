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

@academic_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    """Obtener detalles de un curso específico"""
    try:
        course = AcademicCourse.query.get(course_id)
        if not course:
            return jsonify({"error": "Curso no encontrado"}), 404
        
        return jsonify({"course": course.to_dict()}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@academic_bp.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    """Actualizar un curso existente"""
    try:
        course = AcademicCourse.query.get(course_id)
        if not course:
            return jsonify({"error": "Curso no encontrado"}), 404
        
        data = request.json
        
        # Actualizar campos si están presentes
        if 'name' in data:
            course.name = data['name']
        if 'code' in data:
            course.code = data['code']
        if 'professor' in data:
            course.professor = data['professor']
        if 'schedule' in data:
            course.schedule_info = data['schedule']
        if 'category' in data:
            course.category = data['category']
        if 'icon' in data:
            course.icon = data['icon']
        if 'color' in data:
            course.color = data['color']
        
        db.session.commit()
        
        return jsonify({
            "message": "Curso actualizado exitosamente",
            "course": course.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@academic_bp.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """Eliminar un curso"""
    try:
        course = AcademicCourse.query.get(course_id)
        if not course:
            return jsonify({"error": "Curso no encontrado"}), 404
        
        db.session.delete(course)
        db.session.commit()
        
        return jsonify({"message": "Curso eliminado exitosamente"}), 200
        
    except Exception as e:
        db.session.rollback()
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
        print(f"📊 Generando mapa mental. Texto: {text[:100]}... Contexto: {context}")
        result = StudyToolsService.generate_mind_map(text, context)
        print(f"✅ Mapa mental generado exitosamente")
        return jsonify({"mindmap": result})
    except Exception as e:
        print(f"❌ Error generando mapa mental: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error interno en la IA: {str(e)}"}), 500

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
        print(f"📝 Generando resumen. Tipo: {summary_type}, Texto: {text[:100]}...")
        result = StudyToolsService.generate_summary(text, summary_type)
        print(f"✅ Resumen generado exitosamente")
        return jsonify({"summary": result})
    except Exception as e:
        print(f"❌ Error generando resumen: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error interno en la IA: {str(e)}"}), 500

@academic_bp.route('/tools/timeline', methods=['POST'])
def create_timeline():
    """Genera una línea de tiempo para un proyecto/curso y opcionalmente la guarda
    
    Parámetros:
    - topic: Tema de la línea de tiempo (requerido)
    - type: Tipo de timeline (academic, course, project, free) - default: 'free'
    - user_id: ID del usuario (requerido si save=True)
    - project_id: ID del proyecto (opcional)
    - course_id: ID del curso (opcional - permite crear sin curso)
    - save: Si debe guardarse en BD (default: False)
    """
    if not STUDY_TOOLS_AVAILABLE:
        return jsonify({"error": "Servicio de herramientas de estudio no disponible"}), 503
    
    data = request.json
    topic = data.get('topic')
    timeline_type = data.get('type', 'free')  # Por defecto 'free' para timelines sin curso
    user_id = data.get('user_id')
    project_id = data.get('project_id')
    course_id = data.get('course_id')  # Ahora es completamente opcional
    save_timeline = data.get('save', False)
    
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
            
            # Determinar descripción según el contexto
            if course_id:
                description = f"Línea de tiempo generada para el curso"
            elif project_id:
                description = f"Línea de tiempo generada para el proyecto"
            else:
                description = f"Línea de tiempo libre sobre {topic}"
            
            # Crear el registro en la BD (course_id ahora puede ser None)
            new_timeline = Timeline(
                user_id=user_id,
                project_id=project_id,
                course_id=course_id,  # Puede ser None - sin curso asociado
                title=topic,
                description=description,
                timeline_type=timeline_type,
                course_topic=topic if not course_id else None,  # Guardar tema si no hay curso
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
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Error interno: {str(e)}"}), 500

@academic_bp.route('/timelines/history', methods=['GET'])
def get_timeline_history():
    """Obtiene el historial de líneas de tiempo del usuario
    
    Query params:
    - user_id: ID del usuario (requerido)
    - course_id: Filtrar por curso (opcional)
    - timeline_type: Filtrar por tipo (optional)
    - is_completed: Filtrar por completadas (true/false, opcional)
    - limit: Cantidad máxima de resultados (default: 50)
    """
    user_id = request.args.get('user_id', type=int)
    course_id = request.args.get('course_id', type=int)
    timeline_type = request.args.get('timeline_type')
    is_completed = request.args.get('is_completed')
    limit = request.args.get('limit', 50, type=int)
    
    if not user_id:
        return jsonify({"error": "user_id es requerido"}), 400
    
    try:
        # Construcción de query con filtros
        query = Timeline.query.filter_by(user_id=user_id, is_visible=True)
        
        # Filtrar por curso si se proporciona
        if course_id is not None:
            query = query.filter_by(course_id=course_id)
        
        # Filtrar por tipo si se proporciona
        if timeline_type:
            query = query.filter_by(timeline_type=timeline_type)
        
        # Filtrar por estado completado
        if is_completed is not None:
            is_completed_bool = is_completed.lower() == 'true'
            query = query.filter_by(is_completed=is_completed_bool)
        
        # Ordenar por fecha de creación (más recientes primero)
        timelines = query.order_by(Timeline.created_at.desc()).limit(limit).all()
        
        return jsonify({
            "timelines": [t.to_dict() for t in timelines],
            "total": len(timelines)
        })
    
    except Exception as e:
        print(f"Error obteniendo historial de timelines: {e}")
        return jsonify({"error": "Error al obtener historial"}), 500


@academic_bp.route('/timelines/<int:timeline_id>', methods=['GET'])
def get_timeline_detail(timeline_id):
    """Obtiene los detalles de una línea de tiempo específica"""
    try:
        timeline = Timeline.query.get(timeline_id)
        
        if not timeline:
            return jsonify({"error": "Línea de tiempo no encontrada"}), 404
        
        return jsonify(timeline.to_dict())
    
    except Exception as e:
        print(f"Error obteniendo timeline: {e}")
        return jsonify({"error": "Error al obtener timeline"}), 500


@academic_bp.route('/timelines/<int:timeline_id>', methods=['DELETE'])
def delete_timeline(timeline_id):
    """Elimina una línea de tiempo del historial (soft delete - marca como no visible)"""
    try:
        timeline = Timeline.query.get(timeline_id)
        
        if not timeline:
            return jsonify({"error": "Línea de tiempo no encontrada"}), 404
        
        # Soft delete - solo marca como no visible
        timeline.is_visible = False
        db.session.commit()
        
        return jsonify({
            "message": "Línea de tiempo eliminada exitosamente",
            "timeline_id": timeline_id
        })
    
    except Exception as e:
        db.session.rollback()
        print(f"Error eliminando timeline: {e}")
        return jsonify({"error": "Error al eliminar timeline"}), 500


@academic_bp.route('/timelines/<int:timeline_id>/permanent', methods=['DELETE'])
def delete_timeline_permanent(timeline_id):
    """Elimina permanentemente una línea de tiempo del historial"""
    try:
        timeline = Timeline.query.get(timeline_id)
        
        if not timeline:
            return jsonify({"error": "Línea de tiempo no encontrada"}), 404
        
        # Eliminación permanente
        db.session.delete(timeline)
        db.session.commit()
        
        return jsonify({
            "message": "Línea de tiempo eliminada permanentemente",
            "timeline_id": timeline_id
        })
    
    except Exception as e:
        db.session.rollback()
        print(f"Error eliminando timeline permanentemente: {e}")
        return jsonify({"error": "Error al eliminar timeline"}), 500


@academic_bp.route('/timelines/cleanup', methods=['POST'])
def cleanup_old_timelines():
    """Limpia timelines antiguas o no visibles del historial
    
    Body params:
    - user_id: ID del usuario (requerido)
    - days_old: Eliminar timelines con más de X días (default: 90)
    - delete_completed: Eliminar completadas (default: false)
    - permanent: Eliminación permanente vs soft delete (default: false)
    """
    data = request.json
    user_id = data.get('user_id')
    days_old = data.get('days_old', 90)
    delete_completed = data.get('delete_completed', False)
    permanent = data.get('permanent', False)
    
    if not user_id:
        return jsonify({"error": "user_id es requerido"}), 400
    
    try:
        # Calcular fecha límite
        from datetime import timedelta
        date_limit = datetime.utcnow() - timedelta(days=days_old)
        
        # Query base
        query = Timeline.query.filter(
            Timeline.user_id == user_id,
            Timeline.created_at < date_limit
        )
        
        # Filtrar por completadas si se solicita
        if delete_completed:
            query = query.filter_by(is_completed=True)
        
        timelines = query.all()
        count = len(timelines)
        
        if permanent:
            # Eliminación permanente
            for timeline in timelines:
                db.session.delete(timeline)
        else:
            # Soft delete
            for timeline in timelines:
                timeline.is_visible = False
        
        db.session.commit()
        
        return jsonify({
            "message": f"{count} líneas de tiempo {'eliminadas permanentemente' if permanent else 'ocultadas'}",
            "count": count
        })
    
    except Exception as e:
        db.session.rollback()
        print(f"Error limpiando timelines: {e}")
        return jsonify({"error": "Error al limpiar historial"}), 500


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


# --- 8. EVALUACIÓN DE ESCRITURA ---

try:
    from app.services.academic.writing_evaluator import WritingEvaluator
    WRITING_EVALUATOR_AVAILABLE = True
    print("✅ WritingEvaluator disponible")
except Exception as e:
    print(f"⚠️  WritingEvaluator no disponible: {e}")
    WRITING_EVALUATOR_AVAILABLE = False


@academic_bp.route('/tools/evaluate-writing', methods=['POST'])
def evaluate_writing():
    """
    Evalúa la calidad de escritura de un documento
    
    Acepta:
    - document: Archivo actual (TXT, PDF, DOCX)
    - previous_document: Archivo anterior para comparar (opcional)
    - user_id: ID del usuario
    - course_id: ID del curso (opcional)
    - save_to_history: Si guardar en historial (default: true)
    
    Retorna:
    - Reporte con métricas, scores y recomendaciones
    - ID de evaluación guardada
    """
    try:
        print("=" * 80)
        print("📝 ENDPOINT: Evaluate Writing")
        print("=" * 80)
        
        if not WRITING_EVALUATOR_AVAILABLE:
            return jsonify({
                "error": "Servicio de evaluación de escritura no disponible"
            }), 503
        
        # Validar que se envió un archivo
        if 'document' not in request.files:
            return jsonify({"error": "No se envió ningún documento"}), 400
        
        current_file = request.files['document']
        previous_file = request.files.get('previous_document')
        
        if current_file.filename == '':
            return jsonify({"error": "Nombre de archivo vacío"}), 400
        
        # Validar extensión
        allowed_extensions = {'.txt', '.pdf', '.docx', '.md'}
        current_ext = os.path.splitext(current_file.filename)[1].lower()
        
        if current_ext not in allowed_extensions:
            return jsonify({
                "error": f"Formato no soportado: {current_ext}. Use: {', '.join(allowed_extensions)}"
            }), 400
        
        print(f"📄 Archivo recibido: {current_file.filename}")
        
        # Obtener metadatos
        user_id = request.form.get('user_id', type=int)
        course_id = request.form.get('course_id', type=int)
        save_to_history = request.form.get('save_to_history', 'true').lower() == 'true'
        
        print(f"👤 Usuario: {user_id}, 📚 Curso: {course_id}, 💾 Guardar: {save_to_history}")
        
        # Crear carpeta para guardar archivos
        upload_dir = os.path.join('uploads', 'writing')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generar nombres únicos
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        current_filename = f"current_{timestamp}_{current_file.filename}"
        current_path = os.path.join(upload_dir, current_filename)
        
        # Guardar archivo actual
        current_file.save(current_path)
        print(f"💾 Guardado: {current_path}")
        
        # Guardar archivo anterior si existe
        previous_path = None
        if previous_file and previous_file.filename != '':
            previous_ext = os.path.splitext(previous_file.filename)[1].lower()
            
            if previous_ext in allowed_extensions:
                previous_filename = f"previous_{timestamp}_{previous_file.filename}"
                previous_path = os.path.join(upload_dir, previous_filename)
                previous_file.save(previous_path)
                print(f"💾 Guardado (anterior): {previous_path}")
            else:
                print(f"⚠️  Archivo anterior ignorado (formato inválido)")
        
        # Generar reporte
        metadata = {
            'user_id': user_id,
            'course_id': course_id,
            'timestamp': timestamp
        }
        
        report = WritingEvaluator.generate_report(
            current_file=current_path,
            previous_file=previous_path,
            metadata=metadata
        )
        
        # Guardar en base de datos si se solicita
        evaluation_id = None
        if save_to_history and user_id:
            try:
                from app.models.writing_evaluation import WritingEvaluation
                
                evaluation = WritingEvaluation(
                    user_id=user_id,
                    course_id=course_id,
                    file_name=current_file.filename,
                    file_path=current_path,
                    previous_file_path=previous_path,
                    
                    # Métricas del documento
                    word_count=report['metrics']['current']['word_count'],
                    sentence_count=report['metrics']['current']['sentence_count'],
                    paragraph_count=report['metrics']['current']['paragraph_count'],
                    vocabulary_size=report['metrics']['current']['vocabulary_size'],
                    readability_score=report['metrics']['current']['readability_score'],
                    
                    # Scores de evaluación
                    overall_score=report['evaluation']['overall_score'],
                    grammar_score=report['evaluation']['grammar_score'],
                    coherence_score=report['evaluation']['coherence_score'],
                    vocabulary_score=report['evaluation']['vocabulary_score'],
                    structure_score=report['evaluation']['structure_score'],
                    
                    # Análisis adicional
                    tone_analysis=report['evaluation'].get('tone_analysis'),
                    formality_score=report['evaluation'].get('formality_score'),
                    complexity_level=report['evaluation'].get('complexity_level'),
                    
                    # Comparación
                    improvement_percentage=report['evaluation'].get('improvement_percentage'),
                    improvements_made=report['evaluation'].get('improvements_made'),
                    
                    # Feedback
                    strengths=report['evaluation']['strengths'],
                    weaknesses=report['evaluation']['weaknesses'],
                    recommendations=report['evaluation']['recommendations'],
                    specific_errors=report['evaluation'].get('specific_errors'),
                    suggestions=report['evaluation'].get('suggestions'),
                    summary=report['evaluation']['summary'],
                    
                    # Métricas adicionales
                    additional_metrics=report['metrics']
                )
                
                db.session.add(evaluation)
                db.session.commit()
                evaluation_id = evaluation.id
                
                print(f"✅ Evaluación guardada en BD con ID: {evaluation_id}")
                
            except Exception as e:
                print(f"⚠️  Error guardando en BD: {e}")
                db.session.rollback()
        
        print(f"✅ Reporte generado exitosamente")
        
        return jsonify({
            "message": "Evaluación completada",
            "report": report,
            "evaluation_id": evaluation_id,
            "saved_to_history": save_to_history and evaluation_id is not None
        }), 200
        
    except Exception as e:
        print(f"❌ Error evaluando escritura: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@academic_bp.route('/tools/writing-history/<int:user_id>', methods=['GET'])
def get_writing_history(user_id):
    """
    Obtiene el historial de evaluaciones de escritura de un usuario
    
    Query params:
    - course_id: Filtrar por curso (opcional)
    - limit: Número máximo de resultados (default: 50)
    - offset: Para paginación (default: 0)
    
    Retorna:
    - Lista de evaluaciones con resumen
    """
    try:
        from app.models.writing_evaluation import WritingEvaluation
        
        # Parámetros de consulta
        course_id = request.args.get('course_id', type=int)
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Construir query
        query = WritingEvaluation.query.filter_by(user_id=user_id)
        
        if course_id:
            query = query.filter_by(course_id=course_id)
        
        # Ordenar por fecha descendente
        query = query.order_by(WritingEvaluation.evaluated_at.desc())
        
        # Paginación
        total = query.count()
        evaluations = query.limit(limit).offset(offset).all()
        
        return jsonify({
            "total": total,
            "limit": limit,
            "offset": offset,
            "evaluations": [eval.to_summary_dict() for eval in evaluations]
        }), 200
        
    except Exception as e:
        print(f"❌ Error obteniendo historial: {e}")
        return jsonify({"error": str(e)}), 500


@academic_bp.route('/tools/writing-evaluation/<int:evaluation_id>', methods=['GET'])
def get_writing_evaluation(evaluation_id):
    """
    Obtiene el detalle completo de una evaluación
    
    Retorna:
    - Evaluación completa con todos los detalles
    """
    try:
        from app.models.writing_evaluation import WritingEvaluation
        
        evaluation = WritingEvaluation.query.get(evaluation_id)
        
        if not evaluation:
            return jsonify({"error": "Evaluación no encontrada"}), 404
        
        return jsonify({
            "evaluation": evaluation.to_dict()
        }), 200
        
    except Exception as e:
        print(f"❌ Error obteniendo evaluación: {e}")
        return jsonify({"error": str(e)}), 500


@academic_bp.route('/tools/writing-evaluation/<int:evaluation_id>/pdf', methods=['GET'])
def download_writing_evaluation_pdf(evaluation_id):
    """
    Descarga la evaluación como PDF
    
    Genera un PDF formateado con:
    - Información general
    - Scores visuales
    - Métricas del documento
    - Errores específicos
    - Sugerencias de mejora
    - Recomendaciones
    
    Retorna:
    - PDF descargable
    """
    try:
        from app.models.writing_evaluation import WritingEvaluation
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib.units import inch
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from io import BytesIO
        
        evaluation = WritingEvaluation.query.get(evaluation_id)
        
        if not evaluation:
            return jsonify({"error": "Evaluación no encontrada"}), 404
        
        # Crear PDF en memoria
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, 
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Contenedor para elementos
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#4F46E5'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#7C3AED'),
            spaceAfter=12,
            spaceBefore=20
        )
        
        # Título
        elements.append(Paragraph("Reporte de Evaluación de Escritura", title_style))
        elements.append(Spacer(1, 12))
        
        # Información general
        info_data = [
            ['Documento:', evaluation.file_name],
            ['Fecha:', evaluation.evaluated_at.strftime('%d/%m/%Y %H:%M')],
            ['Palabras:', str(evaluation.word_count)],
            ['Score General:', f"{evaluation.overall_score}/100"]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#EEF2FF')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))
        
        # Scores
        elements.append(Paragraph("Puntuaciones Detalladas", heading_style))
        
        scores_data = [
            ['Aspecto', 'Puntuación'],
            ['Gramática', f"{evaluation.grammar_score}/100"],
            ['Coherencia', f"{evaluation.coherence_score}/100"],
            ['Vocabulario', f"{evaluation.vocabulary_score}/100"],
            ['Estructura', f"{evaluation.structure_score}/100"]
        ]
        
        scores_table = Table(scores_data, colWidths=[3*inch, 2*inch])
        scores_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(scores_table)
        elements.append(Spacer(1, 20))
        
        # Análisis adicional
        if evaluation.tone_analysis:
            elements.append(Paragraph("Análisis de Estilo", heading_style))
            style_data = [
                ['Tono:', evaluation.tone_analysis],
                ['Formalidad:', f"{evaluation.formality_score}/100" if evaluation.formality_score else 'N/A'],
                ['Complejidad:', evaluation.complexity_level or 'N/A']
            ]
            style_table = Table(style_data, colWidths=[2*inch, 4*inch])
            style_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FEF3C7')),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ]))
            elements.append(style_table)
            elements.append(Spacer(1, 20))
        
        # Fortalezas
        elements.append(Paragraph("✓ Fortalezas", heading_style))
        for strength in evaluation.strengths:
            elements.append(Paragraph(f"• {strength}", styles['Normal']))
        elements.append(Spacer(1, 15))
        
        # Áreas de mejora
        elements.append(Paragraph("⚠ Áreas de Mejora", heading_style))
        for weakness in evaluation.weaknesses:
            elements.append(Paragraph(f"• {weakness}", styles['Normal']))
        elements.append(Spacer(1, 15))
        
        # Errores específicos (nueva página si es necesario)
        if evaluation.specific_errors:
            elements.append(PageBreak())
            elements.append(Paragraph("Errores Específicos Detectados", heading_style))
            
            for error in evaluation.specific_errors[:10]:  # Máximo 10 errores
                error_text = f"<b>{error.get('type', 'Error').upper()}:</b> {error.get('error', '')} → {error.get('correction', '')}"
                elements.append(Paragraph(error_text, styles['Normal']))
                
                if error.get('explanation'):
                    elements.append(Paragraph(f"<i>{error['explanation']}</i>", styles['Italic']))
                elements.append(Spacer(1, 10))
        
        # Sugerencias
        if evaluation.suggestions:
            elements.append(Spacer(1, 15))
            elements.append(Paragraph("💡 Sugerencias de Mejora", heading_style))
            
            for suggestion in evaluation.suggestions[:8]:  # Máximo 8 sugerencias
                sugg_text = f"<b>[{suggestion.get('category', 'General').upper()}]</b> {suggestion.get('suggestion', '')}"
                elements.append(Paragraph(sugg_text, styles['Normal']))
                
                if suggestion.get('example'):
                    elements.append(Paragraph(f"Ejemplo: <i>{suggestion['example']}</i>", styles['Italic']))
                elements.append(Spacer(1, 10))
        
        # Recomendaciones
        elements.append(PageBreak())
        elements.append(Paragraph("Recomendaciones para Mejorar", heading_style))
        for i, rec in enumerate(evaluation.recommendations, 1):
            elements.append(Paragraph(f"{i}. {rec}", styles['Normal']))
            elements.append(Spacer(1, 8))
        
        # Resumen final
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("Resumen General", heading_style))
        elements.append(Paragraph(evaluation.summary, styles['Normal']))
        
        # Generar PDF
        doc.build(elements)
        
        # Preparar para descarga
        buffer.seek(0)
        
        filename = f"evaluacion_{evaluation.id}_{evaluation.file_name.rsplit('.', 1)[0]}.pdf"
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except ImportError as e:
        print(f"❌ Error: ReportLab no instalado: {e}")
        return jsonify({
            "error": "ReportLab no está instalado. Instala con: pip install reportlab"
        }), 503
        
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@academic_bp.route('/tools/writing-evaluation/<int:evaluation_id>', methods=['DELETE'])
def delete_writing_evaluation(evaluation_id):
    """
    Elimina una evaluación del historial
    
    Retorna:
    - Confirmación de eliminación
    """
    try:
        from app.models.writing_evaluation import WritingEvaluation
        
        evaluation = WritingEvaluation.query.get(evaluation_id)
        
        if not evaluation:
            return jsonify({"error": "Evaluación no encontrada"}), 404
        
        # Eliminar archivos asociados si existen
        try:
            if evaluation.file_path and os.path.exists(evaluation.file_path):
                os.remove(evaluation.file_path)
            if evaluation.previous_file_path and os.path.exists(evaluation.previous_file_path):
                os.remove(evaluation.previous_file_path)
        except Exception as e:
            print(f"⚠️  Error eliminando archivos: {e}")
        
        # Eliminar registro de BD
        db.session.delete(evaluation)
        db.session.commit()
        
        return jsonify({
            "message": "Evaluación eliminada exitosamente"
        }), 200
        
    except Exception as e:
        print(f"❌ Error eliminando evaluación: {e}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

