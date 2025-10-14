"""
app/services/report_generation/pdf_generator.py
Conversión de DOCX a PDF usando LibreOffice
"""

import os
import subprocess
from typing import Dict
from app.utils.logger import logger


class PDFGenerator:
    """
    Generador de PDFs desde archivos DOCX
    Usa LibreOffice en modo headless
    """
    
    def __init__(self):
        self.logger = logger
        # Directorio de salida
        self.output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'generated', 'pdf'
        )
        os.makedirs(self.output_dir, exist_ok=True)
    
    def convert_docx_to_pdf(self, docx_path: str) -> Dict:
        """
        Convierte un archivo DOCX a PDF usando LibreOffice
        
        Args:
            docx_path: Ruta completa al archivo DOCX
            
        Returns:
            Dict con información del PDF generado
        """
        try:
            self.logger.info(f"Convirtiendo DOCX a PDF: {docx_path}")
            
            # Verificar que el archivo existe
            if not os.path.exists(docx_path):
                return {
                    'success': False,
                    'error': 'Archivo DOCX no encontrado'
                }
            
            # Detectar comando de LibreOffice según sistema operativo
            libreoffice_cmd = self._get_libreoffice_command()
            
            if not libreoffice_cmd:
                return {
                    'success': False,
                    'error': 'LibreOffice no instalado',
                    'message': 'Instala LibreOffice para generar PDFs'
                }
            
            # Comando de conversión
            # --headless: sin interfaz gráfica
            # --convert-to pdf: formato de salida
            # --outdir: directorio de salida
            cmd = [
                libreoffice_cmd,
                '--headless',
                '--convert-to',
                'pdf',
                '--outdir',
                self.output_dir,
                docx_path
            ]
            
            # Ejecutar conversión
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60  # Timeout de 60 segundos
            )
            
            if result.returncode != 0:
                self.logger.error(f"Error LibreOffice: {result.stderr}")
                return {
                    'success': False,
                    'error': 'Error en conversión',
                    'details': result.stderr
                }
            
            # Determinar nombre del PDF generado
            docx_filename = os.path.basename(docx_path)
            pdf_filename = docx_filename.replace('.docx', '.pdf')
            pdf_path = os.path.join(self.output_dir, pdf_filename)
            
            # Verificar que se creó el PDF
            if not os.path.exists(pdf_path):
                return {
                    'success': False,
                    'error': 'PDF no se generó correctamente'
                }
            
            file_size = os.path.getsize(pdf_path)
            
            self.logger.info(f"PDF generado exitosamente: {pdf_path}")
            
            return {
                'success': True,
                'filepath': pdf_path,
                'filename': pdf_filename,
                'file_size': file_size
            }
            
        except subprocess.TimeoutExpired:
            self.logger.error("Timeout en conversión a PDF")
            return {
                'success': False,
                'error': 'Timeout en conversión (>60s)'
            }
        except Exception as e:
            self.logger.error(f"Error convirtiendo a PDF: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_libreoffice_command(self) -> str:
        """
        Detecta el comando de LibreOffice según el sistema operativo
        
        Returns:
            Comando de LibreOffice o None si no está instalado
        """
        import platform
        
        system = platform.system()
        
        # Posibles ubicaciones de LibreOffice
        if system == 'Windows':
            possible_paths = [
                r'C:\Program Files\LibreOffice\program\soffice.exe',
                r'C:\Program Files (x86)\LibreOffice\program\soffice.exe',
                r'C:\Program Files\LibreOffice 7\program\soffice.exe',
                r'C:\Program Files (x86)\LibreOffice 7\program\soffice.exe'
            ]
        elif system == 'Darwin':  # macOS
            possible_paths = [
                '/Applications/LibreOffice.app/Contents/MacOS/soffice'
            ]
        else:  # Linux
            possible_paths = [
                '/usr/bin/libreoffice',
                '/usr/bin/soffice'
            ]
        
        # Verificar cuál existe
        for path in possible_paths:
            if os.path.exists(path):
                self.logger.info(f"LibreOffice encontrado: {path}")
                return path
        
        # Intentar con comando en PATH
        try:
            result = subprocess.run(
                ['libreoffice', '--version'],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return 'libreoffice'
        except:
            pass
        
        try:
            result = subprocess.run(
                ['soffice', '--version'],
                capture_output=True,
                timeout=5
            )
            if result.returncode == 0:
                return 'soffice'
        except:
            pass
        
        self.logger.warning("LibreOffice no encontrado en el sistema")
        return None
    
    def is_libreoffice_installed(self) -> bool:
        """
        Verifica si LibreOffice está instalado
        
        Returns:
            True si está instalado, False si no
        """
        return self._get_libreoffice_command() is not None


# Instancia única
pdf_generator = PDFGenerator()