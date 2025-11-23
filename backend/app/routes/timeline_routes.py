"""
Rutas para gestión de líneas de tiempo
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.timeline import Timeline
from app.models.timeline_step import TimelineStep
from datetime import datetime
import json

# Importar servicio de IA - ACTIVO
from app.services.academic.study_tools import StudyToolsService
AI_AVAILABLE = True

# Definir blueprint
timeline_bp = Blueprint('timeline', __name__, url_prefix='/api/timeline')


@timeline_bp.route('/', methods=['POST'])
@timeline_bp.route('/create', methods=['POST'])
def create_timeline():
    """Crea una nueva línea de tiempo con opción de generar pasos con IA"""
    try:
        data = request.json
        
        # Validar datos requeridos
        if not data.get('user_id') or not data.get('title'):
            return jsonify({"error": "user_id y title son requeridos"}), 400
        
        # Crear la línea de tiempo
        new_timeline = Timeline(
            user_id=data['user_id'],
            project_id=data.get('project_id'),
            course_id=data.get('course_id'),
            title=data['title'],
            description=data.get('description', ''),
            timeline_type=data.get('timeline_type', 'course'),
            end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None
        )
        
        db.session.add(new_timeline)
        db.session.flush()  # Obtener el ID sin hacer commit
        
        # Generar pasos con IA o usar pasos manuales
        if data.get('generate_with_ai') and AI_AVAILABLE:
            try:
                context = data.get('ai_context', data['title'])
                timeline_type = 'academic' if data.get('timeline_type') == 'project' else 'course'
                ai_result = StudyToolsService.generate_timeline(context, timeline_type)
                
                # Extraer pasos del resultado de la IA
                generated_steps = []
                
                if isinstance(ai_result, dict):
                    # La IA retorna 'milestones', convertirlos a steps
                    if 'milestones' in ai_result:
                        for milestone in ai_result['milestones']:
                            generated_steps.append({
                                'title': milestone.get('title', ''),
                                'description': milestone.get('description', ''),
                                'order': milestone.get('order', len(generated_steps) + 1)
                            })
                    elif 'steps' in ai_result:
                        generated_steps = ai_result['steps']
                elif isinstance(ai_result, list):
                    generated_steps = ai_result
                
                # Crear TimelineSteps desde los pasos generados por IA
                for i, step_data in enumerate(generated_steps):
                    step = TimelineStep(
                        timeline_id=new_timeline.id,
                        title=step_data.get('title', f'Paso {i+1}'),
                        description=step_data.get('description', ''),
                        order=step_data.get('order', i + 1)
                    )
                    db.session.add(step)
                    
            except Exception as e:
                print(f"Error generando con IA: {e}")
                import traceback
                traceback.print_exc()
                # Continuar sin pasos si falla la IA
        else:
            # Usar pasos manuales si se proporcionaron
            manual_steps = data.get('steps', [])
            for i, step_data in enumerate(manual_steps):
                if step_data.get('title'):  # Solo crear si tiene título
                    step = TimelineStep(
                        timeline_id=new_timeline.id,
                        title=step_data['title'],
                        description=step_data.get('description', ''),
                        order=step_data.get('order', i + 1)
                    )
                    db.session.add(step)
        
        db.session.commit()
        
        return jsonify({
            "message": "Línea de tiempo creada exitosamente",
            "timeline": new_timeline.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creando línea de tiempo: {e}")
        return jsonify({"error": str(e)}), 500


@timeline_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_timelines(user_id):
    """Obtiene todas las líneas de tiempo de un usuario"""
    try:
        # Filtros opcionales
        visible_only = request.args.get('visible_only', 'false').lower() == 'true'
        project_id = request.args.get('project_id', type=int)
        course_id = request.args.get('course_id', type=int)
        
        query = Timeline.query.filter_by(user_id=user_id)
        
        if visible_only:
            query = query.filter_by(is_visible=True)
        
        if project_id:
            query = query.filter_by(project_id=project_id)
        
        if course_id:
            query = query.filter_by(course_id=course_id)
        
        timelines = query.order_by(Timeline.created_at.desc()).all()
        
        return jsonify({
            "timelines": [t.to_dict() for t in timelines],
            "count": len(timelines)
        }), 200
        
    except Exception as e:
        print(f"Error obteniendo líneas de tiempo: {e}")
        return jsonify({"error": str(e)}), 500


@timeline_bp.route('/<int:timeline_id>', methods=['GET'])
def get_timeline(timeline_id):
    """Obtiene una línea de tiempo específica"""
    try:
        timeline = Timeline.query.get(timeline_id)
        if not timeline:
            return jsonify({"error": "Línea de tiempo no encontrada"}), 404
        
        return jsonify(timeline.to_dict()), 200
        
    except Exception as e:
        print(f"Error obteniendo línea de tiempo: {e}")
        return jsonify({"error": str(e)}), 500


@timeline_bp.route('/<int:timeline_id>', methods=['PUT'])
def update_timeline(timeline_id):
    """Actualiza una línea de tiempo"""
    try:
        timeline = Timeline.query.get(timeline_id)
        if not timeline:
            return jsonify({"error": "Línea de tiempo no encontrada"}), 404
        
        data = request.json
        
        if 'title' in data:
            timeline.title = data['title']
        if 'description' in data:
            timeline.description = data['description']
        if 'is_visible' in data:
            timeline.is_visible = data['is_visible']
        if 'steps' in data:
            timeline.update_steps(data['steps'])
        
        timeline.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "message": "Línea de tiempo actualizada",
            "timeline": timeline.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error actualizando línea de tiempo: {e}")
        return jsonify({"error": str(e)}), 500


@timeline_bp.route('/<int:timeline_id>/step/<int:step_id>/toggle', methods=['PUT'])
def toggle_step(timeline_id, step_id):
    """Marca un paso como completado o incompleto"""
    try:
        timeline = Timeline.query.get(timeline_id)
        if not timeline:
            return jsonify({"error": "Línea de tiempo no encontrada"}), 404
        
        # Buscar el paso (puede ser por ID de TimelineStep o por índice en JSON)
        step = TimelineStep.query.filter_by(id=step_id, timeline_id=timeline_id).first()
        
        if step:
            # Usar modelo TimelineStep
            step.toggle_complete()
            db.session.commit()
            
            return jsonify({
                "message": "Paso actualizado",
                "timeline": timeline.to_dict()
            }), 200
        else:
            # Fallback: usar steps_json (para compatibilidad con código antiguo)
            if not timeline.steps_json:
                return jsonify({"error": "Paso no encontrado"}), 404
                
            steps = json.loads(timeline.steps_json)
            step_index = step_id  # Asumir que step_id es el índice
            
            if step_index < 0 or step_index >= len(steps):
                return jsonify({"error": "Índice de paso inválido"}), 400
            
            # Toggle del estado
            current_state = steps[step_index].get('completed', False)
            steps[step_index]['completed'] = not current_state
            
            if not current_state:
                steps[step_index]['completed_at'] = datetime.utcnow().isoformat()
            else:
                if 'completed_at' in steps[step_index]:
                    del steps[step_index]['completed_at']
            
            timeline.update_steps(steps)
            db.session.commit()
            
            return jsonify({
                "message": "Paso actualizado",
                "timeline": timeline.to_dict()
            }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error actualizando paso: {e}")
        return jsonify({"error": str(e)}), 500


@timeline_bp.route('/<int:timeline_id>/visibility', methods=['PUT'])
def toggle_visibility(timeline_id):
    """Alterna la visibilidad de una línea de tiempo"""
    try:
        timeline = Timeline.query.get(timeline_id)
        if not timeline:
            return jsonify({"error": "Línea de tiempo no encontrada"}), 404
        
        timeline.is_visible = not timeline.is_visible
        timeline.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "message": f"Línea de tiempo {'visible' if timeline.is_visible else 'oculta'}",
            "timeline": timeline.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error cambiando visibilidad: {e}")
        return jsonify({"error": str(e)}), 500


@timeline_bp.route('/<int:timeline_id>/complete', methods=['PUT'])
def mark_timeline_complete(timeline_id):
    """Marca toda la línea de tiempo como completada"""
    try:
        timeline = Timeline.query.get(timeline_id)
        if not timeline:
            return jsonify({"error": "Línea de tiempo no encontrada"}), 404
        
        # Marcar todos los pasos como completados
        steps = json.loads(timeline.steps_json)
        now = datetime.utcnow().isoformat()
        
        for step in steps:
            step['completed'] = True
            if 'completed_at' not in step:
                step['completed_at'] = now
        
        timeline.update_steps(steps)
        db.session.commit()
        
        return jsonify({
            "message": "Línea de tiempo completada",
            "timeline": timeline.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error completando línea de tiempo: {e}")
        return jsonify({"error": str(e)}), 500


@timeline_bp.route('/<int:timeline_id>', methods=['DELETE'])
def delete_timeline(timeline_id):
    """Elimina una línea de tiempo"""
    try:
        timeline = Timeline.query.get(timeline_id)
        if not timeline:
            return jsonify({"error": "Línea de tiempo no encontrada"}), 404
        
        db.session.delete(timeline)
        db.session.commit()
        
        return jsonify({"message": "Línea de tiempo eliminada"}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error eliminando línea de tiempo: {e}")
        return jsonify({"error": str(e)}), 500
