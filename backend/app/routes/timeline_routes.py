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
    Acepta course_id o course_name (si es course_name, crea o busca el curso automáticamente)
    """
    print("=" * 80)
    print("🎯 PETICIÓN RECIBIDA EN /api/timelines/topic/create")
    print("=" * 80)
    
    try:
        data = request.json
        print(f"📝 Datos recibidos: {data}")
        
        # Validar datos requeridos
        if not data.get('user_id') or not data.get('course_topic'):
            return jsonify({"error": "user_id y course_topic son requeridos"}), 400
        
        user_id = int(data['user_id'])
        course_topic = data['course_topic']
        course_id = data.get('course_id')
        course_name = data.get('course_name')
        
        # Si no hay course_id pero sí course_name, buscar o crear el curso
        if not course_id and course_name:
            print(f"🔍 Buscando o creando curso: {course_name}")
            
            # Buscar si el curso ya existe
            from app.models.academic import AcademicCourse
            existing_course = AcademicCourse.query.filter_by(
                user_id=user_id,
                name=course_name
            ).first()
            
            if existing_course:
                course_id = existing_course.id
                print(f"✅ Curso encontrado con ID: {course_id}")
            else:
                # Crear nuevo curso
                new_course = AcademicCourse(
                    user_id=user_id,
                    name=course_name,
                    category='general',
                    icon='BookOpen',
                    color='blue'
                )
                db.session.add(new_course)
                db.session.flush()
                course_id = new_course.id
                print(f"✅ Nuevo curso creado con ID: {course_id}")
        
        if not course_id:
            return jsonify({"error": "Debe proporcionar course_id o course_name"}), 400
        
        course_id = int(course_id)
        
        # Crear título automático si no se proporciona
        title = data.get('title', f"{course_name or 'Curso'} - {course_topic}")
        
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
        
        # Generar pasos con IA (por defecto True para timelines de tema)
        generate_ai = data.get('generate_with_ai', True)  # Por defecto True
        
        if generate_ai and AI_AVAILABLE:
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
        
        # Si no hay pasos generados, crear pasos por defecto
        if not new_timeline.steps or len(new_timeline.steps) == 0:
            print(f"📋 Creando pasos por defecto...")
            default_steps = [
                {
                    'title': f'Investigar conceptos básicos de {course_topic}',
                    'description': 'Buscar y revisar recursos introductorios sobre el tema',
                    'order': 1
                },
                {
                    'title': 'Estudiar contenido principal',
                    'description': f'Revisar y tomar notas sobre los puntos clave de {course_topic}',
                    'order': 2
                },
                {
                    'title': 'Practicar con ejercicios',
                    'description': 'Realizar ejercicios o problemas relacionados con el tema',
                    'order': 3
                },
                {
                    'title': 'Revisar y consolidar conocimientos',
                    'description': 'Hacer un repaso general y verificar comprensión del tema',
                    'order': 4
                }
            ]
            
            for step_data in default_steps:
                step = TimelineStep(
                    timeline_id=new_timeline.id,
                    title=step_data['title'],
                    description=step_data['description'],
                    order=step_data['order']
                )
                db.session.add(step)
                print(f"  ✓ Paso por defecto {step_data['order']}: {step_data['title']}")
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


@timeline_bp.route('/events/create', methods=['POST'])
def create_events_timeline():
    """
    Crea una línea de tiempo de EVENTOS históricos/educativos
    NO vinculada a proyectos - Para organizar cronológicamente eventos de cualquier tema
    Ejemplo: Historia de las computadoras, Evolución del internet, etc.
    """
    print("=" * 80)
    print("📅 PETICIÓN: Crear línea de tiempo de EVENTOS")
    print("=" * 80)
    
    try:
        data = request.json
        print(f"📝 Datos: {data}")
        
        # Validar datos requeridos
        if not data.get('user_id') or not data.get('topic'):
            return jsonify({"error": "user_id y topic son requeridos"}), 400
        
        user_id = int(data['user_id'])
        topic = data['topic']
        description = data.get('description', f'Línea de tiempo histórica sobre {topic}')
        
        print(f"✅ Creando timeline de eventos - user_id: {user_id}, topic: {topic}")
        
        # Crear la línea de tiempo (SIN course_id ni project_id)
        new_timeline = Timeline(
            user_id=user_id,
            course_id=None,  # NO vinculado a cursos
            project_id=None,  # NO vinculado a proyectos
            title=topic,
            description=description,
            timeline_type='free',  # Tipo libre
            course_topic=topic,  # Guardar el tema
            end_date=None
        )
        
        db.session.add(new_timeline)
        db.session.flush()
        
        print(f"✅ Timeline de eventos creado con ID: {new_timeline.id}")
        
        # Generar eventos con IA
        if AI_AVAILABLE:
            try:
                print(f"🤖 Generando eventos históricos con IA para: {topic}")
                
                # Prompt específico para generar eventos cronológicos
                ai_prompt = f"""Genera una línea de tiempo con los eventos más importantes sobre: {topic}
                
Formato requerido: Lista de eventos cronológicos ordenados por fecha.
Cada evento debe tener:
- Título del evento
- Descripción breve
- Contexto histórico o importancia

Genera entre 5-10 eventos clave."""

                ai_result = StudyToolsService.generate_timeline(ai_prompt, 'academic')
                print(f"✅ Resultado IA: {type(ai_result)}")
                
                # Procesar resultado de la IA
                generated_events = []
                
                if isinstance(ai_result, dict):
                    if 'events' in ai_result:
                        generated_events = ai_result['events']
                    elif 'steps' in ai_result:
                        generated_events = ai_result['steps']
                    elif 'milestones' in ai_result:
                        generated_events = ai_result['milestones']
                elif isinstance(ai_result, list):
                    generated_events = ai_result
                
                print(f"✅ Eventos generados: {len(generated_events)}")
                
                # Crear TimelineSteps para cada evento
                for i, event_data in enumerate(generated_events):
                    event = TimelineStep(
                        timeline_id=new_timeline.id,
                        title=event_data.get('title', f'Evento {i+1}'),
                        description=event_data.get('description', ''),
                        order=i + 1
                    )
                    db.session.add(event)
                    print(f"  ✓ Evento {i+1}: {event_data.get('title', '')}")
                
                if len(generated_events) == 0:
                    raise Exception("No se generaron eventos")
                    
            except Exception as e:
                print(f"❌ Error con IA: {e}")
                import traceback
                traceback.print_exc()
                # Continuar con eventos por defecto
        
        # Si no hay eventos, crear eventos por defecto
        if not new_timeline.steps or len(new_timeline.steps) == 0:
            print(f"📋 Creando eventos por defecto para: {topic}")
            
            default_events = [
                {
                    'title': f'Origen de {topic}',
                    'description': 'Primeros desarrollos y conceptos fundamentales',
                    'order': 1
                },
                {
                    'title': 'Evolución temprana',
                    'description': 'Primeras innovaciones y avances significativos',
                    'order': 2
                },
                {
                    'title': 'Periodo de expansión',
                    'description': 'Crecimiento y adopción generalizada',
                    'order': 3
                },
                {
                    'title': 'Innovaciones modernas',
                    'description': 'Desarrollos recientes y tecnologías actuales',
                    'order': 4
                },
                {
                    'title': 'Estado actual y futuro',
                    'description': 'Situación presente y tendencias futuras',
                    'order': 5
                }
            ]
            
            for event_data in default_events:
                event = TimelineStep(
                    timeline_id=new_timeline.id,
                    title=event_data['title'],
                    description=event_data['description'],
                    order=event_data['order']
                )
                db.session.add(event)
                print(f"  ✓ Evento por defecto {event_data['order']}: {event_data['title']}")
        
        db.session.commit()
        print(f"✅ Timeline de eventos guardada exitosamente")
        
        return jsonify({
            "message": "Línea de tiempo de eventos creada exitosamente",
            "timeline": new_timeline.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
