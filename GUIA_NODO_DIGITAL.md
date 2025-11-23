# 🚀 Guía Rápida - Nuevas Funcionalidades Nodo Digital

## 📋 Índice
1. [Instalación y Configuración](#instalación)
2. [Sistema de Cronómetros](#cronómetros)
3. [Exportación de Contenido](#exportación)
4. [Búsqueda y Filtros](#búsqueda)
5. [Procesamiento de Sílabos](#sílabos)
6. [Resolución de Problemas](#problemas)

---

## 🔧 Instalación y Configuración {#instalación}

### 1. Instalar Dependencias del Backend

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Crea o edita el archivo `.env` en la carpeta `backend/`:

```env
# Base de datos
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=rendimiento_estudiantil

# API de Google Gemini (obligatorio para IA)
GEMINI_API_KEY=tu_api_key_aquí

# Flask
SECRET_KEY=tu_secret_key_seguro
FLASK_DEBUG=True
```

### 3. Crear la Tabla de Cronómetros

```bash
cd backend
python create_timer_table.py
```

### 4. Verificar la Instalación

```bash
cd backend
python test_nodo_digital.py
```

Deberías ver:
```
✅ VERIFICACIÓN COMPLETA
🚀 El Nodo Digital está listo para usar!
```

### 5. Iniciar los Servidores

**Backend:**
```bash
cd backend
python run.py
```

**Frontend:**
```bash
cd frontend
npm start
```

---

## ⏱️ Sistema de Cronómetros {#cronómetros}

### Características

- ⏱️ Cronómetro persistente que se guarda en la base de datos
- 📚 Asociable a cursos específicos
- 📝 Asociable a tareas específicas
- 💾 Guarda automáticamente el tiempo acumulado
- 📊 Estadísticas de tiempo de estudio

### Uso en la Interfaz

1. **Iniciar/Pausar:**
   - Click en el botón ▶️ para iniciar
   - Click en ⏸️ para pausar

2. **Guardar Tiempo:**
   - Click en 💾 mientras el cronómetro está corriendo
   - El tiempo se guarda en la base de datos

3. **Reiniciar:**
   - Click en 🔄 para volver a cero
   - Confirma la acción (el tiempo guardado se pierde)

### API del Cronómetro

```javascript
// Iniciar cronómetro
POST /api/timer/start
{
  "user_id": 1,
  "course_id": 5,  // opcional
  "task_id": 12    // opcional
}

// Detener cronómetro
PUT /api/timer/stop/:timer_id

// Reiniciar cronómetro
PUT /api/timer/reset/:timer_id

// Obtener timers del usuario
GET /api/timer/user/:user_id?course_id=5

// Estadísticas
GET /api/timer/stats/:user_id
```

### Ejemplo de Uso con Fetch

```javascript
// Iniciar cronómetro para un curso
const startTimer = async (courseId) => {
  const response = await fetch('/api/timer/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: 1,
      course_id: courseId,
      session_name: 'Sesión de estudio'
    })
  });
  const data = await response.json();
  console.log('Timer iniciado:', data.timer);
};

// Obtener estadísticas
const getStats = async (userId) => {
  const response = await fetch(`/api/timer/stats/${userId}`);
  const stats = await response.json();
  console.log(`Total estudiado: ${stats.total_formatted}`);
};
```

---

## 📥 Exportación de Contenido {#exportación}

### Mapas Mentales

Los mapas mentales se pueden exportar en dos formatos:

**1. JSON (Estructura completa):**
```javascript
// Click en el botón 📄 en la interfaz
// O usa esta función:
const exportAsJSON = (mindmapData) => {
  const dataStr = JSON.stringify(mindmapData, null, 2);
  const dataBlob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(dataBlob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `mindmap-${Date.now()}.json`;
  link.click();
};
```

**2. TXT (Formato legible):**
```javascript
// Click en el botón 📥 en la interfaz
```

### Resúmenes

Los resúmenes se exportan como archivos de texto plano:

```javascript
// Click en el botón 📥
// El archivo contendrá el resumen completo en formato Markdown
```

### Historial Automático

Todas las generaciones se guardan automáticamente en `localStorage`:

```javascript
// Acceder al historial
const history = JSON.parse(localStorage.getItem('study_tools_history'));

// Estructura:
[
  {
    id: 1234567890,
    type: 'mindmap' | 'summary',
    input: 'Texto original...',
    output: {...} | 'Resumen...',
    course: 'Nombre del curso',
    timestamp: '2025-11-21T...'
  }
]
```

---

## 🔍 Búsqueda y Filtros {#búsqueda}

### Búsqueda Global

La barra de búsqueda en el header busca en:
- ✅ Nombres de cursos
- ✅ Nombres de profesores
- ✅ Títulos de tareas
- ✅ Nombres de cursos asociados a tareas

```javascript
// La búsqueda es en tiempo real y case-insensitive
const filteredCourses = courses.filter(course =>
  course.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
  (course.professor && course.professor.toLowerCase().includes(searchTerm.toLowerCase()))
);
```

### Filtros de Tareas

**Por Prioridad:**
- Todas
- Crítica (🔴)
- Alta (🟠)
- Media (🟡)
- Baja (🟢)

**Por Estado:**
- Todos
- Pendiente
- En progreso
- Completada

```javascript
const filteredTasks = tasks.filter(task => {
  const matchesSearch = task.title.toLowerCase().includes(searchTerm.toLowerCase());
  const matchesPriority = filterPriority === 'all' || task.priority === filterPriority;
  const matchesStatus = filterStatus === 'all' || task.status === filterStatus;
  return matchesSearch && matchesPriority && matchesStatus;
});
```

---

## 📚 Procesamiento de Sílabos {#sílabos}

### Cómo Funciona

1. **Sube un PDF del sílabo** en cualquier curso
2. El sistema **extrae el texto** con PyPDF2
3. **Gemini AI analiza** el contenido
4. **Extrae automáticamente:**
   - Tareas y proyectos
   - Fechas de entrega
   - Prioridades estimadas
   - Tipos de actividad (tarea, examen, proyecto, etc.)

### Ejemplo de Análisis

**Input (Sílabo):**
```
Cronograma:
- Semana 3: Ensayo sobre la Revolución Francesa (15/12/2025)
- Semana 5: Examen Parcial 1 (20/12/2025)
- Semana 8: Proyecto Final - Análisis histórico (10/01/2026)
```

**Output (Tareas creadas):**
```json
[
  {
    "title": "Ensayo sobre la Revolución Francesa",
    "type": "tarea",
    "due_date": "2025-12-15",
    "priority": "alta"
  },
  {
    "title": "Examen Parcial 1",
    "type": "examen",
    "due_date": "2025-12-20",
    "priority": "critica"
  },
  {
    "title": "Proyecto Final - Análisis histórico",
    "type": "proyecto",
    "due_date": "2026-01-10",
    "priority": "critica"
  }
]
```

### API

```bash
POST /api/academic/course/:course_id/upload-syllabus
Content-Type: multipart/form-data

file: [PDF del sílabo]
user_id: 1
```

**Respuesta:**
```json
{
  "message": "Sílabo procesado exitosamente",
  "tasks_created": 3,
  "summary": "Se extrajeron 3 tareas del sílabo"
}
```

---

## 🐛 Resolución de Problemas {#problemas}

### Error: "ModuleNotFoundError: No module named 'flask'"

```bash
cd backend
pip install -r requirements.txt
```

### Error: "Table study_timers doesn't exist"

```bash
cd backend
python create_timer_table.py
```

### El cronómetro no guarda el tiempo

**Verifica:**
1. Que el backend esté corriendo (`python run.py`)
2. Que no haya errores en la consola del navegador (F12)
3. Que la tabla existe:
   ```bash
   python -c "from app import create_app, db; app=create_app(); app.app_context().push(); from sqlalchemy import inspect; print(inspect(db.engine).get_table_names())"
   ```

### Error: "La API Key de Gemini no está configurada"

**Solución:**
1. Obtén una API Key en https://makersuite.google.com/app/apikey
2. Agrégala a tu archivo `.env`:
   ```env
   GEMINI_API_KEY=AIza...tu_key_aquí
   ```
3. Reinicia el backend

### El procesamiento de sílabos falla

**Causas comunes:**
1. **PDF con imágenes:** El sistema solo extrae texto. PDFs escaneados no funcionan.
2. **API Key inválida:** Verifica tu `GEMINI_API_KEY`
3. **Límite de API:** Gemini tiene límites de uso gratuitos

**Solución para PDFs escaneados:**
- Usa herramientas OCR online primero
- O mejora el extractor para usar OCR (requiere tesseract)

### Las búsquedas no funcionan

**Verifica:**
1. Que el `searchTerm` se esté actualizando en el estado
2. Que los datos existan (`courses.length > 0`)
3. Que no haya errores en la consola

### Problemas de CORS

Si ves errores de CORS en la consola:

**Backend (`app/__init__.py`):**
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:3001"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

---

## 📞 Soporte

Si encuentras problemas:

1. **Verifica los logs del backend:** Revisa la terminal donde corre `python run.py`
2. **Verifica la consola del navegador:** Presiona F12 y revisa la pestaña Console
3. **Ejecuta el test de verificación:**
   ```bash
   cd backend
   python test_nodo_digital.py
   ```

---

## 🎯 Próximos Pasos

1. **Explora las herramientas IA:**
   - Genera mapas mentales
   - Crea resúmenes
   - Exporta los resultados

2. **Usa el cronómetro:**
   - Mide tu tiempo de estudio
   - Revisa las estadísticas

3. **Sube sílabos:**
   - Deja que la IA extraiga tus tareas
   - Organiza tu semestre automáticamente

4. **Personaliza:**
   - Cambia los colores de los cursos
   - Ajusta las prioridades de las tareas
   - Filtra por estado y prioridad

---

## ✨ ¡Disfruta del Nodo Digital mejorado!
