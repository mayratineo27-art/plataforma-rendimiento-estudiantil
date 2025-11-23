-- Migración: Mejoras para Gestión de Cursos, Sílabos y Líneas de Tiempo
-- Fecha: 2025-11-23

USE plataforma_estudiantil;

-- 1. ACTUALIZAR TABLA DE CURSOS (academic_courses)
ALTER TABLE academic_courses 
ADD COLUMN IF NOT EXISTS code VARCHAR(50) COMMENT 'Código del curso',
ADD COLUMN IF NOT EXISTS category VARCHAR(50) DEFAULT 'general' COMMENT 'Categoría del curso',
ADD COLUMN IF NOT EXISTS icon VARCHAR(50) DEFAULT 'BookOpen' COMMENT 'Icono del curso',
MODIFY COLUMN color VARCHAR(20) DEFAULT 'blue' COMMENT 'Color del curso';

-- 2. CREAR TABLA DE ANÁLISIS DE SÍLABOS (syllabus_analysis)
CREATE TABLE IF NOT EXISTS syllabus_analysis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    file_path VARCHAR(500) COMMENT 'Ruta del archivo PDF',
    file_name VARCHAR(255) COMMENT 'Nombre del archivo',
    course_info_json TEXT COMMENT 'Información del curso en JSON',
    topics_json TEXT COMMENT 'Temas del curso en JSON',
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES academic_courses(id) ON DELETE CASCADE,
    
    INDEX idx_user_syllabus (user_id),
    INDEX idx_course_syllabus (course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Análisis de sílabos con IA';

-- 3. ACTUALIZAR TABLA DE LÍNEAS DE TIEMPO (timelines)
ALTER TABLE timelines
ADD COLUMN IF NOT EXISTS end_date DATETIME COMMENT 'Fecha límite de la línea de tiempo',
MODIFY COLUMN steps_json TEXT NULL COMMENT 'Pasos en JSON (para compatibilidad)';

-- 4. CREAR TABLA DE PASOS DE LÍNEAS DE TIEMPO (timeline_steps)
CREATE TABLE IF NOT EXISTS timeline_steps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timeline_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    `order` INT NOT NULL COMMENT 'Orden del paso',
    completed BOOLEAN DEFAULT FALSE,
    completed_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (timeline_id) REFERENCES timelines(id) ON DELETE CASCADE,
    
    INDEX idx_timeline_steps (timeline_id),
    INDEX idx_step_order (timeline_id, `order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Pasos individuales de líneas de tiempo';

-- 5. MIGRAR DATOS EXISTENTES (OPCIONAL)
-- Si ya tienes cursos, puedes actualizarlos con valores por defecto
UPDATE academic_courses 
SET category = 'general' WHERE category IS NULL;

UPDATE academic_courses 
SET icon = 'BookOpen' WHERE icon IS NULL;

UPDATE academic_courses 
SET color = 'blue' WHERE color IS NULL OR color = '#3B82F6';

-- Mensaje de confirmación
SELECT 'Migración completada exitosamente' as status;
SELECT COUNT(*) as total_cursos FROM academic_courses;
SELECT COUNT(*) as total_syllabus FROM syllabus_analysis;
SELECT COUNT(*) as total_timelines FROM timelines;
SELECT COUNT(*) as total_steps FROM timeline_steps;
