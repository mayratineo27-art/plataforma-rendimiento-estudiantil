"""
app/services/ai/gemini_service.py - Servicio de Google Gemini
Plataforma Integral de Rendimiento Estudiantil

Este servicio centraliza todas las interacciones con la API de Google Gemini
para análisis de texto, generación de contenido y análisis de sentimientos.
"""

import os
import json
import time
from typing import Dict, List, Optional, Any
import google.generativeai as genai
from app import db
from app.models.ai_interactions import AIInteraction


class GeminiService:
    """
    Servicio para interactuar con Google Gemini API
    
    Maneja todas las llamadas a Gemini y registra las interacciones
    en la base de datos para tracking y análisis de costos.
    """
    
    def __init__(self):
        """Inicializar servicio de Gemini"""
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno")
        
        # Configurar Gemini
        genai.configure(api_key=api_key)
        
        # Configuración del modelo
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
        self.max_tokens = int(os.getenv('GEMINI_MAX_TOKENS', 8192))
        self.temperature = float(os.getenv('GEMINI_TEMPERATURE', 0.7))
        
        # Inicializar modelo
        self.model = genai.GenerativeModel(self.model_name)
    
    def generate_content(
        self,
        prompt: str,
        user_id: Optional[int] = None,
        interaction_type: str = 'content_generation',
        related_entity_type: Optional[str] = None,
        related_entity_id: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generar contenido con Gemini
        
        Args:
            prompt (str): Prompt para Gemini
            user_id (int, optional): ID del usuario
            interaction_type (str): Tipo de interacción
            related_entity_type (str, optional): Tipo de entidad relacionada
            related_entity_id (int, optional): ID de entidad relacionada
            **kwargs: Parámetros adicionales para la generación
        
        Returns:
            dict: Respuesta con contenido generado y metadata
        """
        start_time = time.time()
        
        try:
            # Configuración de generación
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=kwargs.get('max_tokens', self.max_tokens),
                temperature=kwargs.get('temperature', self.temperature),
            )
            
            # Generar contenido
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Calcular tiempo de procesamiento
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            # Extraer texto de respuesta
            response_text = response.text
            
            # Estimar tokens (aproximación: 1 token ≈ 4 caracteres)
            tokens_used = len(prompt + response_text) // 4
            
            # Registrar interacción en BD
            self._log_interaction(
                user_id=user_id,
                interaction_type=interaction_type,
                prompt_text=prompt,
                response_text=response_text,
                tokens_used=tokens_used,
                processing_time_ms=processing_time_ms,
                success=True,
                related_entity_type=related_entity_type,
                related_entity_id=related_entity_id
            )
            
            return {
                'success': True,
                'content': response_text,
                'tokens_used': tokens_used,
                'processing_time_ms': processing_time_ms,
                'model': self.model_name
            }
            
        except Exception as e:
            processing_time_ms = int((time.time() - start_time) * 1000)
            
            # Registrar error en BD
            self._log_interaction(
                user_id=user_id,
                interaction_type=interaction_type,
                prompt_text=prompt,
                response_text=None,
                tokens_used=0,
                processing_time_ms=processing_time_ms,
                success=False,
                error_message=str(e),
                related_entity_type=related_entity_type,
                related_entity_id=related_entity_id
            )
            
            return {
                'success': False,
                'error': str(e),
                'processing_time_ms': processing_time_ms
            }
    
    def analyze_text(
        self,
        text: str,
        user_id: Optional[int] = None,
        document_id: Optional[int] = None,
        analysis_type: str = 'comprehensive'
    ) -> Dict[str, Any]:
        """
        Analizar texto académico con Gemini
        
        Args:
            text (str): Texto a analizar
            user_id (int, optional): ID del usuario
            document_id (int, optional): ID del documento
            analysis_type (str): Tipo de análisis
        
        Returns:
            dict: Análisis completo del texto
        """
        prompt = f"""
Analiza el siguiente texto académico y proporciona un análisis detallado en formato JSON.

TEXTO A ANALIZAR:
{text[:5000]}  # Limitar a 5000 caracteres para no exceder límites

INSTRUCCIONES:
Proporciona el análisis en formato JSON con la siguiente estructura:

{{
    "writing_quality_score": 0-100,
    "academic_level": "básico|intermedio|avanzado",
    "main_topics": ["tema1", "tema2", "tema3"],
    "key_concepts": ["concepto1", "concepto2"],
    "technical_terms": ["término1", "término2"],
    "coherence_score": 0-100,
    "cohesion_score": 0-100,
    "sentence_complexity_score": 0-100,
    "readability_score": 0-100,
    "strengths": ["fortaleza1", "fortaleza2"],
    "weaknesses": ["debilidad1", "debilidad2"],
    "recommendations": ["recomendación1", "recomendación2"],
    "summary": "Resumen ejecutivo del análisis en 2-3 oraciones"
}}

IMPORTANTE: Responde ÚNICAMENTE con el JSON, sin texto adicional.
"""
        
        result = self.generate_content(
            prompt=prompt,
            user_id=user_id,
            interaction_type='text_analysis',
            related_entity_type='document',
            related_entity_id=document_id
        )
        
        if result['success']:
            try:
                content = result['content'].strip()
                
                # Intentar parsear directamente
                analysis = json.loads(content)
                result['analysis'] = analysis
                
            except json.JSONDecodeError:
                # Intentar extraer JSON de bloques markdown
                try:
                    if '```json' in content:
                        json_str = content.split('```json')[1].split('```')[0].strip()
                    elif '```' in content:
                        json_str = content.split('```')[1].split('```')[0].strip()
                    else:
                        # Buscar JSON entre llaves
                        import re
                        json_match = re.search(r'\{.*\}', content, re.DOTALL)
                        if json_match:
                            json_str = json_match.group()
                        else:
                            json_str = content
                    
                    analysis = json.loads(json_str)
                    result['analysis'] = analysis
                    
                except Exception as e:
                    result['analysis'] = None
                    result['parse_error'] = f'No se pudo parsear JSON: {str(e)}'
        
        return result
    
    def analyze_sentiment(
        self,
        text: str,
        user_id: Optional[int] = None,
        audio_session_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Analizar sentimiento de texto/transcripción
        
        Args:
            text (str): Texto a analizar
            user_id (int, optional): ID del usuario
            audio_session_id (int, optional): ID de sesión de audio
        
        Returns:
            dict: Análisis de sentimiento
        """
        prompt = f"""
Analiza el sentimiento del siguiente texto y proporciona el resultado en formato JSON.

TEXTO:
{text[:2000]}

Proporciona el análisis en este formato JSON:

{{
    "sentiment": "positive|negative|neutral|mixed",
    "sentiment_score": -100 a +100,
    "emotions_detected": ["emoción1", "emoción2"],
    "confidence": 0-100,
    "keywords": ["palabra_clave1", "palabra_clave2"],
    "summary": "Breve explicación del sentimiento detectado"
}}

IMPORTANTE: Responde ÚNICAMENTE con el JSON, sin texto adicional ni bloques de código markdown.
"""
        
        result = self.generate_content(
            prompt=prompt,
            user_id=user_id,
            interaction_type='sentiment_analysis',
            related_entity_type='audio_session',
            related_entity_id=audio_session_id
        )
        
        if result['success']:
            try:
                content = result['content'].strip()
                
                # Intentar parsear directamente
                sentiment = json.loads(content)
                result['sentiment'] = sentiment
                
            except json.JSONDecodeError:
                # Intentar extraer JSON de bloques markdown
                try:
                    if '```json' in content:
                        json_str = content.split('```json')[1].split('```')[0].strip()
                    elif '```' in content:
                        json_str = content.split('```')[1].split('```')[0].strip()
                    else:
                        # Buscar JSON entre llaves
                        import re
                        json_match = re.search(r'\{.*\}', content, re.DOTALL)
                        if json_match:
                            json_str = json_match.group()
                        else:
                            json_str = content
                    
                    sentiment = json.loads(json_str)
                    result['sentiment'] = sentiment
                    
                except Exception as e:
                    result['sentiment'] = None
                    result['parse_error'] = f'No se pudo parsear JSON: {str(e)}'
        
        return result
    
    def generate_student_profile_summary(
        self,
        profile_data: Dict[str, Any],
        user_id: int
    ) -> Dict[str, Any]:
        """
        Generar resumen de perfil del estudiante con IA
        
        Args:
            profile_data (dict): Datos del perfil del estudiante
            user_id (int): ID del usuario
        
        Returns:
            dict: Resumen generado y consejos personalizados
        """
        prompt = f"""
Genera un resumen de perfil académico personalizado basado en los siguientes datos:

DATOS DEL ESTUDIANTE:
{json.dumps(profile_data, indent=2, ensure_ascii=False)}

Genera DOS textos en español:

1. RESUMEN DEL PERFIL (2-3 párrafos):
Sintetiza las fortalezas, debilidades, estilo de aprendizaje y preparación para tesis.

2. CONSEJOS PERSONALIZADOS (lista de 5-7 recomendaciones):
Proporciona consejos específicos y accionables para mejorar el rendimiento académico.

Responde en formato JSON:
{{
    "profile_summary": "texto del resumen",
    "personalized_advice": "texto con consejos numerados"
}}
"""
        
        result = self.generate_content(
            prompt=prompt,
            user_id=user_id,
            interaction_type='profile_generation',
            related_entity_type='student_profile',
            related_entity_id=user_id
        )
        
        if result['success']:
            try:
                profile_summary = json.loads(result['content'])
                result['profile_summary'] = profile_summary
            except json.JSONDecodeError:
                result['profile_summary'] = None
        
        return result
    
    def generate_report_content(
        self,
        report_data: Dict[str, Any],
        personalization: Dict[str, Any],
        user_id: int
    ) -> Dict[str, Any]:
        """
        Generar contenido para reporte personalizado
        
        Args:
            report_data (dict): Datos para el reporte
            personalization (dict): Perfil de personalización
            user_id (int): ID del usuario
        
        Returns:
            dict: Contenido generado para el reporte
        """
        learning_style = personalization.get('learning_style', 'mixto')
        
        prompt = f"""
Genera contenido para un reporte académico personalizado.

DATOS DEL REPORTE:
{json.dumps(report_data, indent=2, ensure_ascii=False)}

ESTILO DE APRENDIZAJE DEL ESTUDIANTE: {learning_style}

Genera el contenido en formato JSON con:

{{
    "executive_summary": "Resumen ejecutivo (3-4 oraciones)",
    "main_insights": ["insight1", "insight2", "insight3"],
    "detailed_analysis": "Análisis detallado por secciones",
    "key_recommendations": ["recomendación1", "recomendación2", "recomendación3"],
    "areas_of_excellence": ["área1", "área2"],
    "areas_for_improvement": ["área1", "área2"],
    "action_plan": "Plan de acción concreto"
}}

IMPORTANTE: Adapta el lenguaje al estilo de aprendizaje {learning_style}.
"""
        
        result = self.generate_content(
            prompt=prompt,
            user_id=user_id,
            interaction_type='report_generation',
            related_entity_type='report'
        )
        
        if result['success']:
            try:
                report_content = json.loads(result['content'])
                result['report_content'] = report_content
            except json.JSONDecodeError:
                result['report_content'] = None
        
        return result
    
    def _log_interaction(
        self,
        user_id: Optional[int],
        interaction_type: str,
        prompt_text: str,
        response_text: Optional[str],
        tokens_used: int,
        processing_time_ms: int,
        success: bool,
        error_message: Optional[str] = None,
        related_entity_type: Optional[str] = None,
        related_entity_id: Optional[int] = None
    ):
        """
        Registrar interacción con IA en la base de datos
        
        Args:
            Todos los parámetros de la interacción
        """
        try:
            interaction = AIInteraction(
                user_id=user_id,
                interaction_type=interaction_type,
                ai_service='gemini',
                model_used=self.model_name,
                prompt_text=prompt_text[:10000],  # Limitar tamaño
                response_text=response_text[:10000] if response_text else None,
                tokens_used=tokens_used,
                processing_time_ms=processing_time_ms,
                success=success,
                error_message=error_message,
                related_entity_type=related_entity_type,
                related_entity_id=related_entity_id
            )
            
            db.session.add(interaction)
            db.session.commit()
        except Exception as e:
            print(f"Error al registrar interacción: {e}")
            db.session.rollback()


# Instancia global del servicio
gemini_service = GeminiService()