"""
app/services/report_service.py
Servicio principal de generación de reportes
Orquesta PPT, DOCX y visualizaciones
"""

from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.student_profile import StudentProfile
from app.models.report import Report
from app.models.generated_template import GeneratedTemplate
from app.models.user import User
from app.services.report_generation.ppt_generator import ppt_generator
from app.services.report_generation.docx_generator import docx_generator
from app.services.report_generation.data_visualizer import data_visualizer
from app.services.ai.gemini_service import gemini_service
from app.utils.logger import logger
from app.services.report_generation.pdf_generator import pdf_generator


class ReportService:
    """
    Servicio principal de generación de reportes
    Gestiona la creación de reportes y plantillas personalizadas
    """
    
    def __init__(self):
        self.logger = logger
    
    # =====================================================
    # GENERACIÓN DE REPORTES COMPLETOS
    # =====================================================
    
    def generate_complete_report(
        self,
        user_id: int,
        report_type: str = 'integral',
        include_ppt: bool = True,
        include_docx: bool = True
    ) -> Dict:
        """
        Genera un reporte completo con múltiples formatos
        
        Args:
            user_id: ID del usuario
            report_type: Tipo de reporte (integral, semestral, curso)
            include_ppt: Generar PowerPoint
            include_docx: Generar Word
            
        Returns:
            Dict con información de los archivos generados
        """
        try:
            self.logger.info(f"Generando reporte completo para user_id={user_id}")
            
            # Verificar usuario
            user = User.query.get(user_id)
            if not user:
                self.logger.error(f"Usuario {user_id} no encontrado")
                return {'success': False, 'error': 'Usuario no encontrado'}
            
            # Obtener perfil
            profile = StudentProfile.query.filter_by(user_id=user_id).first()
            if not profile:
                self.logger.error(f"No hay perfil generado para user_id={user_id}")
                return {
                    'success': False,
                    'error': 'No hay perfil generado',
                    'message': 'Debes generar tu perfil primero. Ve a "Avatar Personal" → "Generar Perfil"'
                }
            
            # Crear registro de reporte en BD
            report = Report(
                user_id=user_id,
                title=f"Reporte {report_type.title()} - {datetime.now().strftime('%B %Y')}",
                report_type=report_type,
                description=f"Reporte generado automáticamente del perfil académico",
                generation_status='generating'
            )
            db.session.add(report)
            db.session.commit()
            
            self.logger.info(f"Reporte creado con ID={report.id}")
            
            result = {
                'success': True,
                'report_id': report.id,
                'user_id': user_id,
                'report_type': report_type,
                'generated_files': []
            }
            
            # Generar PPT
            if include_ppt:
                ppt_result = self._generate_ppt_report(profile, user_id, report)
                if ppt_result['success']:
                    result['generated_files'].append(ppt_result)
                    result['ppt_file'] = ppt_result
            
            # Generar DOCX
            if include_docx:
                print(f"[DEBUG] Intentando generar DOCX para user_id={user_id}")  
                docx_result = self._generate_docx_report(profile, user_id, report, report_type)
                print(f"[DEBUG] Resultado DOCX: {docx_result}")  
                if docx_result['success']:
                    result['generated_files'].append(docx_result)
                    result['docx_file'] = docx_result

                    # Generar PDF desde DOCX
                    pdf_result = self._generate_pdf_from_docx(docx_result['filepath'], user_id, report)
                    if pdf_result['success']:
                        result['generated_files'].append(pdf_result)
                        result['pdf_file'] = pdf_result
                else:
                    print(f"[DEBUG] Error generando DOCX: {docx_result.get('error')}")  
            
            # Generar datos de visualización
            viz_data = self._generate_visualization_data(profile, user_id)
            result['visualization_data'] = viz_data
            
            # Actualizar reporte en BD
            report.generation_status = 'completed'
            report.generation_completed_at = datetime.utcnow()
            report.report_data = {
                'files_generated': len(result['generated_files']),
                'ppt_included': include_ppt,
                'docx_included': include_docx,
                'generation_timestamp': datetime.utcnow().isoformat()
            }
            db.session.commit()
            
            self.logger.info(f"Reporte completo generado: {len(result['generated_files'])} archivos")
            
            return result
            
        except SQLAlchemyError as e:
            db.session.rollback()
            self.logger.error(f"Error BD en reporte: {str(e)}")
            return {'success': False, 'error': 'Error de base de datos'}
        except Exception as e:
            self.logger.error(f"Error generando reporte: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}
    
    # =====================================================
    # GENERACIÓN DE PLANTILLAS INDIVIDUALES
    # =====================================================
    
    def generate_ppt_template(
        self,
        user_id: int,
        topic: str,
        slides_count: int = 10,
        style: str = 'academic'
    ) -> Dict:
        """
        Genera una plantilla PPT personalizada según el perfil
        
        Args:
            user_id: ID del usuario
            topic: Tema de la presentación
            slides_count: Número de slides
            style: Estilo (academic, professional, creative)
            
        Returns:
            Dict con información del archivo generado
        """
        try:
            self.logger.info(f"Generando plantilla PPT para user_id={user_id}, topic={topic}")
            
            # Obtener perfil
            profile = StudentProfile.query.filter_by(user_id=user_id).first()
            
            # Generar contenido con IA
            content = self._generate_presentation_content_with_ai(
                user_id, profile, topic, slides_count, style
            )
            
            # Crear plantilla usando PPT generator
            result = ppt_generator.generate_student_report_ppt(
                profile=profile,
                user_id=user_id,
                title=topic
            )
            
            if result['success']:
                # Registrar plantilla en BD
                template = GeneratedTemplate(
                    user_id=user_id,
                    title=topic,
                    template_type='ppt',
                    topic=topic,
                    file_path=result['filepath'],
                    file_name=result['filename'],
                    file_size=result['file_size'],
                    personalization_applied={
                        'learning_style': profile.learning_style if profile else 'general',
                        'style': style,
                        'slides_count': slides_count
                    },
                    visual_style=style,
                    ai_model_used='gemini-pro',
                    generation_status='completed'
                )
                db.session.add(template)
                db.session.commit()
                
                result['template_id'] = template.id
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error generando plantilla PPT: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def generate_docx_template(
        self,
        user_id: int,
        topic: str,
        document_type: str = 'informe'
    ) -> Dict:
        """
        Genera una plantilla DOCX personalizada
        
        Args:
            user_id: ID del usuario
            topic: Tema del documento
            document_type: Tipo (informe, ensayo, monografia)
            
        Returns:
            Dict con información del archivo generado
        """
        try:
            self.logger.info(f"Generando plantilla DOCX para user_id={user_id}")
            
            # Obtener perfil
            profile = StudentProfile.query.filter_by(user_id=user_id).first()
            
            # Generar con DOCX generator
            result = docx_generator.generate_detailed_report(
                profile=profile,
                user_id=user_id,
                report_type='academico'
            )
            
            if result['success']:
                # Registrar en BD
                template = GeneratedTemplate(
                    user_id=user_id,
                    title=topic,
                    template_type='docx',
                    topic=topic,
                    file_path=result['filepath'],
                    file_name=result['filename'],
                    file_size=result['file_size'],
                    personalization_applied={
                        'document_type': document_type,
                        'learning_style': profile.learning_style if profile else 'general'
                    },
                    ai_model_used='gemini-pro',
                    generation_status='completed'
                )
                db.session.add(template)
                db.session.commit()
                
                result['template_id'] = template.id
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error generando plantilla DOCX: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    # =====================================================
    # MÉTODOS PRIVADOS - GENERACIÓN
    # =====================================================
    
    def _generate_ppt_report(
        self,
        profile: StudentProfile,
        user_id: int,
        report: Report
    ) -> Dict:
        """Genera archivo PPT del reporte"""
        try:
            result = ppt_generator.generate_student_report_ppt(
                profile=profile,
                user_id=user_id,
                title=report.title
            )
            
            if result['success']:
                # Registrar como template
                template = GeneratedTemplate(
                    user_id=user_id,
                    report_id=report.id,
                    title=report.title,
                    template_type='ppt',
                    file_path=result['filepath'],
                    file_name=result['filename'],
                    file_size=result['file_size'],
                    generation_status='completed'
                )
                db.session.add(template)
                db.session.commit()
                
                result['template_id'] = template.id
                result['type'] = 'ppt'
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error generando PPT: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _generate_docx_report(
        self,
        profile: StudentProfile,
        user_id: int,
        report: Report,
        report_type: str
    ) -> Dict:
        """Genera archivo DOCX del reporte"""
        try:
            # Determinar tipo de reporte DOCX
            docx_type = 'ejecutivo'  # Temporal: completo tiene bugs
            
            # AGREGAR ESTE LOG
            self.logger.info(f"Generando DOCX tipo={docx_type} para user_id={user_id}")
        

            result = docx_generator.generate_detailed_report(
                profile=profile,
                user_id=user_id,
                report_type=docx_type
            )
            
            # AGREGAR ESTE LOG
            self.logger.info(f"Resultado DOCX: {result}")

            if result['success']:
                # Registrar como template
                template = GeneratedTemplate(
                    user_id=user_id,
                    report_id=report.id,
                    title=report.title,
                    template_type='docx',
                    file_path=result['filepath'],
                    file_name=result['filename'],
                    file_size=result['file_size'],
                    generation_status='completed'
                )
                db.session.add(template)
                db.session.commit()
                
                result['template_id'] = template.id
                result['type'] = 'docx'
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error generando DOCX: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}
    
    def _generate_visualization_data(self, profile: StudentProfile, user_id: int) -> Dict:
        """Genera datos para visualizaciones"""
        try:
            return {
                'thesis_readiness': data_visualizer.get_thesis_readiness_chart_data(profile),
                'progress_timeline': data_visualizer.get_progress_timeline_data(user_id),
                'attention_distribution': data_visualizer.get_attention_distribution_data(user_id),
                'strengths_weaknesses': data_visualizer.get_strengths_weaknesses_comparison(profile),
                'session_activity': data_visualizer.get_session_activity_data(user_id, days=30),
                'summary_stats': data_visualizer.get_summary_stats(profile, user_id)
            }
        except Exception as e:
            self.logger.error(f"Error generando visualizaciones: {str(e)}")
            return {}
    
    def _generate_presentation_content_with_ai(
        self,
        user_id: int,
        profile: Optional[StudentProfile],
        topic: str,
        slides_count: int,
        style: str
    ) -> Dict:
        """Genera contenido de presentación con IA"""
        try:
            learning_style = profile.learning_style if profile else 'general'
            
            prompt = f"""Genera el contenido para una presentación de {slides_count} slides sobre: {topic}

Estilo: {style}
Estilo de aprendizaje del estudiante: {learning_style}

Para cada slide, genera:
- Título
- 3-4 puntos clave
- Sugerencia visual

Adapta el contenido al estilo de aprendizaje {learning_style}.
Formato: Slide N: Titulo | Punto 1 | Punto 2 | Punto 3 | Visual"""
            
            response = gemini_service.generate_content(
                prompt=prompt,
                user_id=user_id,
                context="presentation_content"
            )
            
            if response['success']:
                return {'content': response['content']}
            
            return {'content': 'Contenido genérico'}
            
        except Exception as e:
            self.logger.error(f"Error generando contenido: {str(e)}")
            return {'content': ''}
    
    # =====================================================
    # MÉTODOS DE CONSULTA
    # =====================================================
    
    def get_report(self, report_id: int) -> Optional[Dict]:
        """Obtiene un reporte por ID"""
        try:
            report = Report.query.get(report_id)
            if not report:
                return None
            
            return report.to_dict()
        except Exception as e:
            self.logger.error(f"Error obteniendo reporte: {str(e)}")
            return None
    
    def get_user_reports(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Obtiene reportes de un usuario"""
        try:
            reports = Report.query.filter_by(
                user_id=user_id
            ).order_by(
                Report.created_at.desc()
            ).limit(limit).all()
            
            return [r.to_dict() for r in reports]
        except Exception as e:
            self.logger.error(f"Error obteniendo reportes: {str(e)}")
            return []
    
    def get_template(self, template_id: int) -> Optional[Dict]:
        """Obtiene una plantilla por ID"""
        try:
            template = GeneratedTemplate.query.get(template_id)
            if not template:
                return None
            
            return template.to_dict()
        except Exception as e:
            self.logger.error(f"Error obteniendo plantilla: {str(e)}")
            return None
    
    def get_user_templates(self, user_id: int, template_type: Optional[str] = None) -> List[Dict]:
        """Obtiene plantillas de un usuario"""
        try:
            query = GeneratedTemplate.query.filter_by(user_id=user_id)
            
            if template_type:
                query = query.filter_by(template_type=template_type)
            
            templates = query.order_by(
                GeneratedTemplate.created_at.desc()
            ).all()
            
            return [t.to_dict() for t in templates]
        except Exception as e:
            self.logger.error(f"Error obteniendo plantillas: {str(e)}")
            return []
    
    # =====================================================
    # DATOS PARA FRONTEND
    # =====================================================
    
    def get_visualization_data_for_frontend(self, user_id: int) -> Dict:
        """
        Obtiene todos los datos de visualización para el frontend
        Formato compatible con Chart.js
        """
        try:
            profile = StudentProfile.query.filter_by(user_id=user_id).first()
            
            if not profile:
                return {
                    'success': False,
                    'error': 'No hay perfil generado'
                }
            
            data = self._generate_visualization_data(profile, user_id)
            
            return {
                'success': True,
                'user_id': user_id,
                'charts': data,
                'last_updated': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error obteniendo datos frontend: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    def _generate_pdf_from_docx(self, docx_path: str, user_id: int, report: Report) -> Dict:
        """Genera PDF desde DOCX"""
        try:
            result = pdf_generator.convert_docx_to_pdf(docx_path)
        
            if result['success']:
                # Registrar como template
                template = GeneratedTemplate(
                    user_id=user_id,
                    report_id=report.id,
                    title=report.title,
                    template_type='pdf',
                    file_path=result['filepath'],
                    file_name=result['filename'],
                    file_size=result['file_size'],
                    generation_status='completed'
                )
                db.session.add(template)
                db.session.commit()
            
                result['template_id'] = template.id
                result['type'] = 'pdf'
        
            return result
        
        except Exception as e:
            self.logger.error(f"Error generando PDF: {str(e)}")
            return {'success': False, 'error': str(e)}

# Instancia única
report_service = ReportService()