# Líneas de Tiempo por Temas de Cursos

## 📚 Descripción

Nueva funcionalidad que permite crear y gestionar **líneas de tiempo específicas para temas de cualquier curso**, independientemente de los proyectos. Esta característica complementa las líneas de tiempo libres existentes, permitiendo organizar y planificar el estudio de temas específicos dentro de cursos académicos.

## ✨ Características

- **Creación de líneas de tiempo por tema**: Asocia una línea de tiempo a un curso y tema específico
- **Independiente de proyectos**: No requiere tener un proyecto asociado
- **Gestión completa**: Crear, visualizar, actualizar y eliminar líneas de tiempo de temas
- **Interfaz intuitiva**: Componentes React dedicados para una experiencia de usuario óptima
- **Integración con el sistema existente**: Utiliza el modelo Timeline con tipo 'free'

## 🏗️ Arquitectura

### Backend

#### Modelo de Datos
El modelo `Timeline` ha sido extendido con la columna `course_topic`:

```python
# backend/app/models/timeline.py
class Timeline(db.Model):
    # ... campos existentes ...
    course_topic = db.Column(db.String(200), nullable=True, 
                            comment='Tema específico del curso para timelines de tipo free')
```

#### Endpoints API

**POST** `/api/timeline/topic`
- Crea una nueva línea de tiempo de tema
- **Body**:
  ```json
  {
    "user_id": 1,
    "course_name": "Matemáticas",
    "topic_name": "Álgebra Lineal",
    "description": "Estudio de vectores y matrices" // opcional
  }
  ```

**GET** `/api/timeline/topic`
- Obtiene todas las líneas de tiempo de temas del usuario autenticado
- **Response**:
  ```json
  {
    "timelines": [
      {
        "id": 1,
        "course_name": "Matemáticas",
        "course_topic": "Álgebra Lineal",
        "description": "...",
        "start_date": "2025-12-01",
        "end_date": null,
        "timeline_type": "free"
      }
    ]
  }
  ```

#### Archivos Backend Modificados/Creados
- `backend/app/models/timeline.py` - Modelo extendido con `course_topic`
- `backend/app/routes/timeline_routes.py` - Endpoint `/topic/create` (ya existía)
- `backend/add_course_topic_to_timeline.py` - Script de migración

### Frontend

#### Componentes React

**TopicTimelines.jsx**
- Componente principal para visualizar y gestionar líneas de tiempo de temas
- Muestra tarjetas con información de cada línea de tiempo
- Permite crear nuevas líneas de tiempo y eliminar existentes
- Decodifica el token JWT para obtener el `userId`

**CreateTopicTimeline.jsx**
- Formulario para crear nuevas líneas de tiempo de temas
- Valida campos requeridos (curso y tema)
- Maneja estados de carga y errores
- Interfaz con TailwindCSS

#### Rutas Frontend
- **Ruta**: `/timelines-temas`
- **Navegación**: "📚 Temas de Cursos" en el menú principal

#### Archivos Frontend Creados
- `frontend/src/components/TopicTimelines.jsx`
- `frontend/src/components/CreateTopicTimeline.jsx`
- `frontend/src/App.jsx` - Actualizado con nueva ruta

#### Dependencias Añadidas
- `jwt-decode`: ^4.0.0 - Para decodificar tokens JWT en el frontend

## 🚀 Instalación y Configuración

### 1. Backend - Migración de Base de Datos

Ejecuta el script de migración para añadir la columna `course_topic`:

```bash
cd backend
python add_course_topic_to_timeline.py
```

### 2. Frontend - Instalar Dependencias

```bash
cd frontend
npm install
```

Esto instalará `jwt-decode` y otras dependencias necesarias.

### 3. Reiniciar Servicios

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

## 📖 Uso

### Crear una Línea de Tiempo de Tema

1. Navega a "📚 Temas de Cursos" en el menú principal
2. Haz clic en "+ Nueva Línea de Tiempo"
3. Completa el formulario:
   - **Nombre del Curso**: El curso al que pertenece el tema
   - **Tema**: El tema específico a estudiar
   - **Descripción** (opcional): Detalles adicionales
4. Haz clic en "Crear Línea de Tiempo"

### Visualizar Líneas de Tiempo

La página principal muestra todas tus líneas de tiempo de temas en tarjetas con:
- Nombre del tema
- Curso asociado
- Descripción
- Fechas de inicio y fin
- Opciones para ver detalles o eliminar

### Eliminar una Línea de Tiempo

Haz clic en el icono 🗑️ en la tarjeta de la línea de tiempo y confirma la eliminación.

## 🔧 Ejemplos de Uso

### Ejemplo 1: Matemáticas - Cálculo Integral
```
Curso: Matemáticas
Tema: Cálculo Integral
Descripción: Estudio de integrales definidas e indefinidas, técnicas de integración
```

### Ejemplo 2: Historia - Revolución Francesa
```
Curso: Historia Universal
Tema: Revolución Francesa
Descripción: Causas, desarrollo y consecuencias de la Revolución Francesa (1789-1799)
```

### Ejemplo 3: Programación - Algoritmos de Ordenamiento
```
Curso: Estructuras de Datos
Tema: Algoritmos de Ordenamiento
Descripción: QuickSort, MergeSort, HeapSort - análisis de complejidad temporal
```

## 🔄 Diferencias con Líneas de Tiempo Existentes

| Característica | Líneas de Tiempo de Proyectos | Líneas de Tiempo Libres | Líneas de Tiempo de Temas |
|----------------|------------------------------|-------------------------|---------------------------|
| **Tipo** | `project` | `free` | `free` |
| **Asociación** | Proyecto específico | General (SO, tecnologías) | Curso + Tema específico |
| **Campo clave** | `project_id` | Ninguno | `course_topic` + `course_name` |
| **Uso** | Gestión de proyectos | Aprendizaje general | Estudio académico por materias |

## 🔐 Autenticación

Los endpoints requieren autenticación mediante token JWT:
- El token debe incluirse en el header `Authorization: Bearer <token>`
- El `user_id` se extrae automáticamente del token en el backend
- En el frontend, se decodifica el token para obtener el `user_id`

## 🧪 Testing

Para probar la funcionalidad:

```bash
# Backend
cd backend
python -m pytest tests/test_timeline_routes.py -k "topic"

# Frontend
cd frontend
npm test -- --testPathPattern=TopicTimelines
```

## 📝 Notas Técnicas

1. **Modelo Timeline flexible**: Reutiliza el modelo existente con `timeline_type='free'`
2. **Sin eliminación de código**: Toda la funcionalidad anterior se mantiene intacta
3. **Validación de datos**: Se valida que curso y tema sean obligatorios
4. **Manejo de errores**: Mensajes de error claros tanto en backend como frontend
5. **Responsive Design**: Los componentes están diseñados con TailwindCSS para funcionar en móviles y escritorio

## 🐛 Troubleshooting

### Error: "No se pudo obtener el ID del usuario"
- **Causa**: Token JWT no válido o expirado
- **Solución**: Cierra sesión y vuelve a iniciar sesión

### Error: "La columna 'course_topic' no existe"
- **Causa**: Migración de base de datos no ejecutada
- **Solución**: Ejecuta `python add_course_topic_to_timeline.py`

### Error: "jwt-decode is not defined"
- **Causa**: Dependencia no instalada
- **Solución**: Ejecuta `npm install` en el directorio frontend

## 🎯 Próximas Mejoras

- [ ] Añadir filtros por curso
- [ ] Búsqueda de líneas de tiempo
- [ ] Estadísticas de progreso por tema
- [ ] Exportar líneas de tiempo en PDF
- [ ] Compartir líneas de tiempo con otros usuarios
- [ ] Integración con calendario

## 👥 Contribución

Esta funcionalidad se integra perfectamente con el sistema existente. Para contribuir:
1. Mantén la estructura de archivos
2. Sigue las convenciones de código existentes
3. Añade pruebas para nuevas funcionalidades
4. Actualiza esta documentación

## 📄 Licencia

Misma licencia que el proyecto principal.
