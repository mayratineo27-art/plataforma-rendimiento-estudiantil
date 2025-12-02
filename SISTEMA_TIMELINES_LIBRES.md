# 🆓 Sistema de Líneas de Tiempo Libres

## 📋 Resumen

Se ha implementado un nuevo sistema de **Líneas de Tiempo Libres** que permite a los usuarios crear y gestionar timelines para cualquier tema de aprendizaje libre (Sistemas Operativos, Lenguajes de Programación, Frameworks, etc.) **sin vinculación a proyectos o cursos académicos**.

---

## ✨ Características Implementadas

### 1. **Nuevo Tipo de Timeline: `'free'`**
- Se agregó el tipo `'free'` al modelo `Timeline` (además de `'academic'`, `'course'`, `'project'`)
- Las timelines libres NO requieren `course_id` ni `project_id`

### 2. **Componente FreeTimeline.jsx**
- **Ubicación**: `frontend/src/components/FreeTimeline.jsx`
- **Funcionalidades**:
  - ✅ Crear líneas de tiempo libres manualmente o con IA
  - ✅ Listar todas las timelines libres del usuario
  - ✅ Ver detalles de cada timeline
  - ✅ Marcar pasos como completados
  - ✅ Seguimiento de progreso con estadísticas
  - ✅ Eliminar timelines
  - ✅ Interfaz moderna con gradientes indigo-purple

### 3. **Integración en Navegación Principal**
- Nuevo link en el navbar: **"🆓 Timelines Libres"**
- Ruta: `/timelines-libre`
- Accesible desde cualquier parte de la plataforma

### 4. **Actualización de TimelineCreator**
- Ahora incluye selector de tipo de timeline
- Opciones:
  - 📚 Curso Académico
  - 🆓 Línea de Tiempo Libre (SO, Temas Generales)
  - 🎓 Académico General
  - 🚀 Proyecto
- El campo `course_id` se muestra/oculta según el tipo seleccionado

---

## 🚀 Cómo Usar

### **Crear una Línea de Tiempo Libre**

1. Ve a **"🆓 Timelines Libres"** en el navbar
2. Click en **"Nueva Timeline Libre"**
3. Completa el formulario:
   - **Título**: Ej: "Aprender Linux desde Cero"
   - **Descripción**: Objetivo del aprendizaje
   - **Fecha límite** (opcional)
   - **Generar con IA** ✨ o **Pasos Manuales** 📋
4. Click en **"Crear Línea de Tiempo"**

### **Gestionar Timelines**

- **Ver detalles**: Click en cualquier timeline de la lista
- **Marcar pasos completos**: Click en un paso para toggle completado/pendiente
- **Ver progreso**: Barra de progreso y estadísticas en tiempo real
- **Eliminar**: Botón 🗑️ en la vista de detalles

---

## 🛠️ Cambios Técnicos

### **Backend**

#### 1. Modelo Timeline (`backend/app/models/timeline.py`)
```python
# ANTES
timeline_type = db.Column(
    db.Enum('academic', 'course', 'project', name='timeline_type'),
    default='project'
)

# DESPUÉS
timeline_type = db.Column(
    db.Enum('academic', 'course', 'project', 'free', name='timeline_type'),
    default='project'
)
```

#### 2. Script de Migración (`backend/update_timeline_enum.py`)
- Actualiza el ENUM en MySQL para agregar `'free'`
- **Ejecutar**: `python update_timeline_enum.py`

### **Frontend**

#### 1. Nuevo Componente (`frontend/src/components/FreeTimeline.jsx`)
- 700+ líneas
- Componente completo con:
  - Listado de timelines libres
  - Modal de creación
  - Vista de detalles con pasos
  - Integración con IA

#### 2. TimelineCreator Actualizado
```javascript
// Nuevo estado
const [formData, setFormData] = useState({
  timeline_type: 'course', // 'course', 'free', 'academic', 'project'
  course_id: '',
  title: '',
  // ...
});
```

#### 3. App.jsx - Nueva Ruta
```javascript
<Route path="timelines-libre" element={<FreeTimeline />} />
```

---

## 📦 Archivos Modificados/Creados

### **Backend**
- ✅ `backend/app/models/timeline.py` - Enum actualizado
- ✅ `backend/update_timeline_enum.py` - Script de migración

### **Frontend**
- ✅ `frontend/src/components/FreeTimeline.jsx` - Nuevo componente
- ✅ `frontend/src/components/Timeline/TimelineCreator.jsx` - Selector de tipo
- ✅ `frontend/src/App.jsx` - Ruta y navegación

---

## 🔧 Instalación/Configuración

### **1. Actualizar Base de Datos**
```bash
cd backend
python update_timeline_enum.py
```

### **2. Reiniciar Backend**
```bash
cd backend
python run.py
```

### **3. Frontend ya está listo**
No requiere cambios adicionales. Solo refresh del navegador.

---

## 🎨 Interfaz

### **Vista Principal**
- Header con gradiente indigo-purple
- Lista de timelines en tarjetas con:
  - Título
  - Progreso visual (barra de progreso)
  - Número de pasos completados/total
  - Fecha límite (si existe)

### **Vista de Detalles**
- Información completa del timeline
- Estadísticas (Progreso %, Completados, Pendientes)
- Lista de pasos con:
  - Números de orden
  - Check visual para completados
  - Línea de tiempo vertical
  - Descripción de cada paso

### **Modal de Creación**
- Formulario intuitivo
- Opción de generar con IA 🤖
- Pasos manuales con editor inline
- Validación de campos

---

## 🌟 Casos de Uso

### **Sistemas Operativos**
```
Título: Dominar Linux Avanzado
Pasos:
1. Instalación de distribuciones
2. Comandos básicos de terminal
3. Administración de usuarios
4. Configuración de servicios
5. Scripting con Bash
6. Administración de redes
```

### **Lenguajes de Programación**
```
Título: Aprender Python desde Cero
Pasos:
1. Sintaxis básica y variables
2. Estructuras de control
3. Funciones y módulos
4. POO en Python
5. Manejo de archivos
6. Librerías populares
```

### **Tecnologías Web**
```
Título: Dominar React.js
Pasos:
1. JSX y componentes
2. State y Props
3. Hooks (useState, useEffect)
4. Context API
5. React Router
6. Proyecto final
```

---

## 🔮 Funcionalidades Futuras (Opcional)

- ⏱️ **Tiempo estimado por paso**: Agregar duración estimada
- 🏆 **Badges/Logros**: Al completar timelines
- 📊 **Estadísticas globales**: Total de timelines, promedio de completación
- 🔔 **Notificaciones**: Recordatorios de fechas límite
- 📤 **Exportar**: Exportar timeline a PDF/Markdown
- 🤝 **Compartir**: Compartir timelines con otros usuarios

---

## 📝 Notas Técnicas

### **Diferencias con Timelines Académicas**

| Característica | Timeline Académica | Timeline Libre |
|----------------|-------------------|----------------|
| **course_id** | Requerido | NULL |
| **project_id** | Opcional | NULL |
| **Tipo** | 'course', 'academic', 'project' | 'free' |
| **Uso** | Vinculado a cursos/proyectos | Independiente |
| **Ubicación** | Academic Dashboard | Timelines Libres |

### **API Endpoints Usados**
- `GET /api/timelines/user/:userId` - Listar timelines del usuario
- `POST /api/timeline/create` - Crear nueva timeline
- `PUT /api/timeline/:id/step/:stepId/toggle` - Toggle completado de paso
- `DELETE /api/timeline/:id` - Eliminar timeline

---

## ✅ Estado del Sistema

- ✅ Backend: Modelo actualizado
- ✅ Frontend: Componente implementado
- ✅ Navegación: Integrada en navbar
- ⏳ Base de datos: Requiere ejecutar `update_timeline_enum.py`

---

## 🆘 Troubleshooting

### **Error: timeline_type tiene valor no permitido**
**Solución**: Ejecutar `python backend/update_timeline_enum.py`

### **No se muestran las timelines libres**
**Verificar**:
1. El backend está corriendo
2. El usuario tiene timelines con `timeline_type='free'`
3. La ruta `/api/timelines/user/:userId` responde correctamente

### **Error al crear timeline**
**Verificar**:
1. El campo `title` no está vacío
2. El backend acepta `timeline_type='free'`
3. La consola del navegador (F12) para errores JavaScript

---

## 📞 Contacto

Para dudas o mejoras sobre esta funcionalidad, consulta el código en:
- `frontend/src/components/FreeTimeline.jsx`
- `backend/app/models/timeline.py`
- `backend/app/routes/timeline_routes.py`

---

**¡Disfruta organizando tu aprendizaje libre! 🚀**
