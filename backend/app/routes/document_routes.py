"""
app/routes/document_routes.py - Rutas de Documentos (Módulo 1)
Plataforma Integral de Rendimiento Estudiantil
"""

from flask import Blueprint, request, jsonify
# from app import db
# from app.models.document import Document
# from app.utils.file_handler import save_file, validate_file

# Crear blueprint
document_bp = Blueprint('documents', __name__)


@document_bp.route('/upload', methods=['POST'])
def upload_document():
    """
    Subir un documento académico para análisis
    
    Form data esperado:
    - file: archivo PDF o DOCX
    - title: título del documento
    - cycle: ciclo académico (1-10)
    - course_name: nombre del curso
    - document_type: tipo de documento (informe, trabajo_final, etc.)
    """
    # TODO: Implementar subida de archivos
    return jsonify({
        'message': 'Endpoint de subida de documentos - A implementar en Módulo 1'
    }), 501


@document_bp.route('/', methods=['GET'])
def list_documents():
    """
    Listar todos los documentos del usuario
    """
    # TODO: Implementar listado de documentos
    return jsonify({
        'message': 'Endpoint de listado de documentos - A implementar en Módulo 1'
    }), 501


@document_bp.route('/<int:document_id>', methods=['GET'])
def get_document(document_id):
    """
    Obtener información de un documento específico
    """
    return jsonify({
        'message': f'Endpoint de documento {document_id} - A implementar en Módulo 1'
    }), 501


@document_bp.route('/<int:document_id>', methods=['DELETE'])
def delete_document(document_id):
    """
    Eliminar un documento
    """
    return jsonify({
        'message': f'Endpoint de eliminación de documento {document_id} - A implementar en Módulo 1'
    }), 501


@document_bp.route('/<int:document_id>/analysis', methods=['GET'])
def get_document_analysis(document_id):
    """
    Obtener el análisis de un documento específico
    """
    return jsonify({
        'message': f'Endpoint de análisis de documento {document_id} - A implementar en Módulo 1'
    }), 501

@document_bp.route('/test', methods=['GET'])
def test():
    return {'message': 'Document routes working'}