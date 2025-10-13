"""
app/utils/file_handler.py - Utilidades para Manejo de Archivos
Plataforma Integral de Rendimiento Estudiantil

Funciones para subir, validar, guardar y eliminar archivos de forma segura.
"""

import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import current_app


class FileHandler:
    """
    Clase para manejar operaciones con archivos de forma segura
    """
    
    @staticmethod
    def validate_file(file, allowed_extensions, max_size_mb):
        """
        Validar archivo subido
        
        Args:
            file: Objeto de archivo de Flask
            allowed_extensions (list): Extensiones permitidas
            max_size_mb (int): Tamaño máximo en MB
        
        Returns:
            tuple: (is_valid, error_message)
        """
        if not file:
            return False, "No se proporcionó ningún archivo"
        
        if file.filename == '':
            return False, "El archivo no tiene nombre"
        
        # Validar extensión
        if not FileHandler.allowed_file(file.filename, allowed_extensions):
            return False, f"Tipo de archivo no permitido. Permitidos: {', '.join(allowed_extensions)}"
        
        # Validar tamaño (si es posible)
        try:
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)  # Regresar al inicio
            
            max_size_bytes = max_size_mb * 1024 * 1024
            if file_size > max_size_bytes:
                return False, f"El archivo excede el tamaño máximo de {max_size_mb}MB"
        except:
            pass  # Si no se puede verificar el tamaño, continuar
        
        return True, None
    
    @staticmethod
    def allowed_file(filename, allowed_extensions):
        """
        Verificar si la extensión del archivo está permitida
        
        Args:
            filename (str): Nombre del archivo
            allowed_extensions (list): Lista de extensiones permitidas
        
        Returns:
            bool: True si está permitida
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    @staticmethod
    def save_file(file, upload_folder, prefix=''):
        """
        Guardar archivo de forma segura con nombre único
        
        Args:
            file: Objeto de archivo de Flask
            upload_folder (str): Carpeta donde guardar
            prefix (str): Prefijo para el nombre del archivo
        
        Returns:
            dict: Información del archivo guardado
                {
                    'filename': str,
                    'filepath': str,
                    'file_size': int,
                    'mime_type': str
                }
        """
        # Crear carpeta si no existe
        os.makedirs(upload_folder, exist_ok=True)
        
        # Nombre seguro del archivo original
        original_filename = secure_filename(file.filename)
        
        # Generar nombre único
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{prefix}_{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
        
        # Ruta completa
        filepath = os.path.join(upload_folder, unique_filename)
        
        # Guardar archivo
        file.save(filepath)
        
        # Obtener información del archivo
        file_size = os.path.getsize(filepath)
        mime_type = file.content_type if hasattr(file, 'content_type') else None
        
        return {
            'filename': unique_filename,
            'filepath': filepath,
            'file_size': file_size,
            'mime_type': mime_type,
            'original_filename': original_filename
        }
    
    @staticmethod
    def delete_file(filepath):
        """
        Eliminar archivo de forma segura
        
        Args:
            filepath (str): Ruta del archivo a eliminar
        
        Returns:
            bool: True si se eliminó exitosamente
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"Error al eliminar archivo: {e}")
            return False
    
    @staticmethod
    def get_file_info(filepath):
        """
        Obtener información de un archivo
        
        Args:
            filepath (str): Ruta del archivo
        
        Returns:
            dict: Información del archivo
        """
        if not os.path.exists(filepath):
            return None
        
        stat = os.stat(filepath)
        
        return {
            'exists': True,
            'size': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'created': datetime.fromtimestamp(stat.st_ctime),
            'modified': datetime.fromtimestamp(stat.st_mtime),
            'extension': os.path.splitext(filepath)[1][1:].lower()
        }
    
    @staticmethod
    def ensure_folder_exists(folder_path):
        """
        Asegurar que una carpeta existe, crearla si no
        
        Args:
            folder_path (str): Ruta de la carpeta
        """
        os.makedirs(folder_path, exist_ok=True)
    
    @staticmethod
    def get_upload_path(subfolder=''):
        """
        Obtener ruta de carpeta de uploads
        
        Args:
            subfolder (str): Subcarpeta dentro de uploads
        
        Returns:
            str: Ruta completa
        """
        base_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        if subfolder:
            return os.path.join(base_folder, subfolder)
        return base_folder


# Instancia global
file_handler = FileHandler()