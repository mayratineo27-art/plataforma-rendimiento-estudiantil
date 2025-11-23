from flask import Blueprint, request, jsonify
from app import db
from app.models.project import Project, TimeSession
from app.models.academic import AcademicCourse
from datetime import datetime
from sqlalchemy import func

# Definimos el Blueprint
project_bp = Blueprint('project', __name__, url_prefix='/api/projects')

# --- 1. GESTIÓN DE PROYECTOS ---

@project_bp.route('/', methods=['POST'])
def create_project():
    """Crea un proyecto dentro de un curso"""
    try:
        data = request.json
        
        # Validar que el curso existe
        course = AcademicCourse.query.get(data['course_id'])
        if not course:
            return jsonify({"error": "Curso no encontrado"}), 404
        
        new_project = Project(
            course_id=data['course_id'],
            name=data['name'],
            description=data.get('description', ''),
            status=data.get('status', 'not_started'),
            priority=data.get('priority', 'medium'),
            start_date=datetime.fromisoformat(data['start_date']) if 'start_date' in data else None,
            end_date=datetime.fromisoformat(data['end_date']) if 'end_date' in data else None
        )
        
        db.session.add(new_project)
        db.session.commit()
        
        return jsonify({
            "message": "Proyecto creado",
            "project": new_project.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creando proyecto: {e}")
        return jsonify({"error": str(e)}), 500

@project_bp.route('/course/<int:course_id>', methods=['GET'])
def get_course_projects(course_id):
    """Obtiene todos los proyectos de un curso"""
    try:
        projects = Project.query.filter_by(course_id=course_id)\
            .order_by(Project.priority.desc(), Project.created_at.desc()).all()
        
        return jsonify({
            "projects": [p.to_dict() for p in projects]
        }), 200
        
    except Exception as e:
        print(f"Error obteniendo proyectos: {e}")
        return jsonify({"error": str(e)}), 500

@project_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Obtiene un proyecto específico con todas sus sesiones"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"error": "Proyecto no encontrado"}), 404
        
        return jsonify({
            "project": project.to_dict(include_sessions=True)
        }), 200
        
    except Exception as e:
        print(f"Error obteniendo proyecto: {e}")
        return jsonify({"error": str(e)}), 500

@project_bp.route('/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Actualiza un proyecto"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"error": "Proyecto no encontrado"}), 404
        
        data = request.json
        
        if 'name' in data:
            project.name = data['name']
        if 'description' in data:
            project.description = data['description']
        if 'status' in data:
            project.status = data['status']
        if 'priority' in data:
            project.priority = data['priority']
        if 'start_date' in data:
            project.start_date = datetime.fromisoformat(data['start_date']) if data['start_date'] else None
        if 'end_date' in data:
            project.end_date = datetime.fromisoformat(data['end_date']) if data['end_date'] else None
        
        db.session.commit()
        
        return jsonify({
            "message": "Proyecto actualizado",
            "project": project.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error actualizando proyecto: {e}")
        return jsonify({"error": str(e)}), 500

@project_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Elimina un proyecto y todas sus sesiones"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"error": "Proyecto no encontrado"}), 404
        
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({"message": "Proyecto eliminado"}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error eliminando proyecto: {e}")
        return jsonify({"error": str(e)}), 500

# --- 2. SESIONES DE TIEMPO (Timer) ---

@project_bp.route('/<int:project_id>/session/start', methods=['POST'])
def start_session(project_id):
    """Inicia una nueva sesión de tiempo para un proyecto"""
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"error": "Proyecto no encontrado"}), 404
        
        # Verificar si ya hay una sesión activa
        active_session = TimeSession.query.filter_by(
            project_id=project_id,
            is_active=True
        ).first()
        
        if active_session:
            return jsonify({
                "error": "Ya existe una sesión activa",
                "session": active_session.to_dict()
            }), 400
        
        # Crear nueva sesión
        new_session = TimeSession(
            project_id=project_id,
            is_active=True
        )
        
        db.session.add(new_session)
        db.session.commit()
        
        return jsonify({
            "message": "Sesión iniciada",
            "session": new_session.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error iniciando sesión: {e}")
        return jsonify({"error": str(e)}), 500

@project_bp.route('/<int:project_id>/session/stop', methods=['PUT'])
def stop_session(project_id):
    """Detiene la sesión activa y guarda el tiempo"""
    try:
        data = request.json
        duration_seconds = data.get('duration_seconds', 0)
        notes = data.get('notes', '')
        
        # Buscar sesión activa
        active_session = TimeSession.query.filter_by(
            project_id=project_id,
            is_active=True
        ).first()
        
        if not active_session:
            return jsonify({"error": "No hay sesión activa"}), 404
        
        # Actualizar sesión
        active_session.is_active = False
        active_session.duration_seconds = duration_seconds
        active_session.notes = notes
        active_session.ended_at = datetime.utcnow()
        
        # Actualizar tiempo total del proyecto
        project = Project.query.get(project_id)
        if project:
            project.total_time_seconds += duration_seconds
        
        db.session.commit()
        
        return jsonify({
            "message": "Sesión guardada",
            "session": active_session.to_dict(),
            "project_total_time": project.format_time(project.total_time_seconds)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error deteniendo sesión: {e}")
        return jsonify({"error": str(e)}), 500

@project_bp.route('/<int:project_id>/session/active', methods=['GET'])
def get_active_session(project_id):
    """Obtiene la sesión activa si existe"""
    try:
        active_session = TimeSession.query.filter_by(
            project_id=project_id,
            is_active=True
        ).first()
        
        if not active_session:
            return jsonify({"active_session": None}), 200
        
        return jsonify({
            "active_session": active_session.to_dict()
        }), 200
        
    except Exception as e:
        print(f"Error obteniendo sesión activa: {e}")
        return jsonify({"error": str(e)}), 500

@project_bp.route('/<int:project_id>/sessions', methods=['GET'])
def get_project_sessions(project_id):
    """Obtiene todas las sesiones de un proyecto"""
    try:
        sessions = TimeSession.query.filter_by(project_id=project_id)\
            .order_by(TimeSession.started_at.desc()).all()
        
        return jsonify({
            "sessions": [s.to_dict() for s in sessions]
        }), 200
        
    except Exception as e:
        print(f"Error obteniendo sesiones: {e}")
        return jsonify({"error": str(e)}), 500

@project_bp.route('/session/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    """Actualiza notas o duración de una sesión terminada"""
    try:
        session = TimeSession.query.get(session_id)
        if not session:
            return jsonify({"error": "Sesión no encontrada"}), 404
        
        if session.is_active:
            return jsonify({"error": "No se puede editar una sesión activa"}), 400
        
        data = request.json
        old_duration = session.duration_seconds
        
        if 'notes' in data:
            session.notes = data['notes']
        if 'duration_seconds' in data:
            new_duration = data['duration_seconds']
            session.duration_seconds = new_duration
            
            # Actualizar tiempo total del proyecto
            project = Project.query.get(session.project_id)
            if project:
                project.total_time_seconds += (new_duration - old_duration)
        
        db.session.commit()
        
        return jsonify({
            "message": "Sesión actualizada",
            "session": session.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error actualizando sesión: {e}")
        return jsonify({"error": str(e)}), 500

@project_bp.route('/session/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Elimina una sesión y ajusta el tiempo total del proyecto"""
    try:
        session = TimeSession.query.get(session_id)
        if not session:
            return jsonify({"error": "Sesión no encontrada"}), 404
        
        if session.is_active:
            return jsonify({"error": "No se puede eliminar una sesión activa"}), 400
        
        # Ajustar tiempo total del proyecto
        project = Project.query.get(session.project_id)
        if project:
            project.total_time_seconds -= session.duration_seconds
        
        db.session.delete(session)
        db.session.commit()
        
        return jsonify({"message": "Sesión eliminada"}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error eliminando sesión: {e}")
        return jsonify({"error": str(e)}), 500

# --- 3. ESTADÍSTICAS ---

@project_bp.route('/course/<int:course_id>/stats', methods=['GET'])
def get_course_stats(course_id):
    """Obtiene estadísticas de tiempo de todos los proyectos de un curso"""
    try:
        projects = Project.query.filter_by(course_id=course_id).all()
        
        if not projects:
            return jsonify({
                "total_projects": 0,
                "total_time_seconds": 0,
                "projects_data": []
            }), 200
        
        total_time = sum(p.total_time_seconds for p in projects)
        
        projects_data = []
        for project in projects:
            session_count = TimeSession.query.filter_by(project_id=project.id).count()
            projects_data.append({
                "id": project.id,
                "name": project.name,
                "total_time_seconds": project.total_time_seconds,
                "formatted_time": project.format_time(project.total_time_seconds),
                "session_count": session_count,
                "status": project.status,
                "priority": project.priority
            })
        
        # Ordenar por tiempo total descendente
        projects_data.sort(key=lambda x: x['total_time_seconds'], reverse=True)
        
        return jsonify({
            "total_projects": len(projects),
            "total_time_seconds": total_time,
            "formatted_total_time": Project.format_time(total_time),
            "projects_data": projects_data
        }), 200
        
    except Exception as e:
        print(f"Error obteniendo estadísticas: {e}")
        return jsonify({"error": str(e)}), 500
