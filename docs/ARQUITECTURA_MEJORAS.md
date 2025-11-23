# 🏗️ Arquitectura de las Nuevas Funcionalidades

## 📊 Diagrama General

```
┌─────────────────────────────────────────────────────────────┐
│                    PLATAFORMA ESTUDIANTIL                    │
│                   http://localhost:3000                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    ACADEMIC DASHBOARD                        │
│                    /analisis (React)                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Gestión  │  │  Tools   │  │ Timeline │  │ Sílabos  │   │
│  │ 🎨 NEW   │  │          │  │ 🕒 NEW   │  │ 📄 NEW   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│       │              │              │              │         │
│       ▼              ▼              ▼              ▼         │
│  Course      Study Tools    Timeline     Syllabus          │
│  Manager       (IA)         Creator      Analyzer          │
│   Pro                         Pro           Pro            │
└───────┬──────────────┬──────────┬──────────┬───────────────┘
        │              │          │          │
        │    API REST  │          │          │
        ▼              ▼          ▼          ▼
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND (Flask)                             │
│                  http://localhost:5000                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  /api/academic/         /api/timeline/                      │
│  ├─ course/create       ├─ create                           │
│  ├─ course/{id}         ├─ user/{id}                        │
│  ├─ upload-syllabus     └─ {id}/step/{id}/toggle           │
│  ├─ syllabus-history                                        │
│  └─ syllabus/{id}                                           │
│                                                              │
└───────┬──────────────┬──────────┬──────────┬───────────────┘
        │              │          │          │
        ▼              ▼          ▼          ▼
┌─────────────────────────────────────────────────────────────┐
│                  BASE DE DATOS (MySQL)                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  academic_courses (actualizada)                             │
│  ├─ code VARCHAR(50) ⭐ NEW                                 │
│  ├─ category VARCHAR(50) ⭐ NEW                             │
│  ├─ icon VARCHAR(50) ⭐ NEW                                 │
│  └─ color VARCHAR(20) 🔄 UPDATED                            │
│                                                              │
│  syllabus_analysis ⭐ NEW TABLE                             │
│  ├─ course_info_json TEXT                                   │
│  ├─ topics_json TEXT                                        │
│  └─ uploaded_at TIMESTAMP                                   │
│                                                              │
│  timeline_steps ⭐ NEW TABLE                                │
│  ├─ title VARCHAR(200)                                      │
│  ├─ order INT                                               │
│  ├─ completed BOOLEAN                                       │
│  └─ completed_at DATETIME                                   │
│                                                              │
│  timelines (actualizada)                                    │
│  └─ end_date DATETIME ⭐ NEW                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Datos: Gestión de Cursos

```
Usuario                Frontend              Backend             Database
  │                      │                     │                   │
  │   1. Click crear    │                     │                   │
  ├────────────────────>│                     │                   │
  │                      │                     │                   │
  │   2. Llenar form    │                     │                   │
  │   (icono, color,    │                     │                   │
  │    categoría)       │                     │                   │
  ├────────────────────>│                     │                   │
  │                      │                     │                   │
  │   3. Submit         │                     │                   │
  ├────────────────────>│  POST /course/create│                   │
  │                      ├───────────────────>│                   │
  │                      │                     │ INSERT INTO       │
  │                      │                     │ academic_courses  │
  │                      │                     ├─────────────────>│
  │                      │                     │<─────────────────┤
  │                      │<───────────────────┤ Course created    │
  │                      │  {id, name, icon}  │                   │
  │<─────────────────────                     │                   │
  │   4. Curso creado   │                     │                   │
  │   (tarjeta con      │                     │                   │
  │    icono y color)   │                     │                   │
```

---

## 📄 Flujo de Datos: Análisis de Sílabos

```
Usuario              Frontend            Backend           IA Service        Database
  │                    │                   │                   │               │
  │ 1. Seleccionar    │                   │                   │               │
  │    curso          │                   │                   │               │
  ├──────────────────>│                   │                   │               │
  │                    │                   │                   │               │
  │ 2. Cargar PDF     │                   │                   │               │
  ├──────────────────>│ POST upload-      │                   │               │
  │                    │ syllabus          │                   │               │
  │                    ├─────────────────>│                   │               │
  │                    │ (multipart/form)  │                   │               │
  │                    │                   │ 3. Guardar PDF    │               │
  │                    │                   ├─────────────────> │               │
  │                    │                   │                   │               │
  │                    │                   │ 4. Extraer texto  │               │
  │                    │                   │ (PyPDF2)          │               │
  │                    │                   │                   │               │
  │                    │                   │ 5. Analizar con IA│               │
  │                    │                   ├─────────────────>│               │
  │                    │                   │ Gemini API        │               │
  │                    │                   │<─────────────────┤               │
  │                    │                   │ {topics, info}    │               │
  │                    │                   │                   │               │
  │                    │                   │ 6. Guardar análisis               │
  │                    │                   ├─────────────────────────────────>│
  │                    │                   │ INSERT syllabus_analysis          │
  │                    │                   │<─────────────────────────────────┤
  │                    │<─────────────────┤                   │               │
  │                    │ {syllabus_id,     │                   │               │
  │                    │  topics, info}    │                   │               │
  │<───────────────────                   │                   │               │
  │ 7. Ver análisis   │                   │                   │               │
  │    en historial   │                   │                   │               │
  │                    │                   │                   │               │
  │ 8. Click tema     │                   │                   │               │
  ├──────────────────>│ PUT /topic/toggle │                   │               │
  │                    ├─────────────────>│ UPDATE topics_json│               │
  │                    │                   ├─────────────────────────────────>│
  │                    │                   │<─────────────────────────────────┤
  │                    │<─────────────────┤                   │               │
  │<───────────────────   ✅ Completado   │                   │               │
```

---

## 🕒 Flujo de Datos: Líneas de Tiempo

### Opción A: Con IA

```
Usuario              Frontend            Backend           IA Service        Database
  │                    │                   │                   │               │
  │ 1. Click crear    │                   │                   │               │
  │    timeline       │                   │                   │               │
  ├──────────────────>│                   │                   │               │
  │                    │                   │                   │               │
  │ 2. Activar IA     │                   │                   │               │
  │    checkbox       │                   │                   │               │
  ├──────────────────>│                   │                   │               │
  │                    │                   │                   │               │
  │ 3. Escribir       │                   │                   │               │
  │    contexto       │                   │                   │               │
  │ "Examen cálculo   │                   │                   │               │
  │  en 2 semanas"    │                   │                   │               │
  ├──────────────────>│                   │                   │               │
  │                    │                   │                   │               │
  │ 4. Submit         │ POST /timeline/   │                   │               │
  │                    │ create            │                   │               │
  │                    ├─────────────────>│ 5. Generar pasos  │               │
  │                    │ {generate_ai:true,│    con IA         │               │
  │                    │  ai_context}      ├─────────────────>│               │
  │                    │                   │ Gemini API        │               │
  │                    │                   │<─────────────────┤               │
  │                    │                   │ [{step1}, ...]    │               │
  │                    │                   │                   │               │
  │                    │                   │ 6. Crear timeline │               │
  │                    │                   ├─────────────────────────────────>│
  │                    │                   │ INSERT timelines  │               │
  │                    │                   │ INSERT timeline_  │               │
  │                    │                   │ steps (múltiples) │               │
  │                    │                   │<─────────────────────────────────┤
  │                    │<─────────────────┤                   │               │
  │                    │ {timeline,steps}  │                   │               │
  │<───────────────────                   │                   │               │
  │ 7. Ver timeline   │                   │                   │               │
  │    con pasos      │                   │                   │               │
```

### Opción B: Manual

```
Usuario              Frontend            Backend           Database
  │                    │                   │                   │
  │ 1. Agregar paso   │                   │                   │
  │    manualmente    │                   │                   │
  ├──────────────────>│                   │                   │
  │ (título, desc)    │                   │                   │
  │                    │                   │                   │
  │ 2. + Agregar más  │                   │                   │
  ├──────────────────>│                   │                   │
  │                    │                   │                   │
  │ 3. Submit         │ POST /timeline/   │                   │
  │                    │ create            │                   │
  │                    ├─────────────────>│ INSERT timelines  │
  │                    │ {steps: [...]}    │ INSERT steps      │
  │                    │                   ├─────────────────>│
  │                    │                   │<─────────────────┤
  │                    │<─────────────────┤                   │
  │<───────────────────                   │                   │
  │ 4. Timeline creada│                   │                   │
```

---

## 🎨 Componentes Frontend

```
┌─────────────────────────────────────────────────────────────┐
│              CourseManagerPro.jsx                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  State:                                                      │
│  ├─ courses []                                              │
│  ├─ showCreateModal bool                                    │
│  ├─ formData {name, code, professor, icon, category, color} │
│  └─ editingCourse {}                                        │
│                                                              │
│  Components:                                                 │
│  ├─ IconSelector (15 iconos en grid)                       │
│  ├─ CategorySelector (8 categorías con emoji)              │
│  ├─ ColorSelector (9 colores con preview)                  │
│  └─ CourseCard (tarjeta con gradiente y botones)           │
│                                                              │
│  Functions:                                                  │
│  ├─ loadCourses()                                           │
│  ├─ handleCreateOrUpdate()                                  │
│  ├─ handleEdit(course)                                      │
│  └─ handleDelete(courseId)                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│           SyllabusAnalyzerPro.jsx                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  State:                                                      │
│  ├─ syllabusList []                                         │
│  ├─ selectedSyllabus {}                                     │
│  ├─ loading bool                                            │
│  └─ uploading bool                                          │
│                                                              │
│  Components:                                                 │
│  ├─ UploadPanel (drag & drop area)                         │
│  ├─ HistoryList (lateral con tarjetas)                     │
│  ├─ DetailsPanel (temas expandibles)                       │
│  └─ ProgressBar (barra visual)                             │
│                                                              │
│  Functions:                                                  │
│  ├─ loadSyllabusList()                                      │
│  ├─ handleFileUpload(file)                                  │
│  ├─ viewSyllabusDetails(id)                                 │
│  ├─ toggleTopicComplete(index)                              │
│  └─ deleteSyllabus(id)                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              TimelineCreator.jsx                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  State:                                                      │
│  ├─ timelines []                                            │
│  ├─ selectedTimeline {}                                     │
│  ├─ showCreateModal bool                                    │
│  ├─ formData {title, course_id, generate_with_ai, ...}     │
│  └─ manualSteps []                                          │
│                                                              │
│  Components:                                                 │
│  ├─ CreateModal (formulario completo)                      │
│  ├─ AIToggle (checkbox con input de contexto)              │
│  ├─ ManualStepsEditor (agregar/quitar pasos)               │
│  ├─ TimelineList (lateral con tarjetas)                    │
│  └─ TimelineDetails (pasos verticales con línea)           │
│                                                              │
│  Functions:                                                  │
│  ├─ loadTimelines()                                         │
│  ├─ handleCreateTimeline()                                  │
│  ├─ toggleStepComplete(timelineId, stepId)                 │
│  └─ deleteTimeline(id)                                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Modelos de Base de Datos

```python
# academic.py (ACTUALIZADO)
class AcademicCourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(50))              # ⭐ NEW
    professor = db.Column(db.String(150))
    schedule_info = db.Column(db.String(255))
    category = db.Column(db.String(50))          # ⭐ NEW
    icon = db.Column(db.String(50))              # ⭐ NEW
    color = db.Column(db.String(20))             # 🔄 UPDATED
    created_at = db.Column(db.DateTime)
    
    # Relationships
    tasks = db.relationship('AcademicTask', backref='course')
    syllabus_analyses = db.relationship('SyllabusAnalysis')  # ⭐ NEW

# syllabus.py (⭐ NUEVO)
class SyllabusAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('academic_courses.id'))
    file_path = db.Column(db.String(500))
    file_name = db.Column(db.String(255))
    course_info_json = db.Column(db.Text)        # JSON
    topics_json = db.Column(db.Text)             # JSON
    uploaded_at = db.Column(db.DateTime)
    
    # Methods
    def get_topics(self): return json.loads(self.topics_json)
    def set_topics(self, topics): self.topics_json = json.dumps(topics)
    def toggle_topic_complete(self, index): ...

# timeline.py (ACTUALIZADO)
class Timeline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('academic_courses.id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    end_date = db.Column(db.DateTime)            # ⭐ NEW
    steps_json = db.Column(db.Text)              # Compatibilidad
    
    # Relationships
    steps = db.relationship('TimelineStep', ...)  # ⭐ NEW

# timeline_step.py (⭐ NUEVO)
class TimelineStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timeline_id = db.Column(db.Integer, db.ForeignKey('timelines.id'))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    
    # Methods
    def toggle_complete(self): ...
```

---

## 🔌 API Endpoints

```
📚 CURSOS
├─ POST   /api/academic/course/create
│  Body: {user_id, name, code, professor, category, icon, color}
│  Response: {id, message, course}
│
├─ GET    /api/academic/user/{user_id}/courses
│  Response: {courses: [{id, name, code, icon, category, color}, ...]}
│
├─ PUT    /api/academic/course/{course_id}
│  Body: {name, code, professor, category, icon, color}
│  Response: {message, course}
│
└─ DELETE /api/academic/course/{course_id}
   Response: {message}

📄 SÍLABOS
├─ POST   /api/academic/course/{course_id}/upload-syllabus
│  Form: file (PDF), user_id
│  Response: {syllabus_id, syllabus_analysis, tasks_created}
│
├─ GET    /api/academic/user/{user_id}/syllabus-history
│  Response: {syllabus_list: [{id, course_name, topics, ...}, ...]}
│
├─ GET    /api/academic/syllabus/{syllabus_id}
│  Response: {id, course_name, topics, course_info, ...}
│
├─ PUT    /api/academic/syllabus/{syllabus_id}/topic/{topic_index}/toggle
│  Response: {message, syllabus}
│
└─ DELETE /api/academic/syllabus/{syllabus_id}
   Response: {message}

🕒 LÍNEAS DE TIEMPO
├─ POST   /api/timeline/create
│  Body: {user_id, course_id, title, generate_with_ai, steps}
│  Response: {timeline: {id, title, steps, ...}}
│
├─ GET    /api/timeline/user/{user_id}
│  Query: ?course_id=5&visible_only=true
│  Response: {timelines: [{id, title, steps, progress}, ...]}
│
├─ PUT    /api/timeline/{timeline_id}/step/{step_id}/toggle
│  Response: {message, timeline}
│
└─ DELETE /api/timeline/{timeline_id}
   Response: {message}
```

---

## 🎯 Flujo Completo de Usuario

```
1. Login → /login
   ↓
2. Dashboard → /analisis
   ↓
3. [GESTIÓN] Crear Curso
   ├─ Elegir icono 🧠
   ├─ Elegir categoría 🔢
   ├─ Elegir color 🟣
   └─ Guardar ✅
   ↓
4. [SÍLABOS] Cargar PDF
   ├─ Seleccionar curso
   ├─ Subir archivo
   ├─ Esperar análisis IA 🤖
   └─ Ver en historial ✅
   ↓
5. [SÍLABOS] Marcar temas
   ├─ Click en análisis
   ├─ Ver temas
   ├─ Click en tema → ✅
   └─ Ver progreso 📊
   ↓
6. [TIMELINE] Crear plan
   ├─ Opción A: IA
   │  ├─ Activar checkbox
   │  ├─ Escribir contexto
   │  └─ IA genera pasos 🤖
   └─ Opción B: Manual
      ├─ Agregar pasos
      └─ Editar detalles
   ↓
7. [TIMELINE] Seguir progreso
   ├─ Ver lista de planes
   ├─ Click en plan
   ├─ Click en paso → ✅
   └─ Ver progreso visual 📊
   ↓
8. [PROYECTOS] Cronómetro
   ↓
9. [EVOLUCIÓN] Estadísticas
```

---

## 🔐 Seguridad y Validación

```
Frontend Validation:
├─ Campos requeridos marcados con *
├─ Validación de tipos (email, número, fecha)
├─ Límites de caracteres
├─ Formatos de archivo (PDF only)
└─ Tamaño máximo (10MB)

Backend Validation:
├─ Verificar user_id existe
├─ Verificar permisos (user solo ve sus datos)
├─ Sanitizar inputs (SQL injection prevention)
├─ Validar formatos de archivo
├─ Manejo de errores con try/catch
└─ Rollback en caso de error

Database Constraints:
├─ NOT NULL en campos críticos
├─ FOREIGN KEY constraints
├─ CASCADE DELETE para eliminar relacionados
├─ INDEXES para búsquedas rápidas
└─ VARCHAR límites para prevenir overflow
```

---

**Arquitectura diseñada para ser escalable, mantenible y user-friendly 🚀**
