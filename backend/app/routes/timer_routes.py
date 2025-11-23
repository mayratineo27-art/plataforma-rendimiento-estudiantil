"""
Rutas para gestión de cronómetros de estudio
Permite crear, actualizar y consultar sesiones de tiempo
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models.timer import StudyTimer
from app.models.academic import AcademicCourse, AcademicTask

timer_bp = Blueprint('timer', __name__, url_prefix='/api/timer')

@timer_bp.route('/start', methods=['POST'])
def start_timer():
    """Inicia un nuevo cronómetro o continúa uno existente"""
    try:
        data = request.json
        user_id = data.get('user_id')
        course_id = data.get('course_id')
        task_id = data.get('task_id')
        session_name = data.get('session_name')
        
        if not user_id:
            return jsonify({"error": "user_id es requerido"}), 400

        # Buscar si ya existe un timer activo para este contexto
        timer = StudyTimer.query.filter_by(
            user_id=user_id,
            course_id=course_id,
            task_id=task_id,
            is_active=True
        ).first()

        if timer:
            # Ya existe un timer activo, solo actualizar
            return jsonify({"message": "Timer ya está activo", "timer": timer.to_dict()}), 200

        # Crear nuevo timer
        timer = StudyTimer(
            user_id=user_id,
            course_id=course_id,
            task_id=task_id,
            session_name=session_name,
            is_active=True,
            started_at=datetime.utcnow()
        )
        
        db.session.add(timer)
        db.session.commit()
        
        return jsonify({"message": "Timer iniciado", "timer": timer.to_dict()}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@timer_bp.route('/stop/<int:timer_id>', methods=['PUT'])
def stop_timer(timer_id):
    """Detiene un cronómetro y guarda el tiempo acumulado"""
    try:
        timer = StudyTimer.query.get(timer_id)
        
        if not timer:
            return jsonify({"error": "Timer no encontrado"}), 404
        
        if not timer.is_active:
            return jsonify({"error": "Timer ya está detenido"}), 400
        
        # Calcular tiempo transcurrido
        if timer.started_at:
            elapsed = (datetime.utcnow() - timer.started_at).total_seconds()
            timer.total_seconds += int(elapsed)
        
        timer.is_active = False
        timer.started_at = None
        
        db.session.commit()
        
        return jsonify({
            "message": "Timer detenido",
            "timer": timer.to_dict(),
            "formatted_time": timer.format_time()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@timer_bp.route('/reset/<int:timer_id>', methods=['PUT'])
def reset_timer(timer_id):
    """Reinicia un cronómetro a cero"""
    try:
        timer = StudyTimer.query.get(timer_id)
        
        if not timer:
            return jsonify({"error": "Timer no encontrado"}), 404
        
        timer.total_seconds = 0
        timer.is_active = False
        timer.started_at = None
        
        db.session.commit()
        
        return jsonify({"message": "Timer reiniciado", "timer": timer.to_dict()}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@timer_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_timers(user_id):
    """Obtiene todos los timers de un usuario"""
    try:
        course_id = request.args.get('course_id', type=int)
        task_id = request.args.get('task_id', type=int)
        
        query = StudyTimer.query.filter_by(user_id=user_id)
        
        if course_id:
            query = query.filter_by(course_id=course_id)
        if task_id:
            query = query.filter_by(task_id=task_id)
        
        timers = query.order_by(StudyTimer.updated_at.desc()).all()
        
        return jsonify({
            "timers": [t.to_dict() for t in timers],
            "total_timers": len(timers)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@timer_bp.route('/stats/<int:user_id>', methods=['GET'])
def get_user_stats(user_id):
    """Obtiene estadísticas de tiempo de estudio del usuario"""
    try:
        # Total de tiempo estudiado
        timers = StudyTimer.query.filter_by(user_id=user_id).all()
        total_seconds = sum(t.total_seconds for t in timers)
        
        # Tiempo por curso
        course_stats = {}
        for timer in timers:
            if timer.course_id:
                course_name = timer.course.name if timer.course else "Sin curso"
                if course_name not in course_stats:
                    course_stats[course_name] = 0
                course_stats[course_name] += timer.total_seconds
        
        # Formato de tiempo total
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        
        return jsonify({
            "total_seconds": total_seconds,
            "total_formatted": f"{hours}h {minutes}m",
            "total_sessions": len(timers),
            "course_stats": course_stats,
            "active_timers": len([t for t in timers if t.is_active])
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@timer_bp.route('/<int:timer_id>', methods=['DELETE'])
def delete_timer(timer_id):
    """Elimina un cronómetro"""
    try:
        timer = StudyTimer.query.get(timer_id)
        
        if not timer:
            return jsonify({"error": "Timer no encontrado"}), 404
        
        db.session.delete(timer)
        db.session.commit()
        
        return jsonify({"message": "Timer eliminado"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
