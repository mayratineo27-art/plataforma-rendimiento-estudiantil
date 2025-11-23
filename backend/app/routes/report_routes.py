"""
app/routes/report_routes.py
Rutas de API para Módulo 4: Reportes y Plantillas

Endpoints:
- POST /api/reports/generate                      - Generar reporte completo
- GET  /api/reports/<report_id>                   - Obtener reporte
- GET  /api/reports/user/<user_id>                - Listar reportes de usuario
- POST /api/reports/template/ppt                  - Generar plantilla PPT
- POST /api/reports/template/docx                 - Generar plantilla DOCX
- GET  /api/reports/templates/<template_id>       - Obtener plantilla
- GET  /api/reports/templates/user/<user_id>      - Listar plantillas
- GET  /api/reports/visualizations/<user_id>      - Datos para gráficos
"""

from flask import Blueprint, jsonify, request, send_file
from app.services.report_service import report_service
from app.models.user import User
from app.utils.logger import logger
import os

# Crear blueprint
report_bp = Blueprint('reports', __name__)


# =====================================================
# GENERACIÓN DE REPORTES COMPLETOS
# =====================================================

@report_bp.route('/generate', methods=['POST'])
def generate_report():
    """
    Genera un reporte completo con múltiples formatos
    
    Body:
        {
            "user_id": 1,
            "report_type": "integral",  // integral, semestral, curso
            "include_ppt": true,
            "include_docx": true
        }
    
    Response:
        201: Reporte generado
        400: Datos inválidos
        404: Usuario no encontrado
    """
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data:
            return jsonify({
                'success': False,
                'error': 'user_id es requerido'
            }), 400
        
        user_id = data['user_id']
        report_type = data.get('report_type', 'integral')
        include_ppt = data.get('include_ppt', True)
        include_docx = data.get('include_docx', True)
        
        logger.info(f"Generando reporte para user_id={user_id}, tipo={report_type}")
        
        # Verificar usuario
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        # Generar reporte
        result = report_service.generate_complete_report(
            user_id=user_id,
            report_type=report_type,
            include_ppt=include_ppt,
            include_docx=include_docx
        )
        
        if not result['success']:
            return jsonify(result), 400
        
        return jsonify(result), 201
        
    except Exception as e:
        logger.error(f"Error en generate_report: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


# =====================================================
# CONSULTA DE REPORTES
# =====================================================

@report_bp.route('/<int:report_id>', methods=['GET'])
def get_report(report_id):
    """
    Obtiene información de un reporte específico
    
    Response:
        200: Reporte encontrado
        404: Reporte no existe
    """
    try:
        logger.info(f"Obteniendo reporte report_id={report_id}")
        
        report = report_service.get_report(report_id)
        
        if not report:
            return jsonify({
                'success': False,
                'error': 'Reporte no encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'report': report
        }), 200
        
    except Exception as e:
        logger.error(f"Error en get_report: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@report_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_reports(user_id):
    """
    Lista todos los reportes de un usuario
    
    Query params:
        limit: Número de reportes (default: 10)
    
    Response:
        200: Lista de reportes
        404: Usuario no encontrado
    """
    try:
        logger.info(f"Listando reportes de user_id={user_id}")
        
        # Verificar usuario
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        limit = request.args.get('limit', 10, type=int)
        
        reports = report_service.get_user_reports(user_id, limit)
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'reports': reports,
            'total': len(reports)
        }), 200
        
    except Exception as e:
        logger.error(f"Error en get_user_reports: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


# =====================================================
# GENERACIÓN DE PLANTILLAS
# =====================================================

@report_bp.route('/template/ppt', methods=['POST'])
def generate_ppt_template():
    """
    Genera una plantilla PowerPoint personalizada
    
    Body:
        {
            "user_id": 1,
            "topic": "Inteligencia Artificial",
            "slides_count": 10,
            "style": "academic"  // academic, professional, creative
        }
    
    Response:
        201: Plantilla generada
        400: Datos inválidos
    """
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data or 'topic' not in data:
            return jsonify({
                'success': False,
                'error': 'user_id y topic son requeridos'
            }), 400
        
        user_id = data['user_id']
        topic = data['topic']
        slides_count = data.get('slides_count', 10)
        style = data.get('style', 'academic')
        
        logger.info(f"Generando plantilla PPT para user_id={user_id}, topic={topic}")
        
        result = report_service.generate_ppt_template(
            user_id=user_id,
            topic=topic,
            slides_count=slides_count,
            style=style
        )
        
        if not result['success']:
            return jsonify(result), 400
        
        return jsonify(result), 201
        
    except Exception as e:
        logger.error(f"Error en generate_ppt_template: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@report_bp.route('/template/docx', methods=['POST'])
def generate_docx_template():
    """
    Genera una plantilla Word personalizada
    
    Body:
        {
            "user_id": 1,
            "topic": "Análisis de Datos",
            "document_type": "informe"  // informe, ensayo, monografia
        }
    
    Response:
        201: Plantilla generada
        400: Datos inválidos
    """
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data or 'topic' not in data:
            return jsonify({
                'success': False,
                'error': 'user_id y topic son requeridos'
            }), 400
        
        user_id = data['user_id']
        topic = data['topic']
        document_type = data.get('document_type', 'informe')
        
        logger.info(f"Generando plantilla DOCX para user_id={user_id}, topic={topic}")
        
        result = report_service.generate_docx_template(
            user_id=user_id,
            topic=topic,
            document_type=document_type
        )
        
        if not result['success']:
            return jsonify(result), 400
        
        return jsonify(result), 201
        
    except Exception as e:
        logger.error(f"Error en generate_docx_template: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


# =====================================================
# CONSULTA DE PLANTILLAS
# =====================================================

@report_bp.route('/templates/<int:template_id>', methods=['GET'])
def get_template(template_id):
    """
    Obtiene información de una plantilla
    
    Response:
        200: Plantilla encontrada
        404: Plantilla no existe
    """
    try:
        logger.info(f"Obteniendo plantilla template_id={template_id}")
        
        template = report_service.get_template(template_id)
        
        if not template:
            return jsonify({
                'success': False,
                'error': 'Plantilla no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'template': template
        }), 200
        
    except Exception as e:
        logger.error(f"Error en get_template: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@report_bp.route('/templates/user/<int:user_id>', methods=['GET'])
def get_user_templates(user_id):
    """
    Lista plantillas de un usuario
    
    Query params:
        type: Filtrar por tipo (ppt, docx, pdf)
    
    Response:
        200: Lista de plantillas
        404: Usuario no encontrado
    """
    try:
        logger.info(f"Listando plantillas de user_id={user_id}")
        
        # Verificar usuario
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        template_type = request.args.get('type', None)
        
        templates = report_service.get_user_templates(user_id, template_type)
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'templates': templates,
            'total': len(templates),
            'filtered_by': template_type
        }), 200
        
    except Exception as e:
        logger.error(f"Error en get_user_templates: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


# =====================================================
# DESCARGA DE ARCHIVOS
# =====================================================

@report_bp.route('/download/template/<int:template_id>', methods=['GET'])
def download_template(template_id):
    """
    Descarga un archivo de plantilla
    
    Response:
        200: Archivo descargado
        404: Plantilla o archivo no existe
    """
    try:
        logger.info(f"Descargando plantilla template_id={template_id}")
        
        template = report_service.get_template(template_id)
        
        if not template:
            return jsonify({
                'success': False,
                'error': 'Plantilla no encontrada'
            }), 404
        
        filepath = template.get('file_path')
        
        if not filepath or not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'error': 'Archivo no encontrado'
            }), 404
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=template.get('file_name')
        )
        
    except Exception as e:
        logger.error(f"Error en download_template: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


# =====================================================
# DATOS DE VISUALIZACIÓN
# =====================================================

@report_bp.route('/visualizations/<int:user_id>', methods=['GET'])
def get_visualization_data(user_id):
    """
    Obtiene datos para visualizaciones (Chart.js)
    
    Response:
        200: Datos de gráficos
        404: Usuario no encontrado
    """
    try:
        logger.info(f"Obteniendo datos de visualización para user_id={user_id}")
        
        # Verificar usuario
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'error': 'Usuario no encontrado'
            }), 404
        
        data = report_service.get_visualization_data_for_frontend(user_id)
        
        if not data['success']:
            return jsonify(data), 400
        
        return jsonify(data), 200
        
    except Exception as e:
        logger.error(f"Error en get_visualization_data: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


# =====================================================
# HEALTH CHECK
# =====================================================

@report_bp.route('/health', methods=['GET'])
def health_check():
    """
    Verifica que el servicio de reportes está funcionando
    
    Response:
        200: Servicio operativo
    """
    return jsonify({
        'success': True,
        'service': 'Report Generation Service',
        'status': 'operational',
        'endpoints': {
            'generate_report': 'POST /api/reports/generate',
            'get_report': 'GET /api/reports/<report_id>',
            'user_reports': 'GET /api/reports/user/<user_id>',
            'generate_ppt': 'POST /api/reports/template/ppt',
            'generate_docx': 'POST /api/reports/template/docx',
            'get_template': 'GET /api/reports/templates/<template_id>',
            'user_templates': 'GET /api/reports/templates/user/<user_id>',
            'download': 'GET /api/reports/download/template/<template_id>',
            'visualizations': 'GET /api/reports/visualizations/<user_id>'
        }
    }), 200