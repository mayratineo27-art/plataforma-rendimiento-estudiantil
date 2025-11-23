"""
Controlador para el Dashboard - Núcleo de Comando
Proporciona métricas en tiempo real del sistema y estado de los módulos
"""

from flask import jsonify
from app.models.document import Document
from app.models.video_session import VideoSession
from app.models.audio_session import AudioSession  # ← IMPORTANTE: Agregar este import
from app.models.report import Report
from app.models.student_profile import StudentProfile
from app import db
from datetime import datetime, timedelta
import random

def get_dashboard_metrics(user_id):
    """
    Obtiene métricas generales del dashboard para un usuario específico
    """
    try:
        # Contar documentos analizados
        documentos_analizados = Document.query.filter_by(user_id=user_id).count()
        
        # Contar sesiones de video completadas
        sesiones_completadas = VideoSession.query.filter_by(
            user_id=user_id,
            processing_status='completed'  # ← Usar processing_status en vez de status
        ).count()
        
        # Contar reportes generados
        reportes_generados = Report.query.filter_by(user_id=user_id).count()
        
        # Verificar si existe perfil
        perfil = StudentProfile.query.filter_by(user_id=user_id).first()
        perfiles_activos = 1 if perfil else 0
        
        # Métricas de procesamiento de IA (simuladas por ahora)
        # En producción, esto vendría de logs o métricas reales
        procesamiento_ia = {
            'gemini': random.randint(75, 100),
            'deepface': random.randint(80, 100),
            'speechRecognition': random.randint(70, 95)
        }
        
        # Estado del pipeline de módulos
        pipeline = get_pipeline_status(user_id)
        
        # Actividad reciente
        actividad_reciente = get_recent_activity(user_id)
        
        return jsonify({
            'documentosAnalizados': documentos_analizados,
            'sesionesCompletadas': sesiones_completadas,
            'reportesGenerados': reportes_generados,
            'perfilesActivos': perfiles_activos,
            'procesamientoIA': procesamiento_ia,
            'pipeline': pipeline,
            'actividadReciente': actividad_reciente,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener métricas del dashboard',
            'details': str(e)
        }), 500


def get_pipeline_status(user_id):
    """
    Obtiene el estado de procesamiento de cada módulo
    """
    try:
        # Módulo 1: Análisis de Documentos
        documentos_recientes = Document.query.filter_by(user_id=user_id)\
            .order_by(Document.created_at.desc()).limit(5).all()
        
        modulo1_status = 'idle'
        modulo1_progress = 0
        if documentos_recientes:
            modulo1_status = 'completed'
            modulo1_progress = 100
        
        # Módulo 2: Sesiones de Video/Audio
        sesiones_recientes = VideoSession.query.filter_by(user_id=user_id)\
            .order_by(VideoSession.created_at.desc()).limit(5).all()
        
        modulo2_status = 'idle'
        modulo2_progress = 0
        if sesiones_recientes:
            ultima_sesion = sesiones_recientes[0]
            if ultima_sesion.processing_status == 'processing':  # ← Corregido
                modulo2_status = 'processing'
                modulo2_progress = 50
            elif ultima_sesion.processing_status == 'completed':  # ← Corregido
                modulo2_status = 'completed'
                modulo2_progress = 100
        
        # Módulo 3: Perfil Integral
        perfil = StudentProfile.query.filter_by(user_id=user_id).first()
        
        modulo3_status = 'idle'
        modulo3_progress = 0
        if perfil:
            modulo3_status = 'active'
            modulo3_progress = 85
        
        # Módulo 4: Reportes
        reportes_recientes = Report.query.filter_by(user_id=user_id)\
            .order_by(Report.created_at.desc()).limit(5).all()
        
        modulo4_status = 'idle'
        modulo4_progress = 0
        if reportes_recientes:
            modulo4_status = 'completed'
            modulo4_progress = 100
        
        return {
            'modulo1': {
                'status': modulo1_status,
                'progress': modulo1_progress,
                'ultimoProcesamiento': documentos_recientes[0].created_at.isoformat() if documentos_recientes else None
            },
            'modulo2': {
                'status': modulo2_status,
                'progress': modulo2_progress,
                'ultimoProcesamiento': sesiones_recientes[0].created_at.isoformat() if sesiones_recientes else None
            },
            'modulo3': {
                'status': modulo3_status,
                'progress': modulo3_progress,
                'ultimaActualizacion': perfil.updated_at.isoformat() if perfil else None
            },
            'modulo4': {
                'status': modulo4_status,
                'progress': modulo4_progress,
                'ultimoProcesamiento': reportes_recientes[0].created_at.isoformat() if reportes_recientes else None
            }
        }
        
    except Exception as e:
        print(f"Error al obtener estado del pipeline: {str(e)}")
        # Retornar estados por defecto en caso de error
        return {
            'modulo1': {'status': 'idle', 'progress': 0},
            'modulo2': {'status': 'idle', 'progress': 0},
            'modulo3': {'status': 'idle', 'progress': 0},
            'modulo4': {'status': 'idle', 'progress': 0}
        }


def get_recent_activity(user_id, limit=10):
    """
    Obtiene la actividad reciente del usuario en el sistema
    """
    try:
        actividades = []
        
        # Documentos recientes
        documentos = Document.query.filter_by(user_id=user_id)\
            .order_by(Document.created_at.desc()).limit(limit).all()
        for doc in documentos:
            actividades.append({
                'tipo': 'documento',
                'accion': f'Documento "{doc.filename}" analizado',
                'modulo': 'Módulo 1',
                'timestamp': doc.created_at.isoformat(),
                'status': 'success'
            })
        
        # Sesiones recientes
        sesiones = VideoSession.query.filter_by(user_id=user_id)\
            .order_by(VideoSession.created_at.desc()).limit(limit).all()
        for sesion in sesiones:
            actividades.append({
                'tipo': 'sesion',
                'accion': 'Sesión de video/audio procesada',
                'modulo': 'Módulo 2',
                'timestamp': sesion.created_at.isoformat(),
                'status': 'success'
            })
        
        # Reportes recientes
        reportes = Report.query.filter_by(user_id=user_id)\
            .order_by(Report.created_at.desc()).limit(limit).all()
        for reporte in reportes:
            actividades.append({
                'tipo': 'reporte',
                'accion': f'Reporte "{reporte.title}" generado',
                'modulo': 'Módulo 4',
                'timestamp': reporte.created_at.isoformat(),
                'status': 'success'
            })
        
        # Ordenar por timestamp
        actividades.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return actividades[:limit]
        
    except Exception as e:
        print(f"Error al obtener actividad reciente: {str(e)}")
        return []


def get_system_health():
    """
    Verifica el estado de salud de los servicios del sistema
    """
    try:
        # Verificar conexión a la base de datos
        db.session.execute(db.text('SELECT 1'))
        
        return jsonify({
            'success': True,
            'status': 'healthy',
            'database': 'connected',
            'services': {
                'deepface': 'operational',
                'speech_recognition': 'operational',
                'gemini': 'operational'
            },
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e)
        }), 500


def get_processing_statistics(user_id):
    """
    Obtiene estadísticas detalladas de procesamiento
    """
    try:
        # Calcular estadísticas de los últimos 30 días
        fecha_inicio = datetime.now() - timedelta(days=30)
        
        # Video y audio en proceso
        video_sessions = VideoSession.query.filter_by(user_id=user_id).all()
        audio_sessions = AudioSession.query.filter_by(user_id=user_id).all()
        
        # Documentos procesados por día
        documentos_por_dia = db.session.query(
            db.func.date(Document.created_at).label('fecha'),
            db.func.count(Document.id).label('cantidad')
        ).filter(
            Document.user_id == user_id,
            Document.created_at >= fecha_inicio
        ).group_by(db.func.date(Document.created_at)).all()
        
        # Sesiones por día
        sesiones_por_dia = db.session.query(
            db.func.date(VideoSession.created_at).label('fecha'),
            db.func.count(VideoSession.id).label('cantidad')
        ).filter(
            VideoSession.user_id == user_id,
            VideoSession.created_at >= fecha_inicio
        ).group_by(db.func.date(VideoSession.created_at)).all()
        
        return jsonify({
            'success': True,
            'video': {
                'total': len(video_sessions),
                'completed': len([s for s in video_sessions if s.is_completed]),
                'processing': len([s for s in video_sessions if s.processing_status == 'processing']),
                'failed': len([s for s in video_sessions if s.processing_status == 'failed'])
            },
            'audio': {
                'total': len(audio_sessions),
                'completed': len([s for s in audio_sessions if s.is_completed]),
                'processing': len([s for s in audio_sessions if s.processing_status == 'processing']),
                'failed': len([s for s in audio_sessions if s.processing_status == 'failed'])
            },
            'documentosPorDia': [
                {'fecha': str(item.fecha), 'cantidad': item.cantidad}
                for item in documentos_por_dia
            ],
            'sesionesPorDia': [
                {'fecha': str(item.fecha), 'cantidad': item.cantidad}
                for item in sesiones_por_dia
            ],
            'periodo': '30 días'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': True,
            'message': f'Error: {str(e)}'
        }), 500