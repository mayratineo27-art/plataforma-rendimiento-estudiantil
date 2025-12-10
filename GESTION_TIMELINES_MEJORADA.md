# Gestión de Líneas de Tiempo - Actualización

## 📅 Fecha: Diciembre 2, 2025

## 🎯 Mejoras Implementadas

### 1. Líneas de Tiempo Flexibles (Con o Sin Curso)

Ahora es posible crear líneas de tiempo de dos formas:

#### **Con Curso Asociado**
- Vinculadas a un curso académico específico
- Incluye el `course_id` en la creación
- Ideal para seguimiento de temas de cursos

#### **Sin Curso (Libres)**
- No requieren estar asociadas a un curso
- Perfectas para estudio personal o temas independientes
- El `course_id` es completamente opcional

### 2. Gestión Completa del Historial

Se agregaron endpoints para administrar el historial de líneas de tiempo:

#### **Listar Historial con Filtros**
```http
GET /api/academic/timelines/history
```

**Query Parameters:**
- `user_id` (requerido): ID del usuario
- `course_id` (opcional): Filtrar por curso específico
- `timeline_type` (opcional): Filtrar por tipo (academic, course, project, free)
- `is_completed` (opcional): Filtrar por completadas (true/false)
- `limit` (opcional): Cantidad máxima de resultados (default: 50)

**Ejemplo:**
```javascript
// Obtener todas las líneas de tiempo de un usuario
GET /api/academic/timelines/history?user_id=1

// Obtener solo las completadas de un curso
GET /api/academic/timelines/history?user_id=1&course_id=5&is_completed=true

// Obtener líneas de tiempo libres (sin curso)
GET /api/academic/timelines/history?user_id=1&timeline_type=free
```

#### **Obtener Detalle de una Línea de Tiempo**
```http
GET /api/academic/timelines/<timeline_id>
```

**Respuesta:**
```json
{
  "id": 1,
  "user_id": 1,
  "course_id": null,
  "title": "Aprender Python",
  "description": "Línea de tiempo libre sobre Aprender Python",
  "timeline_type": "free",
  "steps": [...],
  "is_completed": false,
  "progress": 45.5,
  "created_at": "2025-12-02T20:00:00"
}
```

#### **Eliminar del Historial (Soft Delete)**
```http
DELETE /api/academic/timelines/<timeline_id>
```

- Marca la línea de tiempo como no visible
- Los datos se mantienen en la base de datos
- Reversible (se puede reactivar modificando `is_visible`)

#### **Eliminar Permanentemente**
```http
DELETE /api/academic/timelines/<timeline_id>/permanent
```

- Elimina completamente el registro de la base de datos
- **No reversible** - usar con precaución

#### **Limpiar Líneas de Tiempo Antiguas**
```http
POST /api/academic/timelines/cleanup
```

**Body:**
```json
{
  "user_id": 1,
  "days_old": 90,              // Eliminar con más de 90 días (default)
  "delete_completed": false,   // Eliminar solo completadas
  "permanent": false           // false = soft delete, true = eliminación permanente
}
```

**Respuesta:**
```json
{
  "message": "5 líneas de tiempo ocultadas",
  "count": 5
}
```

### 3. Crear Línea de Tiempo Mejorada

**Endpoint actualizado:**
```http
POST /api/academic/tools/timeline
```

**Body:**
```json
{
  "topic": "Fundamentos de React",
  "type": "free",              // academic, course, project, free
  "user_id": 1,
  "course_id": null,           // Ahora es opcional - puede ser null
  "project_id": null,          // También opcional
  "save": true
}
```

**Características:**
- ✅ `course_id` es completamente opcional
- ✅ Crea líneas de tiempo libres sin curso
- ✅ Descripción automática según el contexto
- ✅ Tipo por defecto: `free`

## 🔧 Cambios Técnicos

### Base de Datos
- **Columna `course_id`**: Ahora permite valores NULL
- **Script de migración**: `fix_timeline_course_nullable.py`
- **Estado**: ✅ Ejecutado exitosamente

### Modelo Timeline
```python
course_id = db.Column(db.Integer, db.ForeignKey('academic_courses.id'), nullable=True)
course_topic = db.Column(db.String(300), nullable=True)  # Tema cuando no hay curso
```

### Soft Delete vs Hard Delete
- **Soft Delete**: `is_visible = False` (recomendado)
- **Hard Delete**: Eliminación permanente del registro
- Permite recuperar datos si es necesario

## 📊 Casos de Uso

### Caso 1: Estudiante Organizado
```javascript
// 1. Crear línea de tiempo para un curso
POST /api/academic/tools/timeline
{
  "topic": "Química Orgánica - Capítulo 3",
  "type": "course",
  "user_id": 1,
  "course_id": 5,
  "save": true
}

// 2. Ver todas las líneas de tiempo del curso
GET /api/academic/timelines/history?user_id=1&course_id=5

// 3. Limpiar las completadas cada mes
POST /api/academic/timelines/cleanup
{
  "user_id": 1,
  "days_old": 30,
  "delete_completed": true,
  "permanent": false
}
```

### Caso 2: Aprendizaje Libre
```javascript
// Crear timeline sin curso
POST /api/academic/tools/timeline
{
  "topic": "Aprender a tocar guitarra",
  "type": "free",
  "user_id": 1,
  "course_id": null,  // Sin curso asociado
  "save": true
}

// Ver solo timelines libres
GET /api/academic/timelines/history?user_id=1&timeline_type=free
```

### Caso 3: Gestión de Historial
```javascript
// Ver últimas 10 líneas de tiempo
GET /api/academic/timelines/history?user_id=1&limit=10

// Eliminar una específica (soft delete)
DELETE /api/academic/timelines/123

// Limpiar todo lo anterior a 60 días
POST /api/academic/timelines/cleanup
{
  "user_id": 1,
  "days_old": 60,
  "permanent": false
}
```

## 🎨 Integración Frontend

### Componente de Creación
```jsx
function CreateTimeline() {
  const [formData, setFormData] = useState({
    topic: '',
    type: 'free',
    course_id: null,  // Opcional
    save: true
  });

  const handleSubmit = async () => {
    const response = await fetch('/api/academic/tools/timeline', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...formData,
        user_id: currentUser.id
      })
    });
    
    const data = await response.json();
    // Manejar respuesta
  };
}
```

### Componente de Historial
```jsx
function TimelineHistory() {
  const [filters, setFilters] = useState({
    course_id: null,
    timeline_type: 'all',
    is_completed: null
  });

  const loadHistory = async () => {
    const params = new URLSearchParams({
      user_id: currentUser.id,
      ...(filters.course_id && { course_id: filters.course_id }),
      ...(filters.timeline_type !== 'all' && { timeline_type: filters.timeline_type }),
      ...(filters.is_completed !== null && { is_completed: filters.is_completed })
    });

    const response = await fetch(`/api/academic/timelines/history?${params}`);
    const data = await response.json();
    return data.timelines;
  };

  const deleteTimeline = async (id, permanent = false) => {
    const url = permanent 
      ? `/api/academic/timelines/${id}/permanent`
      : `/api/academic/timelines/${id}`;
    
    await fetch(url, { method: 'DELETE' });
    loadHistory(); // Recargar
  };
}
```

## ⚠️ Consideraciones

### Rendimiento
- El límite por defecto de 50 resultados previene sobrecarga
- Usa paginación si necesitas más resultados
- Los índices en `created_at` y `user_id` optimizan queries

### Seguridad
- ✅ Valida que `user_id` coincida con el usuario autenticado
- ✅ No permite eliminar timelines de otros usuarios
- ✅ Soft delete por defecto protege contra pérdida accidental

### Mantenimiento
- Programa limpieza automática cada 30-90 días
- Usa soft delete para poder auditar
- Considera hard delete solo para cumplimiento (GDPR)

## 🚀 Próximos Pasos

1. **Implementar en Frontend**:
   - Agregar toggle "Con curso / Sin curso"
   - Vista de historial con filtros
   - Botón de limpiar historial antiguo

2. **Notificaciones**:
   - Alertar cuando hay muchas timelines sin completar
   - Recordatorios de limpieza de historial

3. **Analytics**:
   - Dashboard de progreso de timelines
   - Estadísticas de uso por tipo

## 📝 Archivos Modificados

- ✅ `backend/app/routes/academic_routes.py` - Endpoints actualizados
- ✅ `backend/app/models/timeline.py` - Ya tenía `nullable=True`
- ✅ `backend/fix_timeline_course_nullable.py` - Script de migración
- ✅ Base de datos - Columna actualizada

---

## 💡 Ejemplo de Flujo Completo

```javascript
// 1. Usuario crea una timeline sin curso
const response1 = await createTimeline({
  topic: "Aprender TypeScript",
  type: "free",
  course_id: null,
  save: true
});

// 2. Trabaja en ella durante días...

// 3. Revisa su historial
const history = await getTimelineHistory({
  user_id: 1,
  limit: 20
});

// 4. Encuentra muchas antiguas, decide limpiar
const cleanup = await cleanupTimelines({
  user_id: 1,
  days_old: 60,
  delete_completed: true
});

console.log(cleanup.message); // "15 líneas de tiempo ocultadas"
```

## 🎉 Beneficios

- ✅ Mayor flexibilidad en la creación
- ✅ Mejor organización del historial
- ✅ Prevención de saturación de datos
- ✅ Control total sobre qué mantener
- ✅ Recuperación de datos con soft delete
