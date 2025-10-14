"""
Servicio de Perfil Integral - ADAPTADO a modelo existente
Compatible con student_profile.py actual
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy import func, desc
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.student_profile import StudentProfile
from app.models.video_session import VideoSession
from app.models.emotion_data import EmotionData
from app.models.attention_metrics import AttentionMetrics
from app.models.audio_session import AudioSession
from app.models.audio_transcription import AudioTranscription
from app.models.document import Document
from app.models.text_analysis import TextAnalysis
from app.models.user import User
from app.services.ai.gemini_service import gemini_service
from app.utils.logger import logger


class ProfileService:
    """Servicio para gestión de perfiles integrales"""
    
    def __init__(self):
        self.logger = logger
    
    def generate_profile(self, user_id: int, force_regenerate: bool = False) -> Dict:
        """Genera o actualiza el perfil integral"""
        try:
            self.logger.info(f"Generando perfil para user_id={user_id}")
            
            # Verificar usuario
            user = User.query.get(user_id)
            if not user:
                return {'success': False, 'error': 'Usuario no encontrado'}
            
            # Verificar perfil existente
            existing_profile = StudentProfile.query.filter_by(user_id=user_id).first()
            
            if existing_profile and not force_regenerate:
                if existing_profile.last_updated:
                    age = (datetime.utcnow() - existing_profile.last_updated).total_seconds()
                    if age < 86400:  # 24 horas
                        self.logger.info("Retornando perfil existente")
                        return self._build_response(existing_profile)
            
            # Recopilar datos
            data = self._aggregate_data(user_id)
            
            if not data['has_data']:
                return {
                    'success': False,
                    'error': 'No hay suficientes datos para generar el perfil',
                    'message': 'El estudiante debe tener al menos una sesión de video o documento analizado'
                }
            
            # Crear o actualizar perfil
            if existing_profile:
                profile = existing_profile
            else:
                profile = StudentProfile(user_id=user_id)
                db.session.add(profile)
            
            # Regenerar perfil usando método del modelo
            profile.regenerate_profile()
            profile.identify_strengths_and_weaknesses()
            profile.generate_recommendations()
            
            # Generar resumen IA personalizado
            ai_summary = self._generate_ai_summary(user_id, profile, data)
            profile.ai_profile_summary = ai_summary
            
            db.session.commit()
            self.logger.info(f"Perfil generado. Score: {profile.thesis_readiness_score}")
            
            return self._build_response(profile)
            
        except SQLAlchemyError as e:
            db.session.rollback()
            self.logger.error(f"Error BD: {str(e)}")
            return {'success': False, 'error': 'Error de base de datos', 'detail': str(e)}
        except Exception as e:
            self.logger.error(f"Error inesperado: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}
    
    def _aggregate_data(self, user_id: int) -> Dict:
        """Recopila datos del estudiante"""
        data = {
            'user_id': user_id,
            'has_data': False,
            'total_documents': 0,
            'total_video_sessions': 0,
            'total_audio_sessions': 0,
        }
        
        # Contar documentos completados
        data['total_documents'] = Document.query.filter_by(
            user_id=user_id,
            processing_status='completed'
        ).count()
        
        # Contar sesiones de video completadas
        data['total_video_sessions'] = VideoSession.query.filter_by(
            user_id=user_id,
            processing_status='completed'
        ).count()
        
        # Contar sesiones de audio
        data['total_audio_sessions'] = AudioSession.query.filter_by(
            user_id=user_id
        ).count()
        
        data['has_data'] = (
            data['total_documents'] > 0 or 
            data['total_video_sessions'] > 0 or 
            data['total_audio_sessions'] > 0
        )
        
        return data
    
    def _generate_ai_summary(self, user_id: int, profile: StudentProfile, data: Dict) -> str:
        """Genera resumen con IA"""
        try:
            user = User.query.get(user_id)
            name = user.first_name if user and hasattr(user, 'first_name') else "Estudiante"
            
            # Obtener todas las fortalezas y debilidades
            all_strengths = []
            if profile.academic_strengths:
                all_strengths.extend(profile.academic_strengths)
            if profile.writing_strengths:
                all_strengths.extend(profile.writing_strengths)
            if profile.technical_strengths:
                all_strengths.extend(profile.technical_strengths)
            
            all_weaknesses = []
            if profile.academic_weaknesses:
                all_weaknesses.extend(profile.academic_weaknesses)
            if profile.writing_weaknesses:
                all_weaknesses.extend(profile.writing_weaknesses)
            if profile.areas_for_improvement:
                all_weaknesses.extend(profile.areas_for_improvement)
            
            prompt = f"""Como experto académico, genera un resumen personalizado para {name}.

DATOS DEL PERFIL:
- Documentos analizados: {profile.total_documents_analyzed}
- Sesiones completadas: {profile.total_sessions_completed}
- Calidad de escritura: {float(profile.avg_writing_quality or 0):.1f}/100
- Riqueza de vocabulario: {float(profile.avg_vocabulary_richness or 0):.1f}/100
- Tendencia: {profile.writing_improvement_trend or 'sin datos'}
- Score preparación tesis: {float(profile.thesis_readiness_score or 0):.1f}/100
- Nivel: {profile.thesis_readiness_level or 'sin evaluar'}
- Estilo de aprendizaje: {profile.learning_style or 'no determinado'}
- Span de atención: {profile.avg_attention_span_minutes or 0} minutos

FORTALEZAS IDENTIFICADAS:
{chr(10).join(f'- {s}' for s in all_strengths) if all_strengths else '- Aún construyendo perfil'}

DEBILIDADES IDENTIFICADAS:
{chr(10).join(f'- {w}' for w in all_weaknesses) if all_weaknesses else '- Sin áreas críticas identificadas'}

INSTRUCCIONES:
1. Genera un resumen en 3 párrafos (máximo 250 palabras)
2. Usa un tono profesional pero cercano y motivador
3. Destaca las fortalezas de manera específica
4. Menciona áreas de mejora como oportunidades de crecimiento
5. Incluye una recomendación específica y accionable
6. NO uses formato markdown ni listas
7. Escribe en párrafos fluidos y naturales

Genera el resumen:"""
            
            response = gemini_service.generate_content(
                prompt=prompt,
                user_id=user_id,
                context="student_profile_summary"
            )
            
            if response['success']:
                return response['content']
            else:
                self.logger.error(f"Error Gemini: {response.get('error')}")
                return self._fallback_summary(name, profile, all_strengths, all_weaknesses)
        
        except Exception as e:
            self.logger.error(f"Error generando resumen: {str(e)}")
            return self._fallback_summary("Estudiante", profile, [], [])
    
    def _fallback_summary(self, name: str, profile: StudentProfile, 
                         strengths: List[str], weaknesses: List[str]) -> str:
        """Resumen de respaldo si falla Gemini"""
        thesis_score = float(profile.thesis_readiness_score or 0)
        writing_quality = float(profile.avg_writing_quality or 0)
        
        strength_text = strengths[0] if strengths else "potencial académico en desarrollo"
        weakness_text = weaknesses[0] if weaknesses else "mantener consistencia en el estudio"
        
        return f"""{name} muestra un perfil académico {'consolidado' if thesis_score > 60 else 'en desarrollo'}. Con un score de preparación para tesis de {thesis_score:.0f}/100 y una calidad de escritura promedio de {writing_quality:.0f}/100, demuestra {'sólido' if writing_quality > 70 else 'creciente'} compromiso con su formación académica.

Entre sus principales fortalezas destaca: {strength_text}. Sin embargo, se identifica como área de oportunidad: {weakness_text}.

Se recomienda continuar desarrollando hábitos de estudio regulares y fortalecer las áreas identificadas para optimizar el rendimiento académico y la preparación para proyectos de mayor envergadura como la tesis."""
    
    # =====================================================
    # MÉTODOS DE CONSULTA
    # =====================================================
    
    def get_profile(self, user_id: int) -> Optional[Dict]:
        """Obtiene perfil existente"""
        try:
            profile = StudentProfile.query.filter_by(user_id=user_id).first()
            if not profile:
                return None
            return self._build_response(profile)
        except Exception as e:
            self.logger.error(f"Error obteniendo perfil: {str(e)}")
            return None
    
    def get_strengths(self, user_id: int) -> List[str]:
        """Obtiene todas las fortalezas"""
        profile = StudentProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            return []
        
        strengths = []
        if profile.academic_strengths:
            strengths.extend(profile.academic_strengths)
        if profile.writing_strengths:
            strengths.extend(profile.writing_strengths)
        if profile.technical_strengths:
            strengths.extend(profile.technical_strengths)
        
        return strengths
    
    def get_weaknesses(self, user_id: int) -> List[str]:
        """Obtiene todas las debilidades"""
        profile = StudentProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            return []
        
        weaknesses = []
        if profile.academic_weaknesses:
            weaknesses.extend(profile.academic_weaknesses)
        if profile.writing_weaknesses:
            weaknesses.extend(profile.writing_weaknesses)
        if profile.areas_for_improvement:
            weaknesses.extend(profile.areas_for_improvement)
        
        return weaknesses
    
    def get_recommendations(self, user_id: int) -> List[str]:
        """Obtiene recomendaciones"""
        profile = StudentProfile.query.filter_by(user_id=user_id).first()
        if not profile:
            return []
        
        recommendations = []
        if profile.study_recommendations:
            recommendations.extend(profile.study_recommendations)
        if profile.resource_recommendations:
            recommendations.extend(profile.resource_recommendations)
        
        return recommendations
    
    def _build_response(self, profile: StudentProfile) -> Dict:
        """Construye respuesta completa del perfil"""
        thesis_score = float(profile.thesis_readiness_score or 0)
        
        # Usar el método to_dict del modelo con detalles
        profile_data = profile.to_dict(include_detailed=True)
        
        return {
            'success': True,
            'profile': profile_data,
            'thesis_readiness': {
                'score': thesis_score,
                'level': profile.thesis_readiness_level or 'No evaluado',
                'message': self._get_readiness_message(thesis_score),
                'estimated_months': profile.estimated_preparation_months
            },
            'summary': profile.ai_profile_summary,
            'strengths': self.get_strengths(profile.user_id),
            'weaknesses': self.get_weaknesses(profile.user_id),
            'recommendations': self.get_recommendations(profile.user_id),
            'learning_style': profile.learning_style,
            'metrics': {
                'attention_score': profile.avg_attention_span_minutes or 0,
                'writing_quality': float(profile.avg_writing_quality or 0),
                'vocabulary_score': float(profile.avg_vocabulary_richness or 0),
                'total_documents': profile.total_documents_analyzed,
                'total_sessions': profile.total_sessions_completed
            },
            'last_updated': profile.last_updated.isoformat() if profile.last_updated else None
        }
    
    def _get_readiness_message(self, score: float) -> str:
        """Mensaje según score de preparación"""
        if score >= 80:
            return "¡Excelente! Estás muy bien preparado para comenzar tu tesis"
        elif score >= 65:
            return "Buen nivel de preparación. Con algunas mejoras estarás listo para la tesis"
        elif score >= 45:
            return "Nivel moderado. Se recomienda fortalecer áreas clave antes de la tesis"
        elif score >= 30:
            return "Necesitas trabajar en varios aspectos antes de la tesis"
        else:
            return "Se requiere preparación significativa antes de abordar la tesis"


# Instancia única
profile_service = ProfileService()