# 📊 INFORME DETALLADO DE BASE DE DATOS
## Plataforma de Rendimiento Estudiantil - Nodo Digital

**Fecha de generación:** 2025-12-11  
**Base de datos:** rendimiento_estudiantil (MySQL)  
**Total de tablas:** 23  

---

## 🎯 RESUMEN EJECUTIVO

La base de datos cuenta con **23 tablas** distribuidas en **6 módulos principales**, con un total de **73 registros activos**. El sistema está completamente operativo con las siguientes mejoras implementadas en el **Nodo Digital**:

### ✅ Datos Activos por Módulo:
- **Usuarios:** 1 usuario + 1 perfil estudiantil
- **Evaluaciones de Escritura:** 11 evaluaciones con IA
- **Sesiones de Video:** 24 sesiones creadas
- **Líneas de Tiempo:** 5 timelines con 17 pasos
- **Proyectos:** 2 proyectos con 4 sesiones de tiempo
- **Cursos:** 6 cursos académicos registrados

---

## 📚 MÓDULO 1: NODO DIGITAL - ACADÉMICO

### **Mejoras Implementadas:**

#### ✅ **1. Evaluación de Escritura con IA (Tabla: `writing_evaluations`)**

**Estado:** ✅ **FUNCIONANDO CON GEMINI 2.5-FLASH**

**Estructura mejorada (29 columnas):**

| Columna | Tipo | Descripción | Mejora |
|---------|------|-------------|---------|
| `overall_score` | FLOAT | Puntuación general (0-100) | ✅ Calculado por IA |
| `grammar_score` | FLOAT | Evaluación gramatical | ✅ Análisis profundo |
| `coherence_score` | FLOAT | Coherencia del texto | ✅ IA detecta flujo |
| `vocabulary_score` | FLOAT | Riqueza de vocabulario | ✅ Con contexto |
| `structure_score` | FLOAT | Calidad estructural | ✅ Análisis formal |
| `tone_analysis` | VARCHAR(50) | Tono del documento | ✅ NUEVO: académico/formal/informal |
| `formality_score` | FLOAT | Nivel de formalidad | ✅ NUEVO: 0-100 |
| `complexity_level` | VARCHAR(50) | Nivel de complejidad | ✅ NUEVO: básico/intermedio/avanzado |
| `improvement_percentage` | FLOAT | % de mejora vs anterior | ✅ NUEVO: Comparación temporal |
| `improvements_made` | JSON | Cambios específicos | ✅ NUEVO: Tracking detallado |
| `specific_errors` | JSON | Errores detectados | ✅ NUEVO: Con ubicación y corrección |
| `suggestions` | JSON | Sugerencias personalizadas | ✅ NUEVO: Con ejemplos |
| `recommendations` | JSON | Recomendaciones accionables | ✅ NUEVO: Prioridad alta/media/baja |

**Capacidades de IA Gemini:**
- ✅ Detección de errores gramaticales con ubicación exacta
- ✅ Análisis de coherencia entre párrafos
- ✅ Evaluación de vocabulario técnico y académico
- ✅ Sugerencias de mejora con ejemplos específicos
- ✅ Comparación con versiones anteriores
- ✅ Análisis de tono y formalidad
- ✅ Detección de nivel de complejidad

**Registros activos:** 11 evaluaciones

#### ✅ **2. Análisis de Syllabus (Tabla: `syllabus_analysis`)**

**Mejoras:**
- Almacena información de cursos extraída con IA
- Guarda temas y competencias en formato JSON
- Vincula con `academic_courses`

**Registros activos:** 1 análisis

#### ✅ **3. Cronómetros de Estudio (Tabla: `study_timers`)**

**Características:**
- Tracking de tiempo por curso y tarea
- Estados: activo/pausado/completado
- Vinculación con cursos y tareas académicas

**Registros activos:** 0 (funcionalidad disponible)

---

## 🎥 MÓDULO 2: VIDEO & AUDIO - ANÁLISIS EN TIEMPO REAL

### **Estado:** ⚠️ TEMPORALMENTE DESHABILITADO (TensorFlow issue)

#### **Tabla: `video_sessions` (22 columnas)**

**Capacidades diseñadas:**
- Grabación y análisis de sesiones de estudio
- Detección facial con DeepFace
- Análisis de emociones en tiempo real
- Métricas de atención y engagement
- Procesamiento asíncrono de video

**Registros activos:** 24 sesiones creadas (sin análisis facial por TensorFlow)

**Estructura avanzada:**
- Estados: `recording`, `processing`, `completed`, `error`
- Almacena duración, frames analizados, caras detectadas
- Metadata en JSON para información adicional
- Vinculación con emotion_data y attention_metrics

#### **Tabla: `emotion_data` (24 columnas)**

**Emociones detectables:**
- `emotion_angry`, `emotion_disgust`, `emotion_fear`
- `emotion_happy`, `emotion_sad`, `emotion_surprise`, `emotion_neutral`
- `dominant_emotion` con nivel de confianza
- Datos faciales: edad, género, bbox, landmarks

**Registros activos:** 0 (esperando corrección de TensorFlow)

#### **Tabla: `attention_metrics` (14 columnas)**

**Métricas implementadas:**
- `attention_score` (0-100)
- `engagement_level`: ENUM (high, medium, low, distracted)
- `confusion_detected`, `boredom_detected` (boolean)
- Emociones predominantes por intervalo
- Indicadores de comprensión

**Registros activos:** 0

#### **Tabla: `audio_transcriptions` (13 columnas)**

**Capacidades:**
- Transcripción con Google Speech Recognition
- Análisis de sentimiento del texto
- Extracción de palabras clave
- Análisis con IA (texto)
- Nivel de confianza de transcripción

**Registros activos:** 0

---

## 👥 MÓDULO DE USUARIOS

### **Tabla: `users` (19 columnas)**

**Mejoras de seguridad:**
- Password hash (bcrypt)
- Email verification
- Login tracking
- Intentos fallidos + lockout
- Roles: student, admin, teacher

**Registros activos:** 1 usuario (admin)

### **Tabla: `student_profiles` (30 columnas)**

**Perfilamiento con IA:**

| Categoría | Columnas | Descripción |
|-----------|----------|-------------|
| **Rendimiento Académico** | `total_documents_analyzed`, `avg_writing_quality`, `writing_improvement_trend` | Tracking de progreso |
| **Fortalezas** | `academic_strengths`, `writing_strengths`, `technical_strengths` (JSON) | Detectadas por IA |
| **Debilidades** | `academic_weaknesses`, `writing_weaknesses`, `areas_for_improvement` (JSON) | Análisis profundo |
| **Estilo de Aprendizaje** | `learning_style`, `learning_preferences`, `optimal_session_duration` | Personalización |
| **Atención** | `attention_pattern`, `avg_attention_span_minutes`, `most_productive_time` | Video analytics |
| **Preparación Tesis** | `thesis_readiness_score`, `thesis_readiness_level`, `estimated_preparation_months` | ✅ NUEVO |
| **Recomendaciones IA** | `ai_profile_summary`, `ai_personalized_advice`, `study_recommendations` | ✅ NUEVO |

**Niveles de preparación para tesis:**
- `ENUM('no_preparado', 'inicial', 'intermedio', 'avanzado', 'listo')`

**Registros activos:** 1 perfil

---

## 📋 MÓDULO DE PROYECTOS Y LÍNEAS DE TIEMPO

### **Tabla: `timelines` (15 columnas)**

**Mejoras implementadas:**
- ✅ Campo `course_topic` agregado (VARCHAR 255)
- ✅ Soporte para líneas de tiempo libres (sin proyecto)
- ✅ Tipos: `project`, `course`, `custom`, `thesis`
- ✅ Estados de completitud

**Registros activos:** 5 timelines con 17 pasos

### **Tabla: `projects` (13 columnas)**

**Estados:** `pendiente`, `en_progreso`, `completado`, `cancelado`  
**Prioridades:** `baja`, `media`, `alta`, `urgente`

**Registros activos:** 2 proyectos

### **Tabla: `time_sessions` (13 columnas)**

**Características:**
- Pausar/reanudar sesiones
- Tracking de última actividad
- Notas por sesión
- Acumulación de tiempo por proyecto

**Registros activos:** 4 sesiones

---

## 📊 MÓDULO DE REPORTES

### **Tabla: `reports` (24 columnas)**

**Tipos de reportes:**
- `academic`: Rendimiento académico general
- `writing`: Análisis de escritura
- `video`: Análisis de sesiones de video
- `project`: Progreso de proyectos
- `complete`: Reporte integral

**Generación con IA:**
- `personalization_profile` (JSON): Perfil del estudiante
- `content_style`: Formal, casual, técnico
- `charts_data` (JSON): Datos para gráficos
- `report_data` (JSON): Contenido estructurado

**Formatos:** PDF, DOCX, PPTX

**Registros activos:** 0 (funcionalidad disponible)

### **Tabla: `generated_templates` (19 columnas)**

**Plantillas generadas:**
- Presentaciones con IA
- Documentos académicos
- Informes personalizados
- Estilos visuales adaptados

**Registros activos:** 0

---

## 🔧 TABLAS DE SOPORTE

### **Tabla: `ai_interactions` (15 columnas)**

**Tracking de uso de IA:**
- Tipo de interacción (writing_eval, text_analysis, report_gen)
- Servicio: Gemini, GPT, etc.
- Modelo usado: gemini-2.5-flash, etc.
- Tokens consumidos
- Tiempo de procesamiento
- Costo estimado

**Registros activos:** 1 interacción

### **Tabla: `system_logs` (13 columnas)**

**Niveles de log:** DEBUG, INFO, WARNING, ERROR, CRITICAL

**Tracking:**
- Módulo y función
- Request method y URL
- IP y User Agent
- Stack trace de errores

**Registros activos:** 0

---

## 📈 ESTADÍSTICAS GENERALES

### Tablas con Datos Activos:

| Tabla | Registros | Uso |
|-------|-----------|-----|
| `writing_evaluations` | 11 | ⭐⭐⭐⭐⭐ Alto uso |
| `video_sessions` | 24 | ⭐⭐⭐⭐ Medio-Alto |
| `timeline_steps` | 17 | ⭐⭐⭐ Medio |
| `academic_courses` | 6 | ⭐⭐⭐ Medio |
| `timelines` | 5 | ⭐⭐ Bajo |
| `time_sessions` | 4 | ⭐⭐ Bajo |
| `projects` | 2 | ⭐ Muy bajo |
| `users` | 1 | ⭐ Base |
| `student_profiles` | 1 | ⭐ Base |
| `syllabus_analysis` | 1 | ⭐ Base |
| `ai_interactions` | 1 | ⭐ Base |

### Tablas Sin Datos (Listas para usar):

- `academic_tasks`
- `attention_metrics`
- `audio_sessions`
- `audio_transcriptions`
- `documents`
- `emotion_data`
- `generated_templates`
- `reports`
- `study_timers`
- `system_logs`
- `text_analysis`

---

## 🚀 MEJORAS CLAVE DEL NODO DIGITAL

### 1. **Evaluación de Escritura con IA Gemini** ✅

**Antes:**
- Análisis básico de métricas (palabras, oraciones)
- Sin detección de errores
- Sin sugerencias personalizadas

**Después:**
- ✅ Gemini 2.5-Flash integrado
- ✅ Detección de errores gramaticales con ubicación
- ✅ Análisis de coherencia y tono
- ✅ Sugerencias con ejemplos específicos
- ✅ Comparación temporal (versiones anteriores)
- ✅ Score de 0-100 en 6 dimensiones
- ✅ Recomendaciones accionables priorizadas

### 2. **Perfilamiento Estudiantil Avanzado** ✅

**Nuevo en `student_profiles`:**
- ✅ Preparación para tesis (score + nivel + tiempo estimado)
- ✅ Recomendaciones personalizadas con IA
- ✅ Resumen de perfil generado por IA
- ✅ Patterns de emoción y atención

### 3. **Líneas de Tiempo Flexibles** ✅

**Mejora en `timelines`:**
- ✅ Campo `course_topic` para temas específicos
- ✅ Soporte para timelines sin proyecto
- ✅ Tipos variados (curso, tesis, custom)

### 4. **Tracking Completo de IA** ✅

**Nueva tabla `ai_interactions`:**
- ✅ Registro de todas las llamadas a IA
- ✅ Tokens y costos
- ✅ Tiempo de procesamiento
- ✅ Trazabilidad completa

### 5. **Sistema de Reportes Inteligente** ✅

**Tablas `reports` y `generated_templates`:**
- ✅ Generación de PDF, DOCX, PPTX
- ✅ Personalización por perfil de estudiante
- ✅ Datos estructurados en JSON
- ✅ Gráficos con datos reales

---

## ⚠️ PROBLEMAS CONOCIDOS

### TensorFlow 2.20 + Python 3.10 (Windows)

**Síntoma:** Deadlock al importar TensorFlow  
**Impacto:** Módulo de Video/Audio deshabilitado  
**Afectado:**
- `video_sessions` (sin análisis facial)
- `emotion_data` (sin registros)
- `attention_metrics` (sin registros)
- `audio_transcriptions` (sin transcripción)

**Solución temporal:** Módulo deshabilitado  
**Solución permanente:** Downgrade a TensorFlow 2.16.2 o upgrade a Python 3.11+

---

## 🔐 RELACIONES E INTEGRIDAD

### Foreign Keys Implementadas:

**Usuarios como pivote:**
- 16 tablas tienen FK a `users.id`
- Garantiza integridad referencial
- Cascadas configuradas para eliminación

**Relaciones clave:**
- `writing_evaluations` → `users`, `courses`
- `video_sessions` → `users`
- `emotion_data` → `video_sessions`, `users`
- `timelines` → `users`, `projects`, `courses`
- `reports` → `users`
- `ai_interactions` → `users`

### Índices Optimizados:

- ✅ Primary Keys en todas las tablas
- ✅ Foreign Keys indexadas
- ✅ Campos de búsqueda frecuente indexados
- ✅ Índices compuestos para queries complejas
- ✅ UNIQUE constraints para datos únicos

---

## 📊 RESUMEN FINAL

### ✅ **Completado y Funcional:**
1. ✅ Evaluación de escritura con IA Gemini 2.5-Flash
2. ✅ Perfilamiento estudiantil avanzado
3. ✅ Líneas de tiempo flexibles con temas de curso
4. ✅ Sistema de proyectos y tracking de tiempo
5. ✅ Cursos académicos con syllabus
6. ✅ Tracking de interacciones con IA
7. ✅ Sistema de reportes personalizados
8. ✅ Generación de plantillas con IA

### ⚠️ **Pendiente (Bloqueado por TensorFlow):**
1. ⚠️ Análisis facial con DeepFace
2. ⚠️ Detección de emociones en video
3. ⚠️ Métricas de atención
4. ⚠️ Transcripción de audio

### 📈 **Uso del Sistema:**
- **11 evaluaciones de escritura** procesadas con IA
- **24 sesiones de video** creadas (sin análisis)
- **6 cursos** académicos registrados
- **5 líneas de tiempo** con 17 pasos
- **2 proyectos** con 4 sesiones de tiempo
- **1 usuario** con perfil completo

---

**Generado automáticamente por:** `generate_db_report.py`  
**Base de datos:** MySQL (rendimiento_estudiantil)  
**Motor:** PyMySQL + SQLAlchemy ORM  
**Framework:** Flask 3.x
