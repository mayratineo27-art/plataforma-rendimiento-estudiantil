# 💻 Ejemplos de Código - Nodo Digital

## 📋 Tabla de Contenidos
1. [Uso del Cronómetro](#cronometro)
2. [Herramientas IA](#ia)
3. [Gestión de Cursos](#cursos)
4. [Gestión de Tareas](#tareas)
5. [Componentes React](#react)

---

## ⏱️ Uso del Cronómetro {#cronometro}

### Ejemplo 1: Cronómetro Simple

```jsx
import Stopwatch from '../components/Stopwatch';

function MyComponent() {
  const userId = 1;
  
  return (
    <div>
      <h2>Mi Sesión de Estudio</h2>
      <Stopwatch userId={userId} />
    </div>
  );
}
```

### Ejemplo 2: Cronómetro Asociado a un Curso

```jsx
import Stopwatch from '../components/Stopwatch';

function CourseStudySession({ courseId }) {
  const userId = 1;
  
  return (
    <div className="study-session">
      <h3>Estudiando: Cálculo I</h3>
      <Stopwatch 
        userId={userId} 
        courseId={courseId} 
      />
    </div>
  );
}
```

### Ejemplo 3: Cronómetro para una Tarea Específica

```jsx
import Stopwatch from '../components/Stopwatch';

function TaskTimer({ task }) {
  return (
    <div className="task-timer">
      <h4>{task.title}</h4>
      <p>Curso: {task.course_name}</p>
      <Stopwatch 
        userId={1} 
        courseId={task.course_id}
        taskId={task.id}
      />
    </div>
  );
}
```

### Ejemplo 4: Obtener Estadísticas de Tiempo

```javascript
// Función para obtener estadísticas
async function getStudyStats(userId) {
  try {
    const response = await fetch(`/api/timer/stats/${userId}`);
    const stats = await response.json();
    
    console.log('Total de tiempo:', stats.total_formatted);
    console.log('Sesiones:', stats.total_sessions);
    console.log('Por curso:', stats.course_stats);
    
    return stats;
  } catch (error) {
    console.error('Error obteniendo estadísticas:', error);
  }
}

// Uso
getStudyStats(1).then(stats => {
  console.log(`Has estudiado ${stats.total_formatted} en total`);
});
```

### Ejemplo 5: Dashboard de Estadísticas

```jsx
import { useEffect, useState } from 'react';
import { Clock, TrendingUp } from 'lucide-react';

function StudyStatsDashboard({ userId }) {
  const [stats, setStats] = useState(null);
  
  useEffect(() => {
    fetch(`/api/timer/stats/${userId}`)
      .then(res => res.json())
      .then(data => setStats(data));
  }, [userId]);
  
  if (!stats) return <div>Cargando...</div>;
  
  return (
    <div className="stats-dashboard">
      <div className="stat-card">
        <Clock size={24} />
        <h3>Tiempo Total</h3>
        <p className="big">{stats.total_formatted}</p>
      </div>
      
      <div className="stat-card">
        <TrendingUp size={24} />
        <h3>Sesiones</h3>
        <p className="big">{stats.total_sessions}</p>
      </div>
      
      <div className="course-breakdown">
        <h3>Por Curso</h3>
        {Object.entries(stats.course_stats).map(([course, seconds]) => {
          const hours = Math.floor(seconds / 3600);
          const mins = Math.floor((seconds % 3600) / 60);
          return (
            <div key={course} className="course-stat">
              <span>{course}</span>
              <span>{hours}h {mins}m</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
```

---

## 🧠 Herramientas IA {#ia}

### Ejemplo 1: Generar Mapa Mental

```javascript
async function generateMindMap(text, courseName = 'General') {
  try {
    const response = await fetch('/api/academic/tools/mindmap', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: text,
        context: `Curso de ${courseName}`
      })
    });
    
    const data = await response.json();
    return data.mindmap;
  } catch (error) {
    console.error('Error generando mapa:', error);
    throw error;
  }
}

// Uso
const mindmap = await generateMindMap(
  'La Revolución Francesa fue un conflicto social...',
  'Historia Mundial'
);

console.log(mindmap);
// {
//   root: "Revolución Francesa",
//   children: [
//     { name: "Causas", children: [...] },
//     { name: "Consecuencias", children: [...] }
//   ]
// }
```

### Ejemplo 2: Generar Resumen

```javascript
async function generateSummary(text) {
  try {
    const response = await fetch('/api/academic/tools/summary', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    
    const data = await response.json();
    return data.summary;
  } catch (error) {
    console.error('Error generando resumen:', error);
    throw error;
  }
}

// Uso
const summary = await generateSummary(
  'La teoría de la relatividad de Einstein revolucionó nuestra comprensión...'
);

console.log(summary);
```

### Ejemplo 3: Componente de Generador IA

```jsx
import { useState } from 'react';
import { Brain, Download } from 'lucide-react';

function AIGenerator({ type = 'mindmap', courseId = null }) {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const generate = async () => {
    setLoading(true);
    try {
      const endpoint = type === 'mindmap' 
        ? '/api/academic/tools/mindmap'
        : '/api/academic/tools/summary';
      
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, context: 'General' })
      });
      
      const data = await response.json();
      setResult(type === 'mindmap' ? data.mindmap : data.summary);
    } catch (error) {
      alert('Error generando contenido');
    } finally {
      setLoading(false);
    }
  };
  
  const exportResult = () => {
    const blob = new Blob([JSON.stringify(result, null, 2)], {
      type: 'application/json'
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${type}-${Date.now()}.json`;
    link.click();
  };
  
  return (
    <div className="ai-generator">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Ingresa el texto..."
        rows={10}
      />
      
      <button onClick={generate} disabled={loading || !text}>
        <Brain size={18} />
        {loading ? 'Generando...' : 'Generar'}
      </button>
      
      {result && (
        <div className="result-panel">
          <button onClick={exportResult}>
            <Download size={18} /> Exportar
          </button>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
```

### Ejemplo 4: Procesar Sílabo

```javascript
async function uploadSyllabus(courseId, file, userId) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('user_id', userId);
  
  try {
    const response = await fetch(
      `/api/academic/course/${courseId}/upload-syllabus`,
      { method: 'POST', body: formData }
    );
    
    const data = await response.json();
    
    if (response.ok) {
      alert(`✅ ${data.tasks_created} tareas creadas automáticamente`);
      return data;
    } else {
      alert(`Error: ${data.error}`);
    }
  } catch (error) {
    console.error('Error subiendo sílabo:', error);
  }
}

// Uso en un componente
function SyllabusUploader({ courseId }) {
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      uploadSyllabus(courseId, file, 1);
    } else {
      alert('Por favor selecciona un archivo PDF');
    }
  };
  
  return (
    <div>
      <input
        type="file"
        accept=".pdf"
        onChange={handleFileChange}
      />
    </div>
  );
}
```

---

## 📚 Gestión de Cursos {#cursos}

### Ejemplo 1: Crear Curso

```javascript
async function createCourse(courseData, userId) {
  try {
    const response = await fetch('/api/academic/courses', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        name: courseData.name,
        professor: courseData.professor,
        schedule_info: courseData.schedule,
        color: courseData.color || '#3B82F6'
      })
    });
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error creando curso:', error);
  }
}

// Uso
const newCourse = await createCourse({
  name: 'Cálculo Diferencial',
  professor: 'Dr. García',
  schedule: 'Lun-Mie-Vie 10:00-12:00',
  color: '#10B981'
}, 1);
```

### Ejemplo 2: Actualizar Curso

```javascript
async function updateCourse(courseId, updates) {
  try {
    const response = await fetch(`/api/academic/course/${courseId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates)
    });
    
    const data = await response.json();
    return data.course;
  } catch (error) {
    console.error('Error actualizando curso:', error);
  }
}

// Uso
await updateCourse(5, {
  professor: 'Dr. Nuevo Profesor',
  schedule_info: 'Mar-Jue 14:00-16:00'
});
```

### Ejemplo 3: Eliminar Curso

```javascript
async function deleteCourse(courseId) {
  if (!confirm('¿Eliminar este curso y todas sus tareas?')) {
    return;
  }
  
  try {
    const response = await fetch(`/api/academic/course/${courseId}`, {
      method: 'DELETE'
    });
    
    if (response.ok) {
      alert('Curso eliminado');
      return true;
    }
  } catch (error) {
    console.error('Error eliminando curso:', error);
  }
}
```

### Ejemplo 4: Obtener Dashboard del Usuario

```javascript
async function getUserDashboard(userId) {
  try {
    const response = await fetch(`/api/academic/user/${userId}/dashboard`);
    const data = await response.json();
    
    return {
      courses: data.courses,
      tasks: data.pending_tasks
    };
  } catch (error) {
    console.error('Error obteniendo dashboard:', error);
  }
}

// Uso en React
function Dashboard() {
  const [data, setData] = useState(null);
  
  useEffect(() => {
    getUserDashboard(1).then(setData);
  }, []);
  
  if (!data) return <div>Cargando...</div>;
  
  return (
    <div>
      <h2>Mis Cursos ({data.courses.length})</h2>
      {data.courses.map(course => (
        <CourseCard key={course.id} course={course} />
      ))}
      
      <h2>Tareas Pendientes ({data.tasks.length})</h2>
      {data.tasks.map(task => (
        <TaskItem key={task.id} task={task} />
      ))}
    </div>
  );
}
```

---

## ✅ Gestión de Tareas {#tareas}

### Ejemplo 1: Alternar Estado de Tarea

```javascript
async function toggleTaskStatus(taskId) {
  try {
    const response = await fetch(`/api/academic/task/${taskId}/toggle`, {
      method: 'PUT'
    });
    
    const updatedTask = await response.json();
    return updatedTask;
  } catch (error) {
    console.error('Error actualizando tarea:', error);
  }
}

// Uso en componente
function TaskItem({ task, onUpdate }) {
  const handleToggle = async () => {
    const updated = await toggleTaskStatus(task.id);
    onUpdate(updated);
  };
  
  return (
    <div className="task-item">
      <button onClick={handleToggle}>
        {task.status === 'completada' ? '✅' : '⬜'}
      </button>
      <span className={task.status === 'completada' ? 'line-through' : ''}>
        {task.title}
      </span>
    </div>
  );
}
```

### Ejemplo 2: Eliminar Tarea

```javascript
async function deleteTask(taskId) {
  if (!confirm('¿Eliminar esta tarea?')) return;
  
  try {
    const response = await fetch(`/api/academic/task/${taskId}`, {
      method: 'DELETE'
    });
    
    if (response.ok) {
      return true;
    }
  } catch (error) {
    console.error('Error eliminando tarea:', error);
  }
}
```

### Ejemplo 3: Filtrar Tareas

```javascript
function filterTasks(tasks, filters) {
  return tasks.filter(task => {
    // Filtro de búsqueda
    if (filters.search) {
      const search = filters.search.toLowerCase();
      if (!task.title.toLowerCase().includes(search) &&
          !task.course_name.toLowerCase().includes(search)) {
        return false;
      }
    }
    
    // Filtro de prioridad
    if (filters.priority && filters.priority !== 'all') {
      if (task.priority !== filters.priority) {
        return false;
      }
    }
    
    // Filtro de estado
    if (filters.status && filters.status !== 'all') {
      if (task.status !== filters.status) {
        return false;
      }
    }
    
    return true;
  });
}

// Uso
const filteredTasks = filterTasks(allTasks, {
  search: 'examen',
  priority: 'critica',
  status: 'pendiente'
});
```

---

## ⚛️ Componentes React {#react}

### Ejemplo 1: Componente de Curso con Acciones

```jsx
import { BookOpen, Trash2, Edit2, Upload } from 'lucide-react';

function CourseCard({ course, onDelete, onEdit, onUploadSyllabus }) {
  return (
    <div 
      className="course-card"
      style={{ borderLeftColor: course.color }}
    >
      <div className="course-header">
        <BookOpen size={20} style={{ color: course.color }} />
        <h3>{course.name}</h3>
      </div>
      
      <p className="professor">{course.professor || 'Sin profesor'}</p>
      <p className="schedule">{course.schedule_info}</p>
      
      <div className="course-actions">
        <button onClick={() => onEdit(course)}>
          <Edit2 size={16} /> Editar
        </button>
        
        <label>
          <Upload size={16} /> Sílabo
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => onUploadSyllabus(course.id, e.target.files[0])}
            style={{ display: 'none' }}
          />
        </label>
        
        <button onClick={() => onDelete(course.id)}>
          <Trash2 size={16} /> Eliminar
        </button>
      </div>
    </div>
  );
}
```

### Ejemplo 2: Lista de Tareas con Filtros

```jsx
import { useState } from 'react';
import { Search, Filter } from 'lucide-react';

function TaskList({ tasks, onToggle, onDelete }) {
  const [search, setSearch] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');
  
  const filtered = tasks.filter(task => {
    const matchesSearch = task.title.toLowerCase().includes(search.toLowerCase());
    const matchesPriority = priorityFilter === 'all' || task.priority === priorityFilter;
    const matchesStatus = statusFilter === 'all' || task.status === statusFilter;
    return matchesSearch && matchesPriority && matchesStatus;
  });
  
  return (
    <div className="task-list">
      <div className="filters">
        <div className="search-box">
          <Search size={16} />
          <input
            type="text"
            placeholder="Buscar tareas..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        
        <select
          value={priorityFilter}
          onChange={(e) => setPriorityFilter(e.target.value)}
        >
          <option value="all">Todas las prioridades</option>
          <option value="critica">Crítica</option>
          <option value="alta">Alta</option>
          <option value="media">Media</option>
          <option value="baja">Baja</option>
        </select>
        
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="all">Todos los estados</option>
          <option value="pendiente">Pendiente</option>
          <option value="en_progreso">En progreso</option>
          <option value="completada">Completada</option>
        </select>
      </div>
      
      <div className="tasks">
        {filtered.map(task => (
          <TaskItem
            key={task.id}
            task={task}
            onToggle={onToggle}
            onDelete={onDelete}
          />
        ))}
      </div>
    </div>
  );
}
```

### Ejemplo 3: Hook Personalizado para Gestión de Tareas

```jsx
import { useState, useEffect } from 'react';

function useTasks(userId) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  
  const loadTasks = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/academic/user/${userId}/dashboard`);
      const data = await response.json();
      setTasks(data.pending_tasks || []);
    } catch (error) {
      console.error('Error cargando tareas:', error);
    } finally {
      setLoading(false);
    }
  };
  
  useEffect(() => {
    loadTasks();
  }, [userId]);
  
  const toggleTask = async (taskId) => {
    // Actualización optimista
    setTasks(tasks.map(t => 
      t.id === taskId 
        ? { ...t, status: t.status === 'completada' ? 'pendiente' : 'completada' }
        : t
    ));
    
    try {
      await fetch(`/api/academic/task/${taskId}/toggle`, { method: 'PUT' });
    } catch (error) {
      console.error('Error actualizando tarea:', error);
      loadTasks(); // Recargar si falla
    }
  };
  
  const deleteTask = async (taskId) => {
    if (!confirm('¿Eliminar esta tarea?')) return;
    
    // Actualización optimista
    setTasks(tasks.filter(t => t.id !== taskId));
    
    try {
      await fetch(`/api/academic/task/${taskId}`, { method: 'DELETE' });
    } catch (error) {
      console.error('Error eliminando tarea:', error);
      loadTasks(); // Recargar si falla
    }
  };
  
  return {
    tasks,
    loading,
    toggleTask,
    deleteTask,
    reload: loadTasks
  };
}

// Uso
function MyComponent() {
  const { tasks, loading, toggleTask, deleteTask } = useTasks(1);
  
  if (loading) return <div>Cargando...</div>;
  
  return (
    <div>
      {tasks.map(task => (
        <TaskItem
          key={task.id}
          task={task}
          onToggle={() => toggleTask(task.id)}
          onDelete={() => deleteTask(task.id)}
        />
      ))}
    </div>
  );
}
```

---

## 🎨 Estilos CSS Recomendados

```css
/* Cronómetro */
.stopwatch {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: linear-gradient(to right, #EFF6FF, #E0E7FF);
  padding: 0.5rem 1rem;
  border-radius: 0.75rem;
  border: 2px solid #BFDBFE;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

/* Cards de curso */
.course-card {
  background: white;
  padding: 1.25rem;
  border-radius: 0.75rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border-left: 4px solid var(--course-color);
  transition: all 0.2s;
}

.course-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

/* Tareas */
.task-item {
  display: flex;
  gap: 0.75rem;
  padding: 0.75rem;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 0.5rem;
  transition: all 0.2s;
}

.task-item:hover {
  border-color: #3B82F6;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1);
}

/* Badges de prioridad */
.priority-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
}

.priority-critica {
  background: #FEE2E2;
  color: #DC2626;
  border: 1px solid #FECACA;
}

.priority-alta {
  background: #FED7AA;
  color: #EA580C;
  border: 1px solid #FDBA74;
}

/* Animaciones */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-in {
  animation: fadeIn 0.3s ease-out;
}
```

---

¡Estos ejemplos te ayudarán a integrar todas las nuevas funcionalidades del Nodo Digital en tu aplicación! 🚀
