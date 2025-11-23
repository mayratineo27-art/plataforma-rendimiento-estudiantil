from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime

class PDFGenerator:
    """
    Servicio para generar PDFs profesionales de análisis de syllabus
    """
    
    @staticmethod
    def generate_syllabus_analysis_pdf(analysis_data, course_name="Análisis de Syllabus"):
        """
        Genera un PDF con el análisis completo del syllabus
        
        Args:
            analysis_data (dict): Datos del análisis generado por IA
            course_name (str): Nombre del curso
            
        Returns:
            BytesIO: Buffer con el contenido del PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        
        # Estilos
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        # Estilo para subtítulos
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#3730a3'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Estilo para secciones
        section_style = ParagraphStyle(
            'CustomSection',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#4338ca'),
            spaceAfter=10,
            spaceBefore=10
        )
        
        # Construir contenido
        story = []
        
        # Portada
        story.append(Spacer(1, 1 * inch))
        story.append(Paragraph(course_name, title_style))
        story.append(Paragraph("Análisis Integral de Syllabus", subtitle_style))
        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph(f"Generado: {datetime.now().strftime('%d de %B de %Y')}", styles['Normal']))
        story.append(Paragraph("Plataforma de Rendimiento Estudiantil", styles['Normal']))
        story.append(PageBreak())
        
        # Información del Curso
        if 'course_info' in analysis_data:
            story.append(Paragraph("📚 Información del Curso", subtitle_style))
            course_info = analysis_data['course_info']
            
            if 'name' in course_info and course_info['name']:
                story.append(Paragraph(f"<b>Nombre:</b> {course_info['name']}", styles['Normal']))
                story.append(Spacer(1, 6))
            
            if 'description' in course_info and course_info['description']:
                story.append(Paragraph(f"<b>Descripción:</b>", styles['Normal']))
                story.append(Paragraph(course_info['description'], styles['BodyText']))
                story.append(Spacer(1, 12))
            
            if 'credits' in course_info and course_info['credits']:
                story.append(Paragraph(f"<b>Créditos:</b> {course_info['credits']}", styles['Normal']))
                story.append(Spacer(1, 6))
            
            if 'prerequisites' in course_info and course_info['prerequisites']:
                story.append(Paragraph(f"<b>Prerequisitos:</b>", styles['Normal']))
                prereq_text = ", ".join(course_info['prerequisites'])
                story.append(Paragraph(prereq_text, styles['BodyText']))
                story.append(Spacer(1, 12))
            
            story.append(Spacer(1, 20))
        
        # Horas de Estudio
        if 'estimated_weekly_hours' in analysis_data:
            story.append(Paragraph(f"<b>⏰ Horas semanales estimadas:</b> {analysis_data['estimated_weekly_hours']}", styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Métodos de Evaluación
        if 'assessment_methods' in analysis_data and analysis_data['assessment_methods']:
            story.append(Paragraph("📊 Métodos de Evaluación", section_style))
            for method in analysis_data['assessment_methods']:
                story.append(Paragraph(f"• {method}", styles['Normal']))
                story.append(Spacer(1, 4))
            story.append(Spacer(1, 12))
        
        story.append(PageBreak())
        
        # Temas del Curso
        if 'topics' in analysis_data and analysis_data['topics']:
            story.append(Paragraph("📖 Temario del Curso", subtitle_style))
            
            for idx, topic in enumerate(analysis_data['topics'], 1):
                # Título del tema
                topic_title = f"{idx}. {topic.get('name', 'Tema sin nombre')}"
                story.append(Paragraph(topic_title, section_style))
                
                # Semana y dificultad
                info_parts = []
                if 'week' in topic and topic['week']:
                    info_parts.append(f"<b>Semana:</b> {topic['week']}")
                if 'difficulty' in topic and topic['difficulty']:
                    diff_colors = {
                        'Baja': '#10b981',
                        'Media': '#f59e0b',
                        'Alta': '#ef4444'
                    }
                    diff_color = diff_colors.get(topic['difficulty'], '#6b7280')
                    info_parts.append(f"<b>Dificultad:</b> <font color='{diff_color}'>{topic['difficulty']}</font>")
                
                if info_parts:
                    story.append(Paragraph(" | ".join(info_parts), styles['Normal']))
                    story.append(Spacer(1, 6))
                
                # Descripción
                if 'description' in topic and topic['description']:
                    story.append(Paragraph(topic['description'], styles['BodyText']))
                    story.append(Spacer(1, 8))
                
                # Subtemas
                if 'subtopics' in topic and topic['subtopics']:
                    story.append(Paragraph("<b>Subtemas:</b>", styles['Normal']))
                    for subtopic in topic['subtopics']:
                        story.append(Paragraph(f"  • {subtopic}", styles['Normal']))
                        story.append(Spacer(1, 3))
                
                story.append(Spacer(1, 16))
        
        story.append(PageBreak())
        
        # Ruta de Aprendizaje
        if 'learning_path' in analysis_data:
            story.append(Paragraph("🎯 Ruta de Aprendizaje Sugerida", subtitle_style))
            learning_path = analysis_data['learning_path']
            
            if 'foundational_topics' in learning_path and learning_path['foundational_topics']:
                story.append(Paragraph("📚 <b>Temas Fundacionales</b>", section_style))
                for topic in learning_path['foundational_topics']:
                    story.append(Paragraph(f"• {topic}", styles['Normal']))
                    story.append(Spacer(1, 4))
                story.append(Spacer(1, 12))
            
            if 'intermediate_topics' in learning_path and learning_path['intermediate_topics']:
                story.append(Paragraph("📖 <b>Temas Intermedios</b>", section_style))
                for topic in learning_path['intermediate_topics']:
                    story.append(Paragraph(f"• {topic}", styles['Normal']))
                    story.append(Spacer(1, 4))
                story.append(Spacer(1, 12))
            
            if 'advanced_topics' in learning_path and learning_path['advanced_topics']:
                story.append(Paragraph("🎓 <b>Temas Avanzados</b>", section_style))
                for topic in learning_path['advanced_topics']:
                    story.append(Paragraph(f"• {topic}", styles['Normal']))
                    story.append(Spacer(1, 4))
                story.append(Spacer(1, 12))
        
        # Mapa de Dependencias
        if 'dependencies_map' in analysis_data and analysis_data['dependencies_map']:
            story.append(PageBreak())
            story.append(Paragraph("🔗 Mapa de Dependencias", subtitle_style))
            
            for dep in analysis_data['dependencies_map']:
                story.append(Paragraph(f"<b>{dep.get('topic', 'Tema')}:</b>", section_style))
                if 'requires' in dep:
                    story.append(Paragraph(f"Requiere: {', '.join(dep['requires'])}", styles['Normal']))
                if 'reason' in dep:
                    story.append(Paragraph(f"<i>{dep['reason']}</i>", styles['Italic']))
                story.append(Spacer(1, 12))
        
        # Recomendaciones
        if 'study_recommendations' in analysis_data and analysis_data['study_recommendations']:
            story.append(PageBreak())
            story.append(Paragraph("💡 Recomendaciones de Estudio", subtitle_style))
            
            for idx, rec in enumerate(analysis_data['study_recommendations'], 1):
                story.append(Paragraph(f"{idx}. {rec}", styles['BodyText']))
                story.append(Spacer(1, 8))
        
        # Fechas Clave
        if 'key_dates' in analysis_data and analysis_data['key_dates']:
            story.append(PageBreak())
            story.append(Paragraph("📅 Fechas Importantes", subtitle_style))
            
            # Crear tabla de fechas
            date_data = [['Fecha', 'Evento', 'Descripción']]
            for date_entry in analysis_data['key_dates']:
                date_data.append([
                    date_entry.get('date', ''),
                    date_entry.get('event', ''),
                    date_entry.get('description', '')
                ])
            
            date_table = Table(date_data, colWidths=[1.5*inch, 2*inch, 3*inch])
            date_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3730a3')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(date_table)
        
        # Construir PDF
        doc.build(story)
        
        # Obtener el valor del buffer
        pdf = buffer.getvalue()
        buffer.close()
        
        return pdf
