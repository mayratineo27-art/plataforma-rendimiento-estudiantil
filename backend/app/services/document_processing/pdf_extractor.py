"""
Servicio para extraer texto de archivos PDF
Utiliza PyPDF2 para procesar documentos PDF
"""
import PyPDF2
import os

class PDFExtractor:
    """Extractor de texto desde archivos PDF"""
    
    @staticmethod
    def extract_text(pdf_path):
        """
        Extrae todo el texto de un archivo PDF
        
        Args:
            pdf_path (str): Ruta al archivo PDF
            
        Returns:
            str: Texto extraído del PDF
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"El archivo {pdf_path} no existe")
        
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            return text.strip()
        
        except Exception as e:
            print(f"❌ Error extrayendo texto del PDF: {e}")
            raise Exception(f"Error al procesar el PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_page(pdf_path, page_number):
        """
        Extrae texto de una página específica
        
        Args:
            pdf_path (str): Ruta al archivo PDF
            page_number (int): Número de página (0-indexed)
            
        Returns:
            str: Texto de la página
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                if page_number >= len(pdf_reader.pages):
                    raise ValueError(f"La página {page_number} no existe en el PDF")
                
                page = pdf_reader.pages[page_number]
                return page.extract_text().strip()
        
        except Exception as e:
            print(f"❌ Error extrayendo página {page_number}: {e}")
            raise Exception(f"Error al procesar la página: {str(e)}")
    
    @staticmethod
    def get_page_count(pdf_path):
        """
        Obtiene el número total de páginas del PDF
        
        Args:
            pdf_path (str): Ruta al archivo PDF
            
        Returns:
            int: Número de páginas
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        
        except Exception as e:
            print(f"❌ Error contando páginas: {e}")
            return 0
    
    @staticmethod
    def get_metadata(pdf_path):
        """
        Extrae metadatos del PDF
        
        Args:
            pdf_path (str): Ruta al archivo PDF
            
        Returns:
            dict: Metadatos del PDF
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata
                
                return {
                    'title': metadata.get('/Title', 'Sin título'),
                    'author': metadata.get('/Author', 'Desconocido'),
                    'subject': metadata.get('/Subject', ''),
                    'creator': metadata.get('/Creator', ''),
                    'producer': metadata.get('/Producer', ''),
                    'pages': len(pdf_reader.pages)
                }
        
        except Exception as e:
            print(f"❌ Error extrayendo metadatos: {e}")
            return {}
