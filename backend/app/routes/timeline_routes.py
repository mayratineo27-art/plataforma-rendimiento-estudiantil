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
    print("=" * 80)
    print("🚀 PETICIÓN RECIBIDA EN /api/timeline/create")
    print("=" * 80)
    
    try:
        data = request.json
        
        print(f"📝 Datos recibidos: {data}")
        
        # Validar datos requeridos
        if not data.get('user_id') or not data.get('title'):
            return jsonify({"error": "user_id y title son requeridos"}), 400
        
        # Convertir course_id y project_id a int o None
        course_id = None
        if data.get('course_id'):
            try:
                course_id = int(data['course_id'])
            except (ValueError, TypeError):
                print(f"⚠️ course_id inválido: {data.get('course_id')}")
        
        project_id = None
        if data.get('project_id'):
            try:
                project_id = int(data['project_id'])
            except (ValueError, TypeError):
                print(f"⚠️ project_id inválido: {data.get('project_id')}")
        
        print(f"✅ IDs convertidos - user_id: {data['user_id']}, course_id: {course_id}, project_id: {project_id}")
        
        # Crear la línea de tiempo
        new_timeline = Timeline(
            user_id=int(data['user_id']),
            project_id=project_id,
            course_id=course_id,
            title=data['title'],
            description=data.get('description', ''),
            timeline_type=data.get('timeline_type', 'course'),
            course_topic=data.get('course_topic'),  # Tema específico del curso
            end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None
        )
        
        db.session.add(new_timeline)
        db.session.flush()  # Obtener el ID sin hacer commit
        
        print(f"✅ Timeline creado en memoria con ID: {new_timeline.id}")
        
        # Generar pasos con IA o usar pasos manuales
        if data.get('generate_with_ai') and AI_AVAILABLE:
            try:
                print(f"🤖 Generando timeline con IA...")
                context = data.get('ai_context', data['title'])
                timeline_type = 'academic' if data.get('timeline_type') == 'project' else 'course'
                
                print(f"📋 Contexto: {context}")
                print(f"📋 Tipo: {timeline_type}")
                
                ai_result = StudyToolsService.generate_timeline(context, timeline_type)
                
                print(f"✅ Resultado IA: {ai_result}")
                
                # Extraer pasos del resultado de la IA
                generated_steps = []
                
                if isinstance(ai_result, dict):
                    # La IA retorna 'milestones', convertirlos a steps
                    if 'milestones' in ai_result:
                        print(f"📦 Procesando {len(ai_result['milestones'])} milestones")
                        for milestone in ai_result['milestones']:
                            generated_steps.append({
                                'title': milestone.get('title', ''),
                                'description': milestone.get('description', ''),
                                'order': milestone.get('order', len(generated_steps) + 1)
                            })
                    elif 'steps' in ai_result:
                        print(f"📦 Procesando {len(ai_result['steps'])} steps")
                        generated_steps = ai_result['steps']
                elif isinstance(ai_result, list):
                    print(f"📦 Procesando lista de {len(ai_result)} items")
                    generated_steps = ai_result
                
                print(f"✅ Pasos generados: {len(generated_steps)}")
                
                # Crear TimelineSteps desde los pasos generados por IA
                for i, step_data in enumerate(generated_steps):
                    step = TimelineStep(
                        timeline_id=new_timeline.id,
                        title=step_data.get('title', f'Paso {i+1}'),
                        description=step_data.get('description', ''),
                        order=step_data.get('order', i + 1)
                    )
                    db.session.add(step)
                    print(f"  ✓ Paso {i+1}: {step_data.get('title', '')}")
                    
            except Exception as e:
                print(f"❌ Error generando con IA: {e}")
                import traceback
                traceback.print_exc()
                # Continuar sin pasos si falla la IA
        else:
            # Usar pasos manuales si se proporcionaron
            manual_steps = data.get('steps', [])
            print(f"📋 Usando {len(manual_steps)} pasos manuales")
            for i, step_data in enumerate(manual_steps):
                if step_data.get('title'):  # Solo crear si tiene título
                    step = TimelineStep(
                        timeline_id=new_timeline.id,
                        title=step_data['title'],
                        description=step_data.get('description', ''),
                        order=step_data.get('order', i + 1)
                    )
                    db.session.add(step)
                    print(f"  ✓ Paso manual {i+1}: {step_data['title']}")
        
        print(f"💾 Guardando en base de datos...")
        db.session.commit()
        print(f"✅ Timeline guardado exitosamente")
        
        return jsonify({
            "message": "Línea de tiempo creada exitosamente",
            "timeline": new_timeline.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creando línea de tiempo: {e}")
        import traceback
        traceback.print_exc()
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


@timeline_bp.route('/topic/create', methods=['POST'])
def create_topic_timeline():
    """
    Crea una línea de tiempo sobre un tema específico de un curso
    Esta línea de tiempo no está vinculada a proyectos, solo a temas del curso
    """
    print("=" * 80)
    print("🎯 PETICIÓN RECIBIDA EN /api/timeline/topic/create")
    print("=" * 80)
    
    try:
        data = request.json
        print(f"📝 Datos recibidos: {data}")
        
        # Validar datos requeridos
        if not data.get('user_id') or not data.get('course_id') or not data.get('course_topic'):
            return jsonify({"error": "user_id, course_id y course_topic son requeridos"}), 400
        
        # Convertir IDs a enteros
        user_id = int(data['user_id'])
        course_id = int(data['course_id'])
        course_topic = data['course_topic']
        
        # Crear título automático si no se proporciona
        title = data.get('title', f"Línea de tiempo: {course_topic}")
        
        print(f"✅ Creando timeline de tema - user_id: {user_id}, course_id: {course_id}, topic: {course_topic}")
        
        # Crear la línea de tiempo
        new_timeline = Timeline(
            user_id=user_id,
            course_id=course_id,
            project_id=None,  # No está vinculado a proyectos
            title=title,
            description=data.get('description', f'Línea de tiempo para estudiar: {course_topic}'),
            timeline_type='free',  # Tipo 'free' para temas libres
            course_topic=course_topic,
            end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None
        )
        
        db.session.add(new_timeline)
        db.session.flush()
        
        print(f"✅ Timeline de tema creado en memoria con ID: {new_timeline.id}")
        
        # Generar pasos con IA o usar pasos manuales
        if data.get('generate_with_ai') and AI_AVAILABLE:
            try:
                print(f"🤖 Generando timeline de tema con IA...")
                ai_context = f"Crear una línea de tiempo de estudio para el tema: {course_topic}"
                
                ai_result = StudyToolsService.generate_timeline(ai_context, 'course')
                print(f"✅ Resultado IA: {ai_result}")
                
                # Extraer pasos del resultado de la IA
                generated_steps = []
                
                if isinstance(ai_result, dict):
                    if 'milestones' in ai_result:
                        print(f"📦 Procesando {len(ai_result['milestones'])} milestones")
                        for milestone in ai_result['milestones']:
                            generated_steps.append({
                                'title': milestone.get('title', ''),
                                'description': milestone.get('description', ''),
                                'order': milestone.get('order', len(generated_steps) + 1)
                            })
                    elif 'steps' in ai_result:
                        print(f"📦 Procesando {len(ai_result['steps'])} steps")
                        generated_steps = ai_result['steps']
                elif isinstance(ai_result, list):
                    print(f"📦 Procesando lista de {len(ai_result)} items")
                    generated_steps = ai_result
                
                print(f"✅ Pasos generados: {len(generated_steps)}")
                
                # Crear TimelineSteps
                for i, step_data in enumerate(generated_steps):
                    step = TimelineStep(
                        timeline_id=new_timeline.id,
                        title=step_data.get('title', f'Paso {i+1}'),
                        description=step_data.get('description', ''),
                        order=step_data.get('order', i + 1)
                    )
                    db.session.add(step)
                    print(f"  ✓ Paso {i+1}: {step_data.get('title', '')}")
                    
            except Exception as e:
                print(f"❌ Error generando con IA: {e}")
                import traceback
                traceback.print_exc()
        else:
            # Usar pasos manuales
            manual_steps = data.get('steps', [])
            print(f"📋 Usando {len(manual_steps)} pasos manuales")
            for i, step_data in enumerate(manual_steps):
                if step_data.get('title'):
                    step = TimelineStep(
                        timeline_id=new_timeline.id,
                        title=step_data['title'],
                        description=step_data.get('description', ''),
                        order=step_data.get('order', i + 1)
                    )
                    db.session.add(step)
                    print(f"  ✓ Paso manual {i+1}: {step_data['title']}")
        
        print(f"💾 Guardando en base de datos...")
        db.session.commit()
        print(f"✅ Timeline de tema guardado exitosamente")
        
        return jsonify({
            "message": "Línea de tiempo de tema creada exitosamente",
            "timeline": new_timeline.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creando línea de tiempo de tema: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

