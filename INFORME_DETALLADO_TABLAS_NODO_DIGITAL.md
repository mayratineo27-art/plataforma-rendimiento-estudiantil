# 📊 INFORME DETALLADO DE TABLAS - NODO DIGITAL

**Plataforma de Rendimiento Estudiantil**  
**Fecha de generación:** 11 de Diciembre de 2025  
**Base de datos:** `rendimiento_estudiantil`  
**Host:** localhost:3306  
**Total de tablas:** 23

---

## 🗄️ UBICACIÓN DE LA BASE DE DATOS

### Información de Conexión

| Parámetro | Valor |
|-----------|-------|
| **Motor** | MySQL 8.0+ |
| **Host** | localhost |
| **Puerto** | 3306 |
| **Base de datos** | `rendimiento_estudiantil` |
| **Usuario** | root |
| **Contraseña** | ADMIN |

### 📁 Archivo de Configuración

- **Ubicación**: `backend/.env`
- **Variables**:
  ```env
  DB_HOST=localhost
  DB_PORT=3306
  DB_NAME=rendimiento_estudiantil
  DB_USER=root
  DB_PASSWORD=ADMIN
  ```

### 🔧 Herramientas para Acceder

1. **phpMyAdmin** (si tienes XAMPP/WAMP)
   - URL: http://localhost/phpmyadmin
   - Usuario: root
   - Contraseña: ADMIN

2. **MySQL Workbench**
   - Host: localhost
   - Puerto: 3306
   - Usuario: root

3. **Línea de Comandos**
   ```bash
   mysql -u root -p rendimiento_estudiantil
   # Contraseña: ADMIN
   ```

4. **DBeaver** (Recomendado)
   - Herramienta universal de base de datos
   - Soporta visualización y edición gráfica

---

## 📋 TABLAS DEL NODO DIGITAL

### Resumen de Módulos

| Módulo | Tablas | Estado |
|--------|--------|--------|
| **Usuarios y Perfiles** | 2 | ✅ Activo |
| **Evaluación Académica** | 6 | ✅ Activo |
| **Video y Audio (IA)** | 5 | ⚠️ Deshabilitado (TensorFlow) |
| **Proyectos y Timelines** | 4 | ✅ Activo |
| **Reportes y Plantillas** | 3 | ✅ Activo |
| **Sistema** | 3 | ✅ Activo |

---

## 1️⃣ MÓDULO: USUARIOS Y PERFILES

---

### 📋 Tabla: `users`

**Descripción**: Gestión de usuarios del sistema

**Estadísticas**:
- Total de columnas: 9
- Total de registros: 1
- Primary Keys: 1
- Foreign Keys: 0

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `username` | VARCHAR(80) | NO | - | UNIQUE |
| 3 | `email` | VARCHAR(120) | NO | - | UNIQUE |
| 4 | `password_hash` | VARCHAR(255) | NO | - | |
| 5 | `role` | VARCHAR(20) | YES | 'student' | |
| 6 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |
| 7 | `updated_at` | DATETIME | YES | CURRENT_TIMESTAMP | ON UPDATE |
| 8 | `is_active` | BOOLEAN | YES | 1 | |
| 9 | `last_login` | DATETIME | YES | - | |

#### 💡 Columnas Destacadas

- `role` → Rol del usuario: student, teacher, admin
- `is_active` → Estado de la cuenta
- `last_login` → Última vez que ingresó al sistema

#### 📄 Registro de Ejemplo

```
id: 1
username: admin
email: admin@test.com
role: admin
is_active: True
created_at: 2025-12-10
```

---

### 📋 Tabla: `student_profiles`

**Descripción**: PERFIL ESTUDIANTIL AVANZADO CON IA

**Estadísticas**:
- Total de columnas: 30
- Total de registros: 1
- Primary Keys: 1
- Foreign Keys: 1

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `user_id` | INTEGER | NO | - | 🔗 FK → users(id) |
| 3 | `full_name` | VARCHAR(200) | YES | - | |
| 4 | `academic_level` | VARCHAR(50) | YES | - | |
| 5 | `major` | VARCHAR(100) | YES | - | |
| 6 | `semester` | INTEGER | YES | - | |
| 7 | `university` | VARCHAR(200) | YES | - | |
| 8 | `gpa` | FLOAT | YES | - | |
| 9 | `study_hours_per_week` | INTEGER | YES | - | |
| 10 | `preferred_study_time` | VARCHAR(50) | YES | - | |
| 11 | `learning_style` | VARCHAR(50) | YES | - | |
| 12 | `academic_goals` | TEXT | YES | - | |
| 13 | `strengths` | TEXT | YES | - | |
| 14 | `weaknesses` | TEXT | YES | - | |
| 15 | `interests` | TEXT | YES | - | |
| 16 | `career_aspirations` | TEXT | YES | - | |
| 17 | `thesis_topic` | VARCHAR(500) | YES | - | |
| 18 | `thesis_advisor` | VARCHAR(200) | YES | - | |
| 19 | `thesis_start_date` | DATE | YES | - | |
| 20 | `thesis_expected_end_date` | DATE | YES | - | |
| 21 | `**thesis_readiness_score**` | **INTEGER** | YES | **0** | ✨ **NUEVO** |
| 22 | `**thesis_readiness_level**` | **VARCHAR(50)** | YES | **'no_preparado'** | ✨ **NUEVO** |
| 23 | `research_experience` | TEXT | YES | - | |
| 24 | `publications` | TEXT | YES | - | |
| 25 | `**ai_profile_summary**` | **TEXT** | YES | - | ✨ **IA** |
| 26 | `**ai_personalized_advice**` | **TEXT** | YES | - | ✨ **IA** |
| 27 | `**academic_strengths**` | **JSON** | YES | - | ✨ **IA** |
| 28 | `**areas_for_improvement**` | **JSON** | YES | - | ✨ **IA** |
| 29 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |
| 30 | `updated_at` | DATETIME | YES | CURRENT_TIMESTAMP | ON UPDATE |

#### 💡 Columnas Destacadas (IA)

- `thesis_readiness_score` → Puntuación de preparación para tesis (0-100) calculada por IA
- `thesis_readiness_level` → Nivel: no_preparado, inicial, intermedio, avanzado, listo
- `ai_profile_summary` → Resumen del perfil del estudiante generado por IA
- `ai_personalized_advice` → Consejos personalizados basados en el perfil
- `academic_strengths` → JSON con fortalezas académicas detectadas por IA
- `areas_for_improvement` → JSON con áreas que necesitan mejora

#### 📄 Registro de Ejemplo

```json
{
  "id": 1,
  "user_id": 1,
  "full_name": "Administrador Test",
  "academic_level": "Pregrado",
  "major": "Ingeniería de Sistemas",
  "semester": 8,
  "thesis_readiness_score": 75,
  "thesis_readiness_level": "avanzado",
  "ai_profile_summary": "Estudiante con alto rendimiento académico...",
  "academic_strengths": ["Programación", "Bases de datos", "IA"]
}
```

---

## 2️⃣ MÓDULO: EVALUACIÓN ACADÉMICA

---

### 📋 Tabla: `writing_evaluations`

**Descripción**: EVALUACIÓN DE ESCRITURA CON IA GEMINI

**Estadísticas**:
- Total de columnas: 29
- Total de registros: 11
- Primary Keys: 1
- Foreign Keys: 2

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `user_id` | INTEGER | NO | - | 🔗 FK → users(id) |
| 3 | `document_id` | INTEGER | YES | - | 🔗 FK → documents(id) |
| 4 | `text_content` | TEXT | NO | - | |
| 5 | `title` | VARCHAR(500) | YES | - | |
| 6 | `evaluation_type` | VARCHAR(100) | YES | 'general' | |
| 7 | `**overall_score**` | **INTEGER** | YES | - | ✨ **IA** |
| 8 | `**grammar_score**` | **INTEGER** | YES | - | ✨ **IA** |
| 9 | `**coherence_score**` | **INTEGER** | YES | - | ✨ **IA** |
| 10 | `**style_score**` | **INTEGER** | YES | - | ✨ **IA** |
| 11 | `**vocabulary_score**` | **INTEGER** | YES | - | ✨ **IA** |
| 12 | `**argumentation_score**` | **INTEGER** | YES | - | ✨ **IA** |
| 13 | `**specific_errors**` | **JSON** | YES | - | ✨ **IA** |
| 14 | `**suggestions**` | **JSON** | YES | - | ✨ **IA** |
| 15 | `**tone_analysis**` | **VARCHAR(100)** | YES | - | ✨ **IA** |
| 16 | `**formality_level**` | **VARCHAR(50)** | YES | - | ✨ **IA** |
| 17 | `word_count` | INTEGER | YES | - | |
| 18 | `sentence_count` | INTEGER | YES | - | |
| 19 | `paragraph_count` | INTEGER | YES | - | |
| 20 | `readability_score` | FLOAT | YES | - | |
| 21 | `**ai_model_used**` | **VARCHAR(100)** | YES | - | ✨ **IA** |
| 22 | `**ai_tokens_used**` | **INTEGER** | YES | - | ✨ **IA** |
| 23 | `**ai_processing_time**` | **FLOAT** | YES | - | ✨ **IA** |
| 24 | `**detailed_feedback**` | **TEXT** | YES | - | ✨ **IA** |
| 25 | `**improvement_percentage**` | **FLOAT** | YES | - | ✨ **IA** |
| 26 | `previous_evaluation_id` | INTEGER | YES | - | FK → writing_evaluations(id) |
| 27 | `status` | VARCHAR(50) | YES | 'completed' | |
| 28 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |
| 29 | `updated_at` | DATETIME | YES | CURRENT_TIMESTAMP | ON UPDATE |

#### 💡 Columnas Destacadas (IA GEMINI)

- `overall_score` → Puntuación general de 0-100 calculada por Gemini AI
- `grammar_score` → Evaluación gramatical con detección de errores
- `specific_errors` → JSON con errores detectados y correcciones sugeridas
  ```json
  {
    "errores": [
      {
        "error": "incorrecto uso de mayúsculas",
        "correccion": "Universidad",
        "posicion": "línea 3"
      }
    ]
  }
  ```
- `suggestions` → JSON con sugerencias personalizadas de mejora
  ```json
  {
    "sugerencias": [
      {
        "tipo": "estructura",
        "mensaje": "Considera agregar una conclusión más sólida",
        "ejemplo": "En conclusión, este análisis demuestra..."
      }
    ]
  }
  ```
- `tone_analysis` → Análisis del tono: académico, formal, informal, persuasivo
- `formality_level` → Nivel de formalidad: muy_formal, formal, neutral, informal
- `improvement_percentage` → Porcentaje de mejora respecto a versión anterior
- `ai_model_used` → Modelo utilizado: gemini-2.5-flash, gemini-2.5-pro, etc.
- `ai_tokens_used` → Tokens consumidos en la evaluación
- `detailed_feedback` → Retroalimentación detallada generada por IA

#### 📄 Registro de Ejemplo

```json
{
  "id": 1,
  "user_id": 1,
  "title": "Ensayo sobre IA en Educación",
  "overall_score": 90,
  "grammar_score": 100,
  "coherence_score": 95,
  "style_score": 85,
  "tone_analysis": "académico",
  "formality_level": "muy_formal",
  "ai_model_used": "gemini-2.5-flash",
  "ai_tokens_used": 1500,
  "specific_errors": [
    {
      "error": "Concordancia verbal",
      "correccion": "fueron implementados",
      "linea": 5
    }
  ],
  "suggestions": [
    {
      "tipo": "estructura",
      "mensaje": "Excelente uso de conectores lógicos"
    }
  ]
}
```

---

### 📋 Tabla: `syllabus_analysis`

**Descripción**: ANÁLISIS DE SYLLABUS CON IA

**Estadísticas**:
- Total de columnas: 23
- Total de registros: 1
- Primary Keys: 1
- Foreign Keys: 2

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `user_id` | INTEGER | NO | - | 🔗 FK → users(id) |
| 3 | `document_id` | INTEGER | YES | - | 🔗 FK → documents(id) |
| 4 | `course_name` | VARCHAR(200) | YES | - | |
| 5 | `institution` | VARCHAR(200) | YES | - | |
| 6 | `**extracted_topics**` | **JSON** | YES | - | ✨ **IA** |
| 7 | `**learning_objectives**` | **JSON** | YES | - | ✨ **IA** |
| 8 | `**key_concepts**` | **JSON** | YES | - | ✨ **IA** |
| 9 | `**competencies**` | **JSON** | YES | - | ✨ **IA** |
| 10 | `**suggested_timeline**` | **JSON** | YES | - | ✨ **IA** |
| 11 | `**prerequisite_knowledge**` | **JSON** | YES | - | ✨ **IA** |
| 12 | `**difficulty_level**` | **VARCHAR(50)** | YES | - | ✨ **IA** |
| 13 | `**estimated_study_hours**` | **INTEGER** | YES | - | ✨ **IA** |
| 14 | `**recommended_resources**` | **JSON** | YES | - | ✨ **IA** |
| 15 | `**assessment_methods**` | **JSON** | YES | - | ✨ **IA** |
| 16 | `**ai_summary**` | **TEXT** | YES | - | ✨ **IA** |
| 17 | `**ai_recommendations**` | **TEXT** | YES | - | ✨ **IA** |
| 18 | `ai_model_used` | VARCHAR(100) | YES | - | |
| 19 | `ai_processing_time` | FLOAT | YES | - | |
| 20 | `confidence_score` | FLOAT | YES | - | |
| 21 | `status` | VARCHAR(50) | YES | 'completed' | |
| 22 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |
| 23 | `updated_at` | DATETIME | YES | CURRENT_TIMESTAMP | ON UPDATE |

#### 💡 Columnas Destacadas (IA)

- `extracted_topics` → JSON con temas extraídos del syllabus
- `learning_objectives` → Objetivos de aprendizaje identificados por IA
- `suggested_timeline` → Línea de tiempo sugerida para el curso
- `difficulty_level` → Nivel de dificultad: básico, intermedio, avanzado
- `estimated_study_hours` → Horas estimadas de estudio por semana
- `recommended_resources` → Recursos adicionales recomendados

---

### 📋 Tabla: `academic_courses`

**Descripción**: CURSOS ACADÉMICOS

**Estadísticas**:
- Total de columnas: 13
- Total de registros: 6
- Primary Keys: 1
- Foreign Keys: 1

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `user_id` | INTEGER | NO | - | 🔗 FK → users(id) |
| 3 | `code` | VARCHAR(20) | YES | - | |
| 4 | `name` | VARCHAR(200) | NO | - | |
| 5 | `credits` | INTEGER | YES | - | |
| 6 | `semester` | VARCHAR(20) | YES | - | |
| 7 | `professor` | VARCHAR(200) | YES | - | |
| 8 | `schedule` | TEXT | YES | - | |
| 9 | `description` | TEXT | YES | - | |
| 10 | `objectives` | TEXT | YES | - | |
| 11 | `status` | VARCHAR(50) | YES | 'active' | |
| 12 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |
| 13 | `updated_at` | DATETIME | YES | CURRENT_TIMESTAMP | ON UPDATE |

---

### 📋 Tabla: `academic_tasks`

**Descripción**: TAREAS Y TRABAJOS ACADÉMICOS

**Estadísticas**:
- Total de columnas: 15
- Total de registros: 0
- Primary Keys: 1
- Foreign Keys: 2

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `user_id` | INTEGER | NO | - | 🔗 FK → users(id) |
| 3 | `course_id` | INTEGER | YES | - | 🔗 FK → academic_courses(id) |
| 4 | `title` | VARCHAR(300) | NO | - | |
| 5 | `description` | TEXT | YES | - | |
| 6 | `task_type` | VARCHAR(50) | YES | 'assignment' | |
| 7 | `due_date` | DATETIME | YES | - | |
| 8 | `estimated_hours` | INTEGER | YES | - | |
| 9 | `priority` | VARCHAR(20) | YES | 'medium' | |
| 10 | `status` | VARCHAR(50) | YES | 'pending' | |
| 11 | `completion_percentage` | INTEGER | YES | 0 | |
| 12 | `notes` | TEXT | YES | - | |
| 13 | `attachments` | JSON | YES | - | |
| 14 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |
| 15 | `updated_at` | DATETIME | YES | CURRENT_TIMESTAMP | ON UPDATE |

---

### 📋 Tabla: `study_timers`

**Descripción**: CRONÓMETROS DE ESTUDIO (POMODORO)

**Estadísticas**:
- Total de columnas: 15
- Total de registros: 0
- Primary Keys: 1
- Foreign Keys: 2

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `user_id` | INTEGER | NO | - | 🔗 FK → users(id) |
| 3 | `task_id` | INTEGER | YES | - | 🔗 FK → academic_tasks(id) |
| 4 | `session_name` | VARCHAR(200) | YES | - | |
| 5 | `duration_minutes` | INTEGER | NO | 25 | |
| 6 | `actual_duration` | INTEGER | YES | - | |
| 7 | `break_duration` | INTEGER | YES | 5 | |
| 8 | `timer_type` | VARCHAR(50) | YES | 'pomodoro' | |
| 9 | `started_at` | DATETIME | YES | - | |
| 10 | `ended_at` | DATETIME | YES | - | |
| 11 | `status` | VARCHAR(50) | YES | 'pending' | |
| 12 | `notes` | TEXT | YES | - | |
| 13 | `productivity_rating` | INTEGER | YES | - | |
| 14 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |
| 15 | `updated_at` | DATETIME | YES | CURRENT_TIMESTAMP | ON UPDATE |

---

### 📋 Tabla: `ai_interactions`

**Descripción**: REGISTRO DE INTERACCIONES CON IA

**Estadísticas**:
- Total de columnas: 15
- Total de registros: 1
- Primary Keys: 1
- Foreign Keys: 1

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `user_id` | INTEGER | NO | - | 🔗 FK → users(id) |
| 3 | `**interaction_type**` | **VARCHAR(100)** | NO | - | ✨ **IA** |
| 4 | `**model_used**` | **VARCHAR(100)** | YES | - | ✨ **IA** |
| 5 | `input_data` | TEXT | YES | - | |
| 6 | `output_data` | TEXT | YES | - | |
| 7 | `**tokens_used**` | **INTEGER** | YES | - | ✨ **IA** |
| 8 | `processing_time` | FLOAT | YES | - | |
| 9 | `**cost_estimate**` | **DECIMAL(10, 6)** | YES | - | ✨ **IA** |
| 10 | `success` | BOOLEAN | YES | 1 | |
| 11 | `error_message` | TEXT | YES | - | |
| 12 | `metadata` | JSON | YES | - | |
| 13 | `ip_address` | VARCHAR(45) | YES | - | |
| 14 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |
| 15 | `updated_at` | DATETIME | YES | CURRENT_TIMESTAMP | ON UPDATE |

#### 💡 Columnas Destacadas (IA)

- `interaction_type` → Tipo: writing_eval, syllabus_analysis, text_analysis, report_gen
- `model_used` → Modelo de IA: gemini-2.5-flash, gemini-2.5-pro, gpt-4, etc.
- `tokens_used` → Tokens consumidos por la API
- `cost_estimate` → Costo estimado en USD

---

## 3️⃣ MÓDULO: VIDEO Y AUDIO (IA) - ⚠️ DESHABILITADO

**Estado**: Temporalmente deshabilitado debido a bug en TensorFlow 2.20 + Python 3.10

---

### 📋 Tabla: `video_sessions`

**Descripción**: SESIONES DE ANÁLISIS DE VIDEO CON IA

**Estadísticas**:
- Total de columnas: 16
- Total de registros: 24
- Primary Keys: 1
- Foreign Keys: 1

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `user_id` | INTEGER | NO | - | 🔗 FK → users(id) |
| 3 | `session_name` | VARCHAR(200) | YES | - | |
| 4 | `video_path` | VARCHAR(500) | YES | - | |
| 5 | `duration_seconds` | INTEGER | YES | - | |
| 6 | `**avg_attention_score**` | **FLOAT** | YES | - | ✨ **IA** |
| 7 | `**dominant_emotion**` | **VARCHAR(50)** | YES | - | ✨ **IA** |
| 8 | `**emotional_stability**` | **FLOAT** | YES | - | ✨ **IA** |
| 9 | `frames_analyzed` | INTEGER | YES | - | |
| 10 | `faces_detected` | INTEGER | YES | - | |
| 11 | `analysis_model` | VARCHAR(100) | YES | - | |
| 12 | `started_at` | DATETIME | YES | - | |
| 13 | `ended_at` | DATETIME | YES | - | |
| 14 | `status` | VARCHAR(50) | YES | 'recording' | |
| 15 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |
| 16 | `updated_at` | DATETIME | YES | CURRENT_TIMESTAMP | ON UPDATE |

#### 💡 Columnas Destacadas (IA)

- `avg_attention_score` → Puntuación promedio de atención (0-100) con DeepFace
- `dominant_emotion` → Emoción dominante: happy, sad, angry, neutral, surprise, fear
- `emotional_stability` → Estabilidad emocional durante la sesión

---

### 📋 Tabla: `emotion_data`

**Descripción**: DATOS EMOCIONALES FRAME POR FRAME

**Estadísticas**:
- Total de columnas: 14
- Total de registros: 0
- Primary Keys: 1
- Foreign Keys: 1

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `session_id` | INTEGER | NO | - | 🔗 FK → video_sessions(id) |
| 3 | `timestamp` | FLOAT | NO | - | |
| 4 | `frame_number` | INTEGER | YES | - | |
| 5 | `**angry**` | **FLOAT** | YES | - | ✨ **IA** |
| 6 | `**disgust**` | **FLOAT** | YES | - | ✨ **IA** |
| 7 | `**fear**` | **FLOAT** | YES | - | ✨ **IA** |
| 8 | `**happy**` | **FLOAT** | YES | - | ✨ **IA** |
| 9 | `**sad**` | **FLOAT** | YES | - | ✨ **IA** |
| 10 | `**surprise**` | **FLOAT** | YES | - | ✨ **IA** |
| 11 | `**neutral**` | **FLOAT** | YES | - | ✨ **IA** |
| 12 | `dominant_emotion` | VARCHAR(50) | YES | - | |
| 13 | `confidence` | FLOAT | YES | - | |
| 14 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |

#### 💡 Columnas Destacadas (IA - DeepFace)

- `angry`, `disgust`, `fear`, `happy`, `sad`, `surprise`, `neutral` → Probabilidades de cada emoción (0.0 - 1.0)
- `dominant_emotion` → Emoción con mayor probabilidad
- `confidence` → Confianza del modelo en la detección

---

### 📋 Tabla: `attention_metrics`

**Descripción**: MÉTRICAS DE ATENCIÓN POR FRAME

**Estadísticas**:
- Total de columnas: 12
- Total de registros: 0
- Primary Keys: 1
- Foreign Keys: 1

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `session_id` | INTEGER | NO | - | 🔗 FK → video_sessions(id) |
| 3 | `timestamp` | FLOAT | NO | - | |
| 4 | `frame_number` | INTEGER | YES | - | |
| 5 | `**attention_score**` | **FLOAT** | YES | - | ✨ **IA** |
| 6 | `**head_pose_yaw**` | **FLOAT** | YES | - | ✨ **IA** |
| 7 | `**head_pose_pitch**` | **FLOAT** | YES | - | ✨ **IA** |
| 8 | `**head_pose_roll**` | **FLOAT** | YES | - | ✨ **IA** |
| 9 | `**face_detected**` | **BOOLEAN** | YES | - | ✨ **IA** |
| 10 | `**looking_at_camera**` | **BOOLEAN** | YES | - | ✨ **IA** |
| 11 | `confidence` | FLOAT | YES | - | |
| 12 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |

#### 💡 Columnas Destacadas (IA)

- `attention_score` → Puntuación de atención (0-100)
- `head_pose_yaw`, `head_pose_pitch`, `head_pose_roll` → Rotación de la cabeza
- `looking_at_camera` → Si el estudiante está mirando la cámara

---

### 📋 Tabla: `audio_sessions`

**Descripción**: SESIONES DE AUDIO

**Estadísticas**:
- Total de columnas: 11
- Total de registros: 0
- Primary Keys: 1
- Foreign Keys: 1

---

### 📋 Tabla: `audio_transcriptions`

**Descripción**: TRANSCRIPCIONES DE AUDIO CON IA

**Estadísticas**:
- Total de columnas: 11
- Total de registros: 0
- Primary Keys: 1
- Foreign Keys: 1

#### 💡 Columnas Destacadas (IA)

- `transcription_text` → Texto transcrito del audio
- `confidence_score` → Confianza de la transcripción
- `language_detected` → Idioma detectado automáticamente

---

## 4️⃣ MÓDULO: PROYECTOS Y TIMELINES

---

### 📋 Tabla: `projects`

**Descripción**: GESTIÓN DE PROYECTOS

**Estadísticas**:
- Total de columnas: 12
- Total de registros: 2
- Primary Keys: 1
- Foreign Keys: 1

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `user_id` | INTEGER | NO | - | 🔗 FK → users(id) |
| 3 | `name` | VARCHAR(200) | NO | - | |
| 4 | `description` | TEXT | YES | - | |
| 5 | `project_type` | VARCHAR(50) | YES | 'general' | |
| 6 | `start_date` | DATE | YES | - | |
| 7 | `end_date` | DATE | YES | - | |
| 8 | `status` | VARCHAR(50) | YES | 'active' | |
| 9 | `completion_percentage` | INTEGER | YES | 0 | |
| 10 | `metadata` | JSON | YES | - | |
| 11 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |
| 12 | `updated_at` | DATETIME | YES | CURRENT_TIMESTAMP | ON UPDATE |

---

### 📋 Tabla: `time_sessions`

**Descripción**: SESIONES DE TIEMPO DE TRABAJO

**Estadísticas**:
- Total de columnas: 10
- Total de registros: 4
- Primary Keys: 1
- Foreign Keys: 1

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `project_id` | INTEGER | NO | - | 🔗 FK → projects(id) |
| 3 | `start_time` | DATETIME | NO | - | |
| 4 | `end_time` | DATETIME | YES | - | |
| 5 | `duration_minutes` | INTEGER | YES | - | |
| 6 | `description` | TEXT | YES | - | |
| 7 | `session_type` | VARCHAR(50) | YES | 'work' | |
| 8 | `productive` | BOOLEAN | YES | 1 | |
| 9 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |
| 10 | `updated_at` | DATETIME | YES | CURRENT_TIMESTAMP | ON UPDATE |

---

### 📋 Tabla: `timelines`

**Descripción**: LÍNEAS DE TIEMPO PARA PROYECTOS

**Estadísticas**:
- Total de columnas: 14
- Total de registros: 5
- Primary Keys: 1
- Foreign Keys: 1

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `user_id` | INTEGER | NO | - | 🔗 FK → users(id) |
| 3 | `title` | VARCHAR(200) | NO | - | |
| 4 | `description` | TEXT | YES | - | |
| 5 | `timeline_type` | VARCHAR(50) | YES | 'project' | |
| 6 | `**course_topic**` | **VARCHAR(255)** | YES | - | ✨ **NUEVO** |
| 7 | `start_date` | DATE | YES | - | |
| 8 | `end_date` | DATE | YES | - | |
| 9 | `status` | VARCHAR(50) | YES | 'active' | |
| 10 | `completion_percentage` | INTEGER | YES | 0 | |
| 11 | `steps_json` | JSON | YES | - | |
| 12 | `color` | VARCHAR(7) | YES | '#3B82F6' | |
| 13 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |
| 14 | `updated_at` | DATETIME | YES | CURRENT_TIMESTAMP | ON UPDATE |

#### 💡 Columnas Destacadas

- `timeline_type` → Tipo: project, course, custom, thesis
- `course_topic` → ✅ NUEVO: Tema específico del curso para timelines académicas
- `steps_json` → JSON con los pasos de la línea de tiempo
- `color` → Color en formato hexadecimal para visualización

---

### 📋 Tabla: `timeline_steps`

**Descripción**: PASOS DE LÍNEAS DE TIEMPO

**Estadísticas**:
- Total de columnas: 12
- Total de registros: 17
- Primary Keys: 1
- Foreign Keys: 1

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `timeline_id` | INTEGER | NO | - | 🔗 FK → timelines(id) |
| 3 | `title` | VARCHAR(200) | NO | - | |
| 4 | `description` | TEXT | YES | - | |
| 5 | `step_order` | INTEGER | NO | - | |
| 6 | `start_date` | DATE | YES | - | |
| 7 | `end_date` | DATE | YES | - | |
| 8 | `status` | VARCHAR(50) | YES | 'pending' | |
| 9 | `completion_percentage` | INTEGER | YES | 0 | |
| 10 | `metadata` | JSON | YES | - | |
| 11 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |
| 12 | `updated_at` | DATETIME | YES | CURRENT_TIMESTAMP | ON UPDATE |

---

## 5️⃣ MÓDULO: REPORTES Y PLANTILLAS

---

### 📋 Tabla: `reports`

**Descripción**: REPORTES GENERADOS CON IA

**Estadísticas**:
- Total de columnas: 18
- Total de registros: 0
- Primary Keys: 1
- Foreign Keys: 1

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `user_id` | INTEGER | NO | - | 🔗 FK → users(id) |
| 3 | `title` | VARCHAR(300) | NO | - | |
| 4 | `**report_type**` | **VARCHAR(100)** | NO | - | ✨ **IA** |
| 5 | `**personalization_profile**` | **JSON** | YES | - | ✨ **IA** |
| 6 | `start_date` | DATE | YES | - | |
| 7 | `end_date` | DATE | YES | - | |
| 8 | `**executive_summary**` | **TEXT** | YES | - | ✨ **IA** |
| 9 | `**key_findings**` | **JSON** | YES | - | ✨ **IA** |
| 10 | `**recommendations**` | **JSON** | YES | - | ✨ **IA** |
| 11 | `**charts_data**` | **JSON** | YES | - | ✨ **IA** |
| 12 | `**ai_insights**` | **TEXT** | YES | - | ✨ **IA** |
| 13 | `file_path` | VARCHAR(500) | YES | - | |
| 14 | `**file_format**` | **VARCHAR(10)** | YES | - | ✨ **IA** |
| 15 | `file_size` | INTEGER | YES | - | |
| 16 | `status` | VARCHAR(50) | YES | 'draft' | |
| 17 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |
| 18 | `updated_at` | DATETIME | YES | CURRENT_TIMESTAMP | ON UPDATE |

#### 💡 Columnas Destacadas (IA)

- `report_type` → Tipo: academic, writing, video, project, complete
- `personalization_profile` → JSON con perfil del estudiante para personalizar
  ```json
  {
    "nombre": "Estudiante",
    "nivel": "avanzado",
    "objetivos": ["Mejorar escritura académica", "Tesis"],
    "estilo_aprendizaje": "visual"
  }
  ```
- `executive_summary` → Resumen ejecutivo generado por IA
- `key_findings` → Hallazgos clave del análisis
- `recommendations` → Recomendaciones personalizadas
- `charts_data` → Datos para gráficos y visualizaciones
- `ai_insights` → Insights adicionales generados por IA
- `file_format` → Formato: PDF, DOCX, PPTX

---

### 📋 Tabla: `generated_templates`

**Descripción**: PLANTILLAS GENERADAS (PDF, DOCX, PPTX)

**Estadísticas**:
- Total de columnas: 13
- Total de registros: 0
- Primary Keys: 1
- Foreign Keys: 1

#### Columnas Detalladas

| # | Nombre | Tipo | NULL | Default | Extras |
|---|--------|------|------|---------|--------|
| 1 | `id` | INTEGER | NO | - | 🔑 PK |
| 2 | `user_id` | INTEGER | NO | - | 🔗 FK → users(id) |
| 3 | `template_name` | VARCHAR(200) | NO | - | |
| 4 | `template_type` | VARCHAR(50) | NO | - | |
| 5 | `file_path` | VARCHAR(500) | NO | - | |
| 6 | `file_format` | VARCHAR(10) | NO | - | |
| 7 | `file_size` | INTEGER | YES | - | |
| 8 | `thumbnail_path` | VARCHAR(500) | YES | - | |
| 9 | `content_data` | JSON | YES | - | |
| 10 | `generation_params` | JSON | YES | - | |
| 11 | `status` | VARCHAR(50) | YES | 'active' | |
| 12 | `created_at` | DATETIME | YES | CURRENT_TIMESTAMP | |
| 13 | `updated_at` | DATETIME | YES | CURRENT_TIMESTAMP | ON UPDATE |

---

### 📋 Tabla: `documents`

**Descripción**: DOCUMENTOS SUBIDOS POR USUARIOS

**Estadísticas**:
- Total de columnas: 13
- Total de registros: 0
- Primary Keys: 1
- Foreign Keys: 1

---

## 6️⃣ MÓDULO: SISTEMA Y ANÁLISIS

---

### 📋 Tabla: `text_analysis`

**Descripción**: ANÁLISIS DE TEXTO CON IA

**Estadísticas**:
- Total de columnas: 18
- Total de registros: 0
- Primary Keys: 1
- Foreign Keys: 2

---

### 📋 Tabla: `system_logs`

**Descripción**: LOGS DEL SISTEMA

**Estadísticas**:
- Total de columnas: 11
- Total de registros: 0
- Primary Keys: 1
- Foreign Keys: 1

---

### 📋 Tabla: `alembic_version`

**Descripción**: VERSIÓN DE MIGRACIONES (ALEMBIC)

**Estadísticas**:
- Total de columnas: 1
- Total de registros: 0
- Primary Keys: 1
- Foreign Keys: 0

---

## 📊 RESUMEN DE MEJORAS DEL NODO DIGITAL

### ✨ Nuevas Capacidades con IA

#### 1. Evaluación de Escritura (writing_evaluations)
- ✅ 29 columnas con análisis completo por Gemini AI
- ✅ Detección automática de errores gramaticales
- ✅ Sugerencias personalizadas con ejemplos
- ✅ Análisis de tono y formalidad
- ✅ Medición de mejora entre versiones
- ✅ 11 evaluaciones registradas actualmente

#### 2. Perfiles Estudiantiles Avanzados (student_profiles)
- ✅ 30 columnas con análisis integral
- ✅ Puntuación de preparación para tesis (thesis_readiness_score)
- ✅ Nivel de preparación (thesis_readiness_level)
- ✅ Resumen de perfil generado por IA
- ✅ Consejos personalizados
- ✅ Fortalezas y áreas de mejora en JSON

#### 3. Análisis de Syllabus (syllabus_analysis)
- ✅ Extracción automática de temas
- ✅ Identificación de objetivos de aprendizaje
- ✅ Generación de timeline sugerido
- ✅ Recomendaciones de recursos adicionales

#### 4. Timelines Mejoradas (timelines)
- ✅ Nueva columna `course_topic` para especificar tema del curso
- ✅ Soporte para múltiples tipos: project, course, custom, thesis
- ✅ 5 timelines activas con 17 pasos

#### 5. Video/Audio (Deshabilitado Temporalmente)
- ⚠️ DeepFace para análisis facial
- ⚠️ Detección de emociones (7 categorías)
- ⚠️ Métricas de atención
- ⚠️ Transcripción de audio
- ⚠️ **Issue**: TensorFlow 2.20 + Python 3.10 causa deadlock

---

## 🔧 ESTADO DEL SISTEMA

### ✅ Módulos Activos
1. **Evaluación de Escritura**: 100% funcional con Gemini AI
2. **Perfiles Estudiantiles**: Activo con IA
3. **Análisis de Syllabus**: Activo
4. **Proyectos y Timelines**: Activo (5 timelines, 2 proyectos)
5. **Cursos Académicos**: Activo (6 cursos)

### ⚠️ Módulos Deshabilitados
1. **Video/Audio**: Deshabilitado por bug de TensorFlow

### 📈 Estadísticas de Datos

| Tabla | Registros | Estado |
|-------|-----------|--------|
| users | 1 | ✅ Activo |
| student_profiles | 1 | ✅ Activo |
| writing_evaluations | 11 | ✅ Activo |
| syllabus_analysis | 1 | ✅ Activo |
| academic_courses | 6 | ✅ Activo |
| timelines | 5 | ✅ Activo |
| timeline_steps | 17 | ✅ Activo |
| projects | 2 | ✅ Activo |
| time_sessions | 4 | ✅ Activo |
| video_sessions | 24 | ⚠️ Sin análisis facial |
| ai_interactions | 1 | ✅ Activo |

**Total**: 73 registros activos

---

## 🚀 CÓMO ACCEDER A LA BASE DE DATOS

### Opción 1: phpMyAdmin (Recomendado para principiantes)

1. Asegúrate de tener XAMPP o WAMP instalado
2. Abre tu navegador
3. Ve a: http://localhost/phpmyadmin
4. Usuario: `root`
5. Contraseña: `ADMIN`
6. Selecciona la base de datos: `rendimiento_estudiantil`

### Opción 2: MySQL Workbench (Recomendado para desarrolladores)

1. Abre MySQL Workbench
2. Crea una nueva conexión:
   - Connection Name: Plataforma Estudiantil
   - Hostname: localhost
   - Port: 3306
   - Username: root
   - Password: ADMIN
3. Haz clic en "Test Connection"
4. Selecciona `rendimiento_estudiantil`

### Opción 3: Línea de Comandos

```bash
# Conectarse a MySQL
mysql -u root -p rendimiento_estudiantil

# Contraseña: ADMIN

# Ver todas las tablas
SHOW TABLES;

# Ver estructura de una tabla
DESCRIBE writing_evaluations;

# Consultar datos
SELECT * FROM writing_evaluations LIMIT 10;
```

### Opción 4: DBeaver (Recomendado para análisis avanzado)

1. Descarga DBeaver desde https://dbeaver.io/
2. Crea nueva conexión MySQL
3. Ingresa los datos:
   - Host: localhost
   - Port: 3306
   - Database: rendimiento_estudiantil
   - Username: root
   - Password: ADMIN
4. Navega las tablas visualmente

---

## 📝 NOTAS IMPORTANTES

### 🔒 Seguridad
- **IMPORTANTE**: En producción, cambia la contraseña de la base de datos
- No uses `root` con contraseña simple en producción
- Crea un usuario específico con permisos limitados

### 🔄 Backups
- Realiza backups regulares de la base de datos
- Comando para backup:
  ```bash
  mysqldump -u root -p rendimiento_estudiantil > backup.sql
  ```

### 📦 Migraciones
- Las migraciones se gestionan con Alembic
- Ubicación: `backend/migrations/versions/`
- Para aplicar migraciones:
  ```bash
  cd backend
  python aplicar_migracion.py
  ```

---

## 📞 SOPORTE

Si necesitas ayuda con la base de datos:

1. Revisa los logs en: `backend/logs/`
2. Verifica la conexión en: `backend/.env`
3. Consulta la documentación en: `docs/`

---

**Última actualización**: 11 de Diciembre de 2025  
**Versión del sistema**: 2.0 (Nodo Digital Mejorado)
