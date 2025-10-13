-- ============================================
-- Base de Datos: Plataforma Integral de Rendimiento Estudiantil
-- Sistema de análisis académico con IA
-- ============================================

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS rendimiento_estudiantil 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE rendimiento_estudiantil;

-- ============================================
-- TABLA: users
-- Almacena información de estudiantes y usuarios del sistema
-- ============================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    student_code VARCHAR(50) UNIQUE,
    career VARCHAR(100),
    current_cycle INT DEFAULT 1,
    enrollment_date DATE,
    profile_image_url VARCHAR(500),
    role ENUM('student', 'admin', 'instructor') DEFAULT 'student',
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    last_login DATETIME,
    failed_login_attempts INT DEFAULT 0,
    lockout_until DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_student_code (student_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLA: documents
-- Almacena documentos académicos subidos por estudiantes
-- ============================================
CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    file_size INT NOT NULL,
    mime_type VARCHAR(100),
    cycle INT NOT NULL,
    course_name VARCHAR(200),
    document_type ENUM('informe', 'trabajo_final', 'proyecto', 'ensayo', 'monografia', 'otro') DEFAULT 'informe',
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
    processing_started_at DATETIME,
    processing_completed_at DATETIME,
    error_message TEXT,
    meta_info JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_cycle (cycle),
    INDEX idx_upload_date (upload_date),
    INDEX idx_processing_status (processing_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLA: text_analysis
-- Resultados del análisis de texto de documentos (Módulo 1)
-- ============================================
CREATE TABLE text_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    document_id INT NOT NULL,
    user_id INT NOT NULL,
    
    -- Métricas de vocabulario
    total_words INT,
    unique_words INT,
    vocabulary_richness DECIMAL(5,2),
    technical_terms_count INT,
    technical_terms JSON,
    
    -- Métricas de complejidad
    avg_sentence_length DECIMAL(6,2),
    avg_word_length DECIMAL(5,2),
    sentence_complexity_score DECIMAL(5,2),
    readability_score DECIMAL(5,2),
    
    -- Análisis estructural
    paragraph_count INT,
    sentence_count INT,
    coherence_score DECIMAL(5,2),
    cohesion_score DECIMAL(5,2),
    
    -- Análisis semántico con IA
    main_topics JSON,
    key_concepts JSON,
    writing_quality_score DECIMAL(5,2),
    academic_level_assessment VARCHAR(50),
    
    -- Comparación con documentos previos
    improvement_percentage DECIMAL(5,2),
    comparison_notes TEXT,
    
    -- Tiempo de desarrollo (si está disponible)
    development_time_minutes INT,
    
    -- Análisis completo generado por IA
    ai_analysis_summary TEXT,
    ai_recommendations TEXT,
    
    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_document_id (document_id),
    INDEX idx_user_id (user_id),
    INDEX idx_analysis_date (analysis_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLA: video_sessions
-- Sesiones de análisis de video en tiempo real (Módulo 2)
-- ============================================
CREATE TABLE video_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    session_name VARCHAR(255),
    session_type ENUM('clase', 'exposicion', 'estudio', 'tutorial', 'otro') DEFAULT 'estudio',
    course_name VARCHAR(200),
    
    -- Información de la sesión
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    duration_seconds INT,
    
    -- Archivos de video
    video_file_path VARCHAR(500),
    video_file_size INT,
    
    -- Estado de procesamiento
    processing_status ENUM('recording', 'processing', 'completed', 'failed') DEFAULT 'recording',
    processing_started_at DATETIME,
    processing_completed_at DATETIME,
    error_message TEXT,
    
    -- Resumen de métricas
    total_frames_analyzed INT DEFAULT 0,
    faces_detected_count INT DEFAULT 0,
    avg_attention_score DECIMAL(5,2),
    dominant_emotion VARCHAR(50),
    
    -- Metadata
    metadata JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_start_time (start_time),
    INDEX idx_processing_status (processing_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLA: emotion_data
-- Datos de emociones detectadas frame por frame
-- ============================================
CREATE TABLE emotion_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    user_id INT NOT NULL,
    
    -- Timestamp del frame
    timestamp_seconds DECIMAL(10,3) NOT NULL,
    frame_number INT NOT NULL,
    
    -- Detección facial
    face_detected BOOLEAN DEFAULT FALSE,
    face_count INT DEFAULT 0,
    face_confidence DECIMAL(5,2),
    
    -- Emociones básicas (7 emociones de DeepFace)
    emotion_angry DECIMAL(5,2) DEFAULT 0,
    emotion_disgust DECIMAL(5,2) DEFAULT 0,
    emotion_fear DECIMAL(5,2) DEFAULT 0,
    emotion_happy DECIMAL(5,2) DEFAULT 0,
    emotion_sad DECIMAL(5,2) DEFAULT 0,
    emotion_surprise DECIMAL(5,2) DEFAULT 0,
    emotion_neutral DECIMAL(5,2) DEFAULT 0,
    
    -- Emoción dominante
    dominant_emotion VARCHAR(50),
    dominant_emotion_confidence DECIMAL(5,2),
    
    -- Emociones contextuales (16 emociones mapeadas)
    contextual_emotion VARCHAR(50),
    contextual_emotion_confidence DECIMAL(5,2),
    
    -- Atributos adicionales
    age INT,
    gender VARCHAR(20),
    
    -- Datos del rostro
    face_bbox JSON,
    face_landmarks JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (session_id) REFERENCES video_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_session_id (session_id),
    INDEX idx_timestamp (timestamp_seconds),
    INDEX idx_frame_number (frame_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLA: attention_metrics
-- Métricas de atención calculadas a partir de emociones
-- ============================================
CREATE TABLE attention_metrics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    user_id INT NOT NULL,
    
    -- Intervalo de tiempo
    time_interval_start DECIMAL(10,3) NOT NULL,
    time_interval_end DECIMAL(10,3) NOT NULL,
    interval_duration_seconds INT,
    
    -- Score de atención (0-100)
    attention_score DECIMAL(5,2) NOT NULL,
    engagement_level ENUM('muy_bajo', 'bajo', 'medio', 'alto', 'muy_alto'),
    
    -- Emociones predominantes en el intervalo
    predominant_emotions JSON,
    
    -- Indicadores de comprensión
    comprehension_indicators JSON,
    confusion_detected BOOLEAN DEFAULT FALSE,
    boredom_detected BOOLEAN DEFAULT FALSE,
    
    -- Análisis
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (session_id) REFERENCES video_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_session_id (session_id),
    INDEX idx_time_interval (time_interval_start, time_interval_end)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLA: audio_sessions
-- Sesiones de audio y transcripción (Módulo 2)
-- ============================================
CREATE TABLE audio_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT,
    user_id INT NOT NULL,
    
    -- Información del audio
    audio_file_path VARCHAR(500),
    audio_file_size INT,
    audio_duration_seconds INT,
    audio_format VARCHAR(20),
    
    -- Estado de procesamiento
    processing_status ENUM('pending', 'processing', 'completed', 'failed') DEFAULT 'pending',
    processing_started_at DATETIME,
    processing_completed_at DATETIME,
    error_message TEXT,
    
    -- Transcripción
    transcription_text LONGTEXT,
    transcription_confidence DECIMAL(5,2),
    transcription_accuracy_percentage DECIMAL(5,2),
    language_detected VARCHAR(10),
    
    -- Metadata
    metadata JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (session_id) REFERENCES video_sessions(id) ON DELETE SET NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_session_id (session_id),
    INDEX idx_user_id (user_id),
    INDEX idx_processing_status (processing_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLA: audio_transcriptions
-- Segmentos de transcripción del audio
-- ============================================
CREATE TABLE audio_transcriptions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    audio_session_id INT NOT NULL,
    user_id INT NOT NULL,
    
    -- Segmento de tiempo
    start_time DECIMAL(10,3) NOT NULL,
    end_time DECIMAL(10,3) NOT NULL,
    duration_seconds DECIMAL(6,3),
    
    -- Transcripción
    text TEXT NOT NULL,
    confidence DECIMAL(5,2),
    
    -- Análisis de sentimiento
    sentiment VARCHAR(50),
    sentiment_score DECIMAL(5,2),
    
    -- Palabras clave
    keywords JSON,
    
    -- Análisis con Gemini
    ai_analysis TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (audio_session_id) REFERENCES audio_sessions(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_audio_session_id (audio_session_id),
    INDEX idx_time_range (start_time, end_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLA: student_profiles
-- Perfil integral del estudiante (Módulo 3)
-- ============================================
CREATE TABLE student_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    
    -- Análisis académico
    total_documents_analyzed INT DEFAULT 0,
    total_sessions_completed INT DEFAULT 0,
    avg_writing_quality DECIMAL(5,2),
    avg_vocabulary_richness DECIMAL(5,2),
    writing_improvement_trend VARCHAR(50),
    
    -- Fortalezas identificadas
    academic_strengths JSON,
    writing_strengths JSON,
    technical_strengths JSON,
    
    -- Debilidades identificadas
    academic_weaknesses JSON,
    writing_weaknesses JSON,
    areas_for_improvement JSON,
    
    -- Estilo de aprendizaje
    learning_style VARCHAR(100),
    learning_preferences JSON,
    optimal_session_duration INT,
    attention_pattern VARCHAR(100),
    
    -- Preparación para tesis
    thesis_readiness_score DECIMAL(5,2),
    thesis_readiness_level ENUM('bajo', 'medio', 'alto', 'excelente'),
    estimated_preparation_months INT,
    
    -- Patrones de comportamiento
    most_productive_time VARCHAR(50),
    avg_attention_span_minutes INT,
    emotion_patterns JSON,
    
    -- Recomendaciones personalizadas
    study_recommendations JSON,
    resource_recommendations JSON,
    
    -- Resumen generado por IA
    ai_profile_summary TEXT,
    ai_personalized_advice TEXT,
    
    last_updated DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_thesis_readiness (thesis_readiness_score)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLA: reports
-- Reportes generados para estudiantes (Módulo 4)
-- ============================================
CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    
    -- Información del reporte
    title VARCHAR(255) NOT NULL,
    report_type ENUM('semestral', 'curso', 'sesion', 'progreso', 'integral', 'personalizado') NOT NULL,
    description TEXT,
    
    -- Período del reporte
    period_start DATE,
    period_end DATE,
    cycle INT,
    course_name VARCHAR(200),
    
    -- Archivos generados
    file_path VARCHAR(500),
    file_name VARCHAR(255),
    file_format VARCHAR(20),
    file_size INT,
    
    -- Estado de generación
    generation_status ENUM('pending', 'generating', 'completed', 'failed') DEFAULT 'pending',
    generation_started_at DATETIME,
    generation_completed_at DATETIME,
    error_message TEXT,
    
    -- Contenido del reporte
    report_data JSON,
    charts_data JSON,
    
    -- Personalización aplicada
    personalization_profile JSON,
    content_style VARCHAR(100),
    
    -- Metadata
    metadata JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_report_type (report_type),
    INDEX idx_generation_status (generation_status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLA: generated_templates
-- Plantillas personalizadas generadas (PPT, DOCX)
-- ============================================
CREATE TABLE generated_templates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    report_id INT,
    
    -- Información de la plantilla
    title VARCHAR(255) NOT NULL,
    template_type ENUM('ppt', 'docx', 'pdf', 'otro') NOT NULL,
    topic VARCHAR(255),
    description TEXT,
    
    -- Archivo generado
    file_path VARCHAR(500) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size INT,
    
    -- Personalización
    personalization_applied JSON,
    visual_style VARCHAR(100),
    content_focus JSON,
    
    -- IA utilizada
    ai_model_used VARCHAR(100),
    ai_prompt_used TEXT,
    
    -- Estado
    generation_status ENUM('pending', 'generating', 'completed', 'failed') DEFAULT 'pending',
    generation_time_seconds INT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (report_id) REFERENCES reports(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_report_id (report_id),
    INDEX idx_template_type (template_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLA: ai_interactions
-- Registro de todas las interacciones con APIs de IA
-- ============================================
CREATE TABLE ai_interactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    
    -- Información de la interacción
    interaction_type VARCHAR(100) NOT NULL,
    ai_service VARCHAR(50) NOT NULL,
    model_used VARCHAR(100),
    
    -- Input/Output
    prompt_text MEDIUMTEXT,
    response_text MEDIUMTEXT,
    
    -- Métricas
    tokens_used INT,
    processing_time_ms INT,
    cost_estimate DECIMAL(10,6),
    
    -- Contexto
    related_entity_type VARCHAR(50),
    related_entity_id INT,
    
    -- Resultado
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_interaction_type (interaction_type),
    INDEX idx_ai_service (ai_service),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- TABLA: system_logs
-- Logs del sistema para debugging y auditoría
-- ============================================
CREATE TABLE system_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    
    -- Información del log
    log_level ENUM('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL') NOT NULL,
    module VARCHAR(100),
    function_name VARCHAR(100),
    
    -- Mensaje
    message TEXT NOT NULL,
    stack_trace TEXT,
    
    -- Contexto
    request_method VARCHAR(10),
    request_url VARCHAR(500),
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    
    -- Metadata adicional
    metadata JSON,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_log_level (log_level),
    INDEX idx_module (module),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================
-- VISTAS ÚTILES
-- ============================================

-- Vista: Resumen de progreso académico por estudiante
CREATE VIEW v_student_progress_summary AS
SELECT 
    u.id AS user_id,
    u.username,
    u.email,
    u.current_cycle,
    COUNT(DISTINCT d.id) AS total_documents,
    COUNT(DISTINCT vs.id) AS total_video_sessions,
    AVG(ta.writing_quality_score) AS avg_writing_quality,
    AVG(ta.vocabulary_richness) AS avg_vocabulary_richness,
    AVG(am.attention_score) AS avg_attention_score,
    sp.thesis_readiness_score,
    sp.learning_style
FROM users u
LEFT JOIN documents d ON u.id = d.user_id
LEFT JOIN text_analysis ta ON d.id = ta.document_id
LEFT JOIN video_sessions vs ON u.id = vs.user_id
LEFT JOIN attention_metrics am ON vs.id = am.session_id
LEFT JOIN student_profiles sp ON u.id = sp.user_id
WHERE u.role = 'student'
GROUP BY u.id;

-- Vista: Análisis de emociones por sesión
CREATE VIEW v_emotion_analysis_by_session AS
SELECT 
    vs.id AS session_id,
    vs.user_id,
    vs.session_name,
    vs.duration_seconds,
    COUNT(ed.id) AS total_frames,
    AVG(ed.emotion_happy) AS avg_happy,
    AVG(ed.emotion_neutral) AS avg_neutral,
    AVG(ed.emotion_sad) AS avg_sad,
    AVG(ed.emotion_angry) AS avg_angry,
    AVG(ed.emotion_surprise) AS avg_surprise,
    AVG(ed.emotion_fear) AS avg_fear,
    AVG(ed.emotion_disgust) AS avg_disgust,
    AVG(am.attention_score) AS avg_attention_score
FROM video_sessions vs
LEFT JOIN emotion_data ed ON vs.id = ed.session_id
LEFT JOIN attention_metrics am ON vs.id = am.session_id
GROUP BY vs.id;