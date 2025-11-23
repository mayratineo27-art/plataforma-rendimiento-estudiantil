"""
Rutas de API para el Módulo 3: Perfil Integral del Estudiante

Endpoints:
- GET  /api/profile/<user_id>                    - Obtener perfil completo
- POST /api/profile/<user_id>/regenerate         - Regenerar perfil
- GET  /api/profile/<user_id>/strengths          - Obtener fortalezas
- GET  /api/profile/<user_id>/weaknesses         - Obtener debilidades  
- GET  /api/profile/<user_id>/thesis-readiness   - Score preparación tesis
- GET  /api/profile/<user_id>/recommendations    - Obtener recomendaciones
"""

from flask import Blueprint, jsonify, request
from app.services.profile_service import profile_service
from app.models.user import User
from app.utils.logger import logger


# Crear blueprint
profile_bp = Blueprint('profile', __name__)


# =====================================================
# ENDPOINT 1: OBTENER PERFIL COMPLETO
# =====================================================

@profile_bp.route('/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    """
    Obtiene el perfil integral de un estudiante
    
    Si no existe, genera uno nuevo automáticamente
    
    Response:
        200: Perfil obtenido exitosamente
        404: Usuario no encontrado
        500: Error interno
    
    Ejemplo:
        GET /api/profile/1
    """
    try:
        logger.info(f"Solicitud de perfil para user_id={user_id}")
        
        # Verificar que el usuario existe
        user = User.query.get(user_id)
        logger.debug(f"Usuario encontrado: {user}")  # Log adicional
        
        if not user:
            logger.warning(f"Usuario {user_id} no encontrado")  # Log adicional
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Intentar obtener perfil existente
        profile = profile_service.get_profile(user_id)
        logger.debug(f"Perfil obtenido: {profile}")  # Log adicional
        
        # Si no existe, generar uno nuevo
        if not profile:
            logger.info(f"Perfil no existe, generando nuevo para user_id={user_id}")
            result = profile_service.generate_profile(user_id)
            
            if not result.get('success'):
                logger.error(f"Error generando perfil: {result}")  # Log adicional
                return jsonify(result), 400
            
            return jsonify(result), 201
        
        # Retornar perfil existente
        return jsonify(profile), 200
    
    except Exception as e:
        logger.error(f"Error en get_profile: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)  # Mostrar error específico en desarrollo
        }), 500


# =====================================================
# ENDPOINT 2: REGENERAR PERFIL
# =====================================================

@profile_bp.route('/<int:user_id>/regenerate', methods=['POST'])
def regenerate_profile(user_id):
    """
    Fuerza la regeneración del perfil con datos actualizados
    
    Útil cuando:
    - El estudiante subió nuevos documentos
    - Completó nuevas sesiones de video/audio
    - Quiere ver su progreso actualizado
    
    Response:
        200: Perfil regenerado exitosamente
        400: No hay datos suficientes
        404: Usuario no encontrado
        500: Error interno
    
    Ejemplo:
        POST /api/profile/1/regenerate
    """
    try:
        logger.info(f"Regenerando perfil para user_id={user_id}")
        
        # Verificar que el usuario existe
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Forzar regeneración
        result = profile_service.generate_profile(
            user_id=user_id, 
            force_regenerate=True
        )
        
        if not result.get('success'):
            return jsonify(result), 400
        
        logger.info(f"Perfil regenerado exitosamente para user_id={user_id}")
        
        return jsonify({
            **result,
            'message': 'Perfil regenerado exitosamente con los datos más recientes'
        }), 200
    
    except Exception as e:
        logger.error(f"Error en regenerate_profile: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


# =====================================================
# ENDPOINT 3: OBTENER FORTALEZAS
# =====================================================

@profile_bp.route('/<int:user_id>/strengths', methods=['GET'])
def get_strengths(user_id):
    """
    Obtiene solo las fortalezas identificadas del estudiante
    
    Response:
        200: Fortalezas obtenidas
        404: Usuario o perfil no encontrado
        500: Error interno
    
    Ejemplo:
        GET /api/profile/1/strengths
    """
    try:
        logger.info(f"Obteniendo fortalezas de user_id={user_id}")
        
        # Verificar que el usuario existe
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Obtener fortalezas
        strengths = profile_service.get_strengths(user_id)
        
        if not strengths:
            return jsonify({
                'success': False,
                'error': 'No hay perfil generado para este usuario',
                'message': 'Genera el perfil primero con GET /api/profile/<user_id>'
            }), 404
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'strengths': strengths,
            'total': len(strengths)
        }), 200
    
    except Exception as e:
        logger.error(f"Error en get_strengths: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


# =====================================================
# ENDPOINT 4: OBTENER DEBILIDADES
# =====================================================

@profile_bp.route('/<int:user_id>/weaknesses', methods=['GET'])
def get_weaknesses(user_id):
    """
    Obtiene las áreas de mejora identificadas del estudiante
    
    Response:
        200: Debilidades obtenidas
        404: Usuario o perfil no encontrado
        500: Error interno
    
    Ejemplo:
        GET /api/profile/1/weaknesses
    """
    try:
        logger.info(f"Obteniendo debilidades de user_id={user_id}")
        
        # Verificar que el usuario existe
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Obtener debilidades
        weaknesses = profile_service.get_weaknesses(user_id)
        
        if not weaknesses:
            return jsonify({
                'success': False,
                'error': 'No hay perfil generado para este usuario',
                'message': 'Genera el perfil primero con GET /api/profile/<user_id>'
            }), 404
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'weaknesses': weaknesses,
            'total': len(weaknesses)
        }), 200
    
    except Exception as e:
        logger.error(f"Error en get_weaknesses: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


# =====================================================
# ENDPOINT 5: THESIS READINESS SCORE
# =====================================================

@profile_bp.route('/<int:user_id>/thesis-readiness', methods=['GET'])
def get_thesis_readiness(user_id):
    """
    Obtiene el score de preparación para tesis del estudiante
    
    Retorna:
    - Score (0-100)
    - Nivel (bajo, moderado, bueno, excelente)
    - Mensaje interpretativo
    - Recomendaciones específicas
    
    Response:
        200: Score obtenido
        404: Usuario o perfil no encontrado
        500: Error interno
    
    Ejemplo:
        GET /api/profile/1/thesis-readiness
    """
    try:
        logger.info(f"Obteniendo thesis readiness de user_id={user_id}")
        
        # Verificar que el usuario existe
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Obtener perfil
        profile = profile_service.get_profile(user_id)
        
        if not profile:
            return jsonify({
                'success': False,
                'error': 'No hay perfil generado para este usuario',
                'message': 'Genera el perfil primero con GET /api/profile/<user_id>'
            }), 404
        
        # Extraer información de thesis readiness
        thesis_info = profile.get('thesis_readiness', {})
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'thesis_readiness': {
                'score': thesis_info.get('score', 0),
                'level': thesis_info.get('level', 'No evaluado'),
                'message': thesis_info.get('message', ''),
                'breakdown': {
                    'documents_analyzed': profile['metrics']['total_documents'],
                    'writing_quality': profile['metrics']['writing_quality'],
                    'vocabulary_score': profile['metrics']['vocabulary_score'],
                    'attention_score': profile['metrics']['attention_score']
                }
            },
            'recommendations': profile.get('recommendations', [])
        }), 200
    
    except Exception as e:
        logger.error(f"Error en get_thesis_readiness: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


# =====================================================
# ENDPOINT 6: OBTENER RECOMENDACIONES
# =====================================================

@profile_bp.route('/<int:user_id>/recommendations', methods=['GET'])
def get_recommendations(user_id):
    """
    Obtiene recomendaciones personalizadas para el estudiante
    
    Response:
        200: Recomendaciones obtenidas
        404: Usuario o perfil no encontrado
        500: Error interno
    
    Ejemplo:
        GET /api/profile/1/recommendations
    """
    try:
        logger.info(f"Obteniendo recomendaciones de user_id={user_id}")
        
        # Verificar que el usuario existe
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Obtener recomendaciones
        recommendations = profile_service.get_recommendations(user_id)
        
        if not recommendations:
            return jsonify({
                'success': False,
                'error': 'No hay perfil generado para este usuario',
                'message': 'Genera el perfil primero con GET /api/profile/<user_id>'
            }), 404
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'recommendations': recommendations,
            'total': len(recommendations)
        }), 200
    
    except Exception as e:
        logger.error(f"Error en get_recommendations: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


# =====================================================
# ENDPOINT 7: HEALTH CHECK
# =====================================================

@profile_bp.route('/health', methods=['GET'])
def health_check():
    """
    Verifica que el servicio de perfiles está funcionando
    
    Response:
        200: Servicio operativo
    
    Ejemplo:
        GET /api/profile/health
    """
    return jsonify({
        'success': True,
        'service': 'Profile Service',
        'status': 'operational',
        'endpoints': {
            'get_profile': 'GET /api/profile/<user_id>',
            'regenerate': 'POST /api/profile/<user_id>/regenerate',
            'strengths': 'GET /api/profile/<user_id>/strengths',
            'weaknesses': 'GET /api/profile/<user_id>/weaknesses',
            'thesis_readiness': 'GET /api/profile/<user_id>/thesis-readiness',
            'recommendations': 'GET /api/profile/<user_id>/recommendations'
        }
    }), 200