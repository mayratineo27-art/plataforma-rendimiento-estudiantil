# 🎯 Líneas de Tiempo por Tema de Curso

## 📋 Descripción General

Esta nueva funcionalidad permite a los usuarios crear **líneas de tiempo específicas para temas de cualquier curso**, sin necesidad de estar vinculadas a proyectos. Es perfecta para organizar el estudio de temas específicos de manera independiente.

## ✨ Características Principales

### 1. **Creación de Líneas de Tiempo por Tema**
- Crear líneas de tiempo enfocadas en temas específicos de un curso
- No requiere crear un proyecto primero
- Tipo de timeline: `free` (libre de proyectos)
- Campo especial `course_topic` para especificar el tema

### 2. **Generación Automática con IA**
- Opción de generar pasos de estudio automáticamente usando IA
- Basado en el tema del curso especificado
- Pasos personalizados según el contexto del tema

### 3. **Gestión Manual de Pasos**
- Opción de añadir pasos manualmente si no se desea usar IA
- Control total sobre el contenido de cada paso
- Posibilidad de editar y personalizar

### 4. **Seguimiento de Progreso**
- Marcar pasos como completados
- Barra de progreso visual
- Estadísticas de avance
- Fecha límite opcional

## 🚀 Uso

### Backend - Endpoint Nuevo

```bash
POST /api/timeline/topic/create
```

**Body de la petición:**
```json
{
  "user_id": 1,
  "course_id": 5,
  "course_topic": "Integrales por partes",
  "title": "Dominar integrales por partes",  // Opcional
  "description": "Plan de estudio para...",   // Opcional
  "end_date": "2025-12-31",                   // Opcional
  "generate_with_ai": true,                   // true o false
  "steps": [                                   // Solo si generate_with_ai es false
    {
      "title": "Revisar teoría básica",
      "description": "Estudiar definiciones",
      "order": 1
    }
  ]
}
```

**Respuesta exitosa:**
```json
{
  "message": "Línea de tiempo de tema creada exitosamente",
  "timeline": {
    "id": 42,
    "user_id": 1,
    "course_id": 5,
    "course_name": "Cálculo Integral",
    "project_id": null,
    "title": "Dominar integrales por partes",
    "course_topic": "Integrales por partes",
    "timeline_type": "free",
    "progress": 0,
    "steps": [...]
  }
}
```

### Frontend - Componentes Nuevos

#### 1. `TopicTimelineCreator.jsx`
Componente para crear nuevas líneas de tiempo de temas.

**Uso:**
```jsx
import TopicTimelineCreator from './components/Timeline/TopicTimelineCreator';

function MyComponent() {
  return <TopicTimelineCreator userId={1} />;
}
```

**Características:**
- Formulario intuitivo para crear timelines
- Selector de curso
- Campo para especificar el tema
- Toggle para generar con IA
- Editor de pasos manuales
- Vista previa de timelines existentes

#### 2. `TopicTimelineView.jsx`
Componente para visualizar y gestionar líneas de tiempo de temas.

**Uso:**
```jsx
import TopicTimelineView from './components/Timeline/TopicTimelineView';

function MyComponent() {
  return <TopicTimelineView userId={1} courseId={5} />; // courseId opcional
}
```

**Características:**
- Lista de todas las líneas de tiempo de temas
- Filtros por estado (todos, en progreso, completados)
- Toggle de visibilidad
- Marcar pasos como completados
- Eliminar timelines
- Vista expandible con todos los pasos

## 🗄️ Cambios en la Base de Datos

### Modelo `Timeline` Extendido

Se añadió la columna:
```sql
course_topic VARCHAR(300) NULL COMMENT 'Tema específico del curso para timelines de tipo free'
```

El enum `timeline_type` ya incluía el valor `'free'`:
```python
timeline_type = db.Column(
    db.Enum('academic', 'course', 'project', 'free', name='timeline_type'),
    default='project'
)
```

### Script de Migración

Ejecutar el script para añadir la columna:
```bash
cd backend
python add_course_topic_column.py
```

## 📖 Ejemplos de Uso

### Ejemplo 1: Crear Timeline con IA

```javascript
const response = await axios.post('http://localhost:5000/api/timeline/topic/create', {
  user_id: 1,
  course_id: 5,
  course_topic: "Revolución Francesa",
  generate_with_ai: true,
  end_date: "2025-12-20"
});
```

### Ejemplo 2: Crear Timeline con Pasos Manuales

```javascript
const response = await axios.post('http://localhost:5000/api/timeline/topic/create', {
  user_id: 1,
  course_id: 3,
  course_topic: "ADN y ARN",
  title: "Comprender estructura del ADN",
  description: "Estudio detallado de ácidos nucleicos",
  generate_with_ai: false,
  steps: [
    {
      title: "Leer capítulo 5 del libro",
      description: "Páginas 120-150",
      order: 1
    },
    {
      title: "Ver video explicativo",
      description: "Canal de YouTube: BiologíaFácil",
      order: 2
    },
    {
      title: "Hacer ejercicios de práctica",
      order: 3
    }
  ]
});
```

## 🎨 Interfaz de Usuario

### Características Visuales

1. **Diseño moderno con gradientes**
   - Colores morados e índigos
   - Barras de progreso animadas
   - Iconos descriptivos

2. **Tarjetas de timeline**
   - Header con color según progreso
   - Información del curso y tema
   - Barra de progreso visual
   - Lista de próximos pasos

3. **Modal de creación**
   - Formulario paso a paso
   - Toggle para IA
   - Editor de pasos manuales
   - Validación en tiempo real

## 🔧 Integración con Sistema Existente

### Compatibilidad
- ✅ Compatible con timelines de proyectos existentes
- ✅ Usa los mismos endpoints base de timeline
- ✅ Se integra con el sistema de cursos académicos
- ✅ Respeta el sistema de visibilidad y permisos

### Diferencias con Timeline de Proyectos
- **Timeline de Proyecto:** `timeline_type='project'`, requiere `project_id`
- **Timeline de Tema:** `timeline_type='free'`, requiere `course_topic`, `project_id=null`

## 📊 Casos de Uso

1. **Preparación para exámenes**
   - Crear timeline para cada tema del examen
   - Marcar progreso de estudio
   - Establecer fechas límite

2. **Estudio independiente**
   - Organizar temas de interés personal
   - No vinculado a proyectos específicos
   - Flexibilidad total

3. **Repaso de temas específicos**
   - Repasar temas difíciles
   - Líneas de tiempo cortas y enfocadas
   - Seguimiento detallado

## 🚦 Estado de Implementación

- ✅ Backend: Modelo extendido
- ✅ Backend: Endpoint `/api/timeline/topic/create`
- ✅ Backend: Script de migración
- ✅ Frontend: Componente `TopicTimelineCreator.jsx`
- ✅ Frontend: Componente `TopicTimelineView.jsx`
- ✅ Documentación completa

## 📝 Notas Adicionales

- El campo `course_topic` es obligatorio para timelines de tipo 'free'
- Si no se proporciona `title`, se genera automáticamente como "Línea de tiempo: {topic}"
- La IA genera pasos contextualizados al tema específico
- Los timelines de temas pueden tener fecha límite opcional
- Se pueden ocultar/mostrar igual que los timelines de proyectos

## 🔜 Mejoras Futuras Posibles

1. Estadísticas de temas estudiados por curso
2. Recomendaciones de temas relacionados
3. Compartir timelines de temas con otros usuarios
4. Plantillas predefinidas por materia
5. Integración con sistema de evaluación

---

**Fecha de implementación:** 1 de Diciembre, 2025
**Versión:** 1.0.0
