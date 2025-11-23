"""
app/services/report_generation/data_visualizer.py
Prepara datos para visualizaciones (Chart.js, gráficos en PPT)
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from app.models.student_profile import StudentProfile
from app.models.video_session import VideoSession
from app.models.attention_metrics import AttentionMetrics
from app.models.document import Document
from app.models.text_analysis import TextAnalysis
from app.utils.logger import logger


class DataVisualizer:
    """
    Prepara datos del estudiante para visualizaciones
    Compatible con Chart.js y gráficos de PPT
    """
    
    def __init__(self):
        self.logger = logger
    
    # =====================================================
    # DATOS PARA GRÁFICOS DE PERFIL
    # =====================================================
    
    def get_thesis_readiness_chart_data(self, profile: StudentProfile) -> Dict:
        """
        Datos para gráfico de radar de preparación para tesis
        
        Returns:
            Dict compatible con Chart.js radar chart
        """
        try:
            # Factores del thesis readiness
            factors = {
                'Documentos Analizados': min((profile.total_documents_analyzed / 10) * 100, 100),
                'Calidad de Escritura': float(profile.avg_writing_quality or 0),
                'Vocabulario Técnico': float(profile.avg_vocabulary_richness or 0),
                'Capacidad de Atención': min((profile.avg_attention_span_minutes or 0) / 60 * 100, 100),
                'Consistencia': 70 if profile.writing_improvement_trend == 'improving' else 50
            }
            
            return {
                'type': 'radar',
                'labels': list(factors.keys()),
                'datasets': [{
                    'label': 'Preparación para Tesis',
                    'data': list(factors.values()),
                    'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                    'borderColor': 'rgba(54, 162, 235, 1)',
                    'pointBackgroundColor': 'rgba(54, 162, 235, 1)',
                    'pointBorderColor': '#fff'
                }],
                'options': {
                    'scale': {
                        'ticks': {'beginAtZero': True, 'max': 100}
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error en thesis readiness chart: {str(e)}")
            return self._empty_radar_chart()
    
    def get_progress_timeline_data(self, user_id: int) -> Dict:
        """
        Línea de tiempo de progreso del estudiante
        
        Returns:
            Dict compatible con Chart.js line chart
        """
        try:
            # Obtener análisis de texto ordenados por fecha
            analyses = TextAnalysis.query.filter_by(
                user_id=user_id
            ).order_by(TextAnalysis.analysis_date).all()
            
            if not analyses:
                return self._empty_line_chart()
            
            dates = []
            writing_scores = []
            vocab_scores = []
            
            for analysis in analyses:
                dates.append(analysis.analysis_date.strftime('%Y-%m-%d'))
                writing_scores.append(float(analysis.writing_quality_score or 0))
                vocab_scores.append(float(analysis.vocabulary_richness or 0))
            
            return {
                'type': 'line',
                'labels': dates,
                'datasets': [
                    {
                        'label': 'Calidad de Escritura',
                        'data': writing_scores,
                        'borderColor': 'rgba(75, 192, 192, 1)',
                        'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                        'tension': 0.4
                    },
                    {
                        'label': 'Riqueza de Vocabulario',
                        'data': vocab_scores,
                        'borderColor': 'rgba(153, 102, 255, 1)',
                        'backgroundColor': 'rgba(153, 102, 255, 0.2)',
                        'tension': 0.4
                    }
                ],
                'options': {
                    'scales': {
                        'y': {'beginAtZero': True, 'max': 100}
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error en progress timeline: {str(e)}")
            return self._empty_line_chart()
    
    def get_attention_distribution_data(self, user_id: int) -> Dict:
        """
        Distribución de niveles de atención
        
        Returns:
            Dict compatible con Chart.js doughnut chart
        """
        try:
            # Obtener métricas de atención
            metrics = AttentionMetrics.query.filter_by(user_id=user_id).all()
            
            if not metrics:
                return self._empty_doughnut_chart()
            
            # Contar niveles
            levels = {
                'Muy Alto': 0,
                'Alto': 0,
                'Medio': 0,
                'Bajo': 0,
                'Muy Bajo': 0
            }
            
            for metric in metrics:
                level = metric.engagement_level
                if level == 'muy_alto':
                    levels['Muy Alto'] += 1
                elif level == 'alto':
                    levels['Alto'] += 1
                elif level == 'medio':
                    levels['Medio'] += 1
                elif level == 'bajo':
                    levels['Bajo'] += 1
                elif level == 'muy_bajo':
                    levels['Muy Bajo'] += 1
            
            return {
                'type': 'doughnut',
                'labels': list(levels.keys()),
                'datasets': [{
                    'label': 'Niveles de Atención',
                    'data': list(levels.values()),
                    'backgroundColor': [
                        'rgba(75, 192, 192, 0.8)',   # Muy Alto - verde
                        'rgba(54, 162, 235, 0.8)',   # Alto - azul
                        'rgba(255, 206, 86, 0.8)',   # Medio - amarillo
                        'rgba(255, 159, 64, 0.8)',   # Bajo - naranja
                        'rgba(255, 99, 132, 0.8)'    # Muy Bajo - rojo
                    ],
                    'borderColor': 'white',
                    'borderWidth': 2
                }]
            }
        except Exception as e:
            self.logger.error(f"Error en attention distribution: {str(e)}")
            return self._empty_doughnut_chart()
    
    def get_strengths_weaknesses_comparison(self, profile: StudentProfile) -> Dict:
        """
        Comparación de fortalezas vs debilidades
        
        Returns:
            Dict compatible con Chart.js bar chart
        """
        try:
            # Contar fortalezas
            strengths_count = 0
            if profile.academic_strengths:
                strengths_count += len(profile.academic_strengths)
            if profile.writing_strengths:
                strengths_count += len(profile.writing_strengths)
            if profile.technical_strengths:
                strengths_count += len(profile.technical_strengths)
            
            # Contar debilidades
            weaknesses_count = 0
            if profile.academic_weaknesses:
                weaknesses_count += len(profile.academic_weaknesses)
            if profile.writing_weaknesses:
                weaknesses_count += len(profile.writing_weaknesses)
            if profile.areas_for_improvement:
                weaknesses_count += len(profile.areas_for_improvement)
            
            return {
                'type': 'bar',
                'labels': ['Fortalezas', 'Áreas de Mejora'],
                'datasets': [{
                    'label': 'Cantidad',
                    'data': [strengths_count, weaknesses_count],
                    'backgroundColor': [
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(255, 159, 64, 0.8)'
                    ],
                    'borderColor': [
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    'borderWidth': 2
                }],
                'options': {
                    'scales': {
                        'y': {'beginAtZero': True}
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error en strengths/weaknesses: {str(e)}")
            return self._empty_bar_chart()
    
    def get_session_activity_data(self, user_id: int, days: int = 30) -> Dict:
        """
        Actividad de sesiones en los últimos N días
        
        Returns:
            Dict compatible con Chart.js line chart
        """
        try:
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Obtener sesiones en el rango
            sessions = VideoSession.query.filter(
                VideoSession.user_id == user_id,
                VideoSession.start_time >= start_date,
                VideoSession.start_time <= end_date
            ).order_by(VideoSession.start_time).all()
            
            if not sessions:
                return self._empty_line_chart()
            
            # Agrupar por día
            daily_counts = {}
            daily_durations = {}
            
            for session in sessions:
                date_key = session.start_time.strftime('%Y-%m-%d')
                daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
                duration_hours = (session.duration_seconds or 0) / 3600
                daily_durations[date_key] = daily_durations.get(date_key, 0) + duration_hours
            
            # Ordenar fechas
            sorted_dates = sorted(daily_counts.keys())
            
            return {
                'type': 'line',
                'labels': sorted_dates,
                'datasets': [
                    {
                        'label': 'Sesiones por Día',
                        'data': [daily_counts[d] for d in sorted_dates],
                        'borderColor': 'rgba(54, 162, 235, 1)',
                        'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                        'yAxisID': 'y',
                        'tension': 0.4
                    },
                    {
                        'label': 'Horas de Estudio',
                        'data': [daily_durations[d] for d in sorted_dates],
                        'borderColor': 'rgba(255, 99, 132, 1)',
                        'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                        'yAxisID': 'y1',
                        'tension': 0.4
                    }
                ],
                'options': {
                    'scales': {
                        'y': {'type': 'linear', 'position': 'left'},
                        'y1': {'type': 'linear', 'position': 'right', 'grid': {'drawOnChartArea': False}}
                    }
                }
            }
        except Exception as e:
            self.logger.error(f"Error en session activity: {str(e)}")
            return self._empty_line_chart()
    
    # =====================================================
    # DATOS SIMPLIFICADOS PARA PPT
    # =====================================================
    
    def get_summary_stats(self, profile: StudentProfile, user_id: int) -> Dict:
        """
        Estadísticas resumidas para slides
        
        Returns:
            Dict con stats clave
        """
        try:
            return {
                'total_documents': profile.total_documents_analyzed,
                'total_sessions': profile.total_sessions_completed,
                'thesis_score': float(profile.thesis_readiness_score or 0),
                'thesis_level': profile.thesis_readiness_level or 'bajo',
                'writing_quality': float(profile.avg_writing_quality or 0),
                'vocabulary_score': float(profile.avg_vocabulary_richness or 0),
                'attention_span': profile.avg_attention_span_minutes or 0,
                'learning_style': profile.learning_style or 'No determinado',
                'improvement_trend': profile.writing_improvement_trend or 'stable'
            }
        except Exception as e:
            self.logger.error(f"Error en summary stats: {str(e)}")
            return {}
    
    # =====================================================
    # CHARTS VACÍOS (FALLBACK)
    # =====================================================
    
    def _empty_radar_chart(self) -> Dict:
        """Chart vacío tipo radar"""
        return {
            'type': 'radar',
            'labels': ['Sin datos'],
            'datasets': [{
                'label': 'Sin información',
                'data': [0],
                'backgroundColor': 'rgba(200, 200, 200, 0.2)'
            }]
        }
    
    def _empty_line_chart(self) -> Dict:
        """Chart vacío tipo línea"""
        return {
            'type': 'line',
            'labels': ['Sin datos'],
            'datasets': [{
                'label': 'Sin información',
                'data': [0],
                'borderColor': 'rgba(200, 200, 200, 1)'
            }]
        }
    
    def _empty_doughnut_chart(self) -> Dict:
        """Chart vacío tipo dona"""
        return {
            'type': 'doughnut',
            'labels': ['Sin datos'],
            'datasets': [{
                'label': 'Sin información',
                'data': [1],
                'backgroundColor': ['rgba(200, 200, 200, 0.5)']
            }]
        }
    
    def _empty_bar_chart(self) -> Dict:
        """Chart vacío tipo barra"""
        return {
            'type': 'bar',
            'labels': ['Sin datos'],
            'datasets': [{
                'label': 'Sin información',
                'data': [0],
                'backgroundColor': 'rgba(200, 200, 200, 0.5)'
            }]
        }


# Instancia única
data_visualizer = DataVisualizer()