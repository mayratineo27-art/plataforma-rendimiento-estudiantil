# 🚀 Inicio Rápido - Nuevas Funcionalidades

## ⚡ Pasos para Empezar

### 1️⃣ Aplicar Migraciones de Base de Datos (5 minutos)

```bash
# Abrir MySQL
mysql -u root -p

# Ejecutar migración principal
source database/migrations/mejoras_gestion_2025_11_23.sql

# Verificar
USE plataforma_estudiantil;
SHOW TABLES;

# Ejecutar migración de líneas de tiempo de temas
cd backend
python add_course_topic_to_timeline.py
# O en Windows: py add_course_topic_to_timeline.py
```

### 2️⃣ Instalar Dependencias Frontend (2 minutos)

```bash
cd frontend
npm install
```

**Nota:** Esto instalará `jwt-decode` y otras dependencias nuevas necesarias para las líneas de tiempo de temas.

### 3️⃣ Reiniciar Backend (30 segundos)

```bash
cd backend

# Windows
.\iniciar_backend.bat

# Linux/Mac
source venv/bin/activate
python run.py
```

### 4️⃣ Reiniciar Frontend (30 segundos)

```bash
cd frontend
npm start
```

**¡Listo!** Abre `http://localhost:3000/analisis` 🎉

---

## 🎯 Prueba las Nuevas Funcionalidades

### 📚 Líneas de Tiempo por Temas de Cursos

```
1. Navega a "📄 Nodo Digital" en el menú principal
2. Haz clic en la pestaña "Temas"
3. Click en "+ Nueva Línea de Tiempo"
4. Llenar formulario:
   - Curso: "Matemáticas"
   - Tema: "Álgebra Lineal"
   - Descripción: "Vectores, matrices y sistemas lineales"
5. Click en "Crear Línea de Tiempo"
```

### 📚 Gestión de Cursos (Tab "Gestión")

```
1. Click en botón con mensaje motivacional
2. Llenar formulario:
   - Nombre: "Cálculo Diferencial"
   - Código: "MAT-101"
   - Profesor: "Dr. Juan Pérez"
3. Elegir icono: 🧠 Brain
4. Elegir categoría: 🔢 Matemáticas
5. Elegir color: 🟣 Purple
6. Crear curso
```

**Resultado:** Curso creado con diseño moderno y personalizado

---

### 📄 Análisis de Sílabos (Tab "Sílabos")

```
1. Seleccionar curso del dropdown
2. Click en área de carga o arrastrar PDF
3. Esperar análisis (automático con IA)
4. Ver en historial lateral
5. Click en análisis para ver detalles
6. Click en cualquier tema para marcar como completado ✅
```

**Resultado:** Historial de sílabos con progreso visual

---

### 🕒 Líneas de Tiempo (Tab "Línea de Tiempo")

#### Opción A: Con IA 🤖
```
1. Click en botón "Crea tu ruta al éxito 🚀"
2. Seleccionar curso
3. Título: "Plan de estudio Parcial 1"
4. Activar checkbox "Generar con IA"
5. Contexto: "Examen de cálculo sobre derivadas en 2 semanas"
6. Crear
```

#### Opción B: Manual 📝
```
1. Click en botón "Crea tu ruta al éxito 🚀"
2. Seleccionar curso
3. Título: "Plan personalizado"
4. NO activar IA
5. Agregar pasos manualmente:
   - Paso 1: "Revisar capítulo 1"
   - Paso 2: "Hacer ejercicios"
   - ...
6. Crear
```

**Resultado:** Línea de tiempo con pasos interactivos

---

## 🎨 Personalización Rápida

### Cambiar Icono de Curso

```javascript
Iconos disponibles:
📚 BookOpen  🧠 Brain     💻 Laptop   </> Code    💡 Lightbulb
⭐ Star      ⚡ Zap       🎯 Target   🚀 Rocket   🏆 Award
🎵 Music     📷 Camera    ❤️ Heart    ☕ Coffee   📈 TrendingUp
```

### Cambiar Categoría

```javascript
Categorías:
📚 General      🔬 Ciencias     🔢 Matemáticas  ⚙️ Ingeniería
🎨 Artes        🌍 Idiomas      💻 Tecnología   💼 Negocios
```

### Cambiar Color

```javascript
Colores:
🔵 Blue    🟣 Purple  🟢 Green   🟠 Orange  🌸 Pink
🔷 Indigo  🔴 Red     🔷 Cyan    🟡 Yellow
```

---

## 📱 Interfaz de Usuario

### Navegación

```
/analisis
├── Gestión       → CourseManagerPro (iconos y categorías)
├── Herramientas  → StudyTools (IA)
├── Línea Tiempo  → TimelineCreator (crear y gestionar)
├── Sílabos       → SyllabusAnalyzerPro (historial y progreso)
├── Proyectos     → ModernProjectManager (cronómetro)
└── Evolución     → EvolutionChart (estadísticas)
```

### Atajos de Teclado

- `Esc` - Cerrar modales
- `Ctrl+Shift+R` - Limpiar cache y recargar

---

## ✅ Verificación Rápida

Ejecuta este checklist en 2 minutos:

```bash
# 1. ¿Backend corriendo?
curl http://localhost:5000/api/health
# Debe responder: {"status":"running"}

# 2. ¿Frontend corriendo?
curl http://localhost:3000
# Debe responder: HTML

# 3. ¿Base de datos actualizada?
mysql -u root -p -e "USE plataforma_estudiantil; DESCRIBE syllabus_analysis;"
# Debe mostrar tabla sin error
```

---

## 🐛 Solución de Problemas en 30 Segundos

### Backend no inicia
```bash
cd backend
pip install -r requirements.txt
python run.py
```

### Frontend no compila
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Migración falla
```bash
# Verificar usuario y permisos
mysql -u root -p -e "SELECT USER();"

# Ejecutar manualmente línea por línea
# Copiar desde mejoras_gestion_2025_11_23.sql
```

### Componentes no aparecen
```
1. Ctrl+Shift+R (limpiar cache)
2. Verificar consola del navegador (F12)
3. Verificar que archivos .jsx existen en src/components/
```

---

## 📦 Estructura de Archivos

```
plataforma-rendimiento-estudiantil/
├── frontend/src/components/
│   ├── Courses/CourseManagerPro.jsx         ⭐ NUEVO
│   ├── Syllabus/SyllabusAnalyzerPro.jsx     ⭐ NUEVO
│   └── Timeline/TimelineCreator.jsx         ⭐ NUEVO
│
├── backend/app/
│   ├── models/
│   │   ├── syllabus.py                      ⭐ NUEVO
│   │   └── timeline_step.py                 ⭐ NUEVO
│   └── routes/
│       ├── academic_routes.py               🔄 ACTUALIZADO
│       └── timeline_routes.py               🔄 ACTUALIZADO
│
├── database/migrations/
│   └── mejoras_gestion_2025_11_23.sql       ⭐ NUEVO
│
└── docs/
    ├── MEJORAS_NOVIEMBRE_2025.md            📚 Documentación completa
    └── RESUMEN_MEJORAS.md                   📝 Resumen ejecutivo
```

---

## 🎓 Ejemplos de Uso

### Crear Curso de Matemáticas

```javascript
{
  "name": "Cálculo Integral",
  "code": "MAT-201",
  "professor": "Dr. María García",
  "schedule": "Mar-Jue 14:00-16:00",
  "category": "matematicas",
  "icon": "TrendingUp",
  "color": "purple"
}
```

### Crear Línea de Tiempo con IA

```javascript
{
  "title": "Preparación Examen Final",
  "course_id": 5,
  "generate_with_ai": true,
  "ai_context": "Examen final de cálculo integral sobre métodos de integración, aplicaciones y series. Tengo 3 semanas para estudiar.",
  "end_date": "2025-12-15"
}
```

### Análisis de Sílabo

```javascript
// Simplemente cargar PDF
// La IA extrae automáticamente:
// - Información del curso
// - Lista de temas
// - Objetivos
// - Evaluaciones
```

---

## 🔍 Endpoints API Principales

### Cursos
```bash
# Crear curso
POST http://localhost:5000/api/academic/course/create
Content-Type: application/json
{ "user_id": 1, "name": "Curso", "icon": "Brain", ... }

# Listar cursos
GET http://localhost:5000/api/academic/user/1/courses
```

### Sílabos
```bash
# Cargar PDF
POST http://localhost:5000/api/academic/course/5/upload-syllabus
Content-Type: multipart/form-data
file: syllabus.pdf
user_id: 1

# Ver historial
GET http://localhost:5000/api/academic/user/1/syllabus-history

# Marcar tema
PUT http://localhost:5000/api/academic/syllabus/1/topic/0/toggle
```

### Líneas de Tiempo
```bash
# Crear
POST http://localhost:5000/api/timeline/create
Content-Type: application/json
{ "user_id": 1, "title": "Plan", "generate_with_ai": true, ... }

# Listar
GET http://localhost:5000/api/timeline/user/1

# Marcar paso
PUT http://localhost:5000/api/timeline/1/step/1/toggle
```

---

## 💡 Tips y Trucos

### 1. Mensajes Motivacionales Aleatorios
Cada vez que recargas, el botón de crear muestra un mensaje diferente:
- "¡Crea tu próxima aventura académica! 🚀"
- "¡Expande tu conocimiento! 🧠"
- ...

### 2. Progreso Visual Dinámico
Los colores cambian según el progreso:
- 0-39%: Morado-Rosa
- 40-69%: Amarillo-Naranja
- 70-99%: Azul-Índigo
- 100%: Verde

### 3. Historial Persistente
Todo se guarda automáticamente:
- Análisis de sílabos
- Líneas de tiempo
- Progreso de temas
- Pasos completados

### 4. Click para Completar
En sílabos y líneas de tiempo, simplemente haz click en cualquier tema/paso para marcarlo como completado. ¡Así de fácil!

### 5. Generación con IA
Cuanto más contexto des a la IA, mejores serán los pasos generados. Incluye:
- Tiempo disponible
- Temas específicos
- Tipo de evaluación
- Dificultad

---

## 🎉 ¡Todo Listo!

Ahora tienes:
- ✅ Cursos con iconos y categorías
- ✅ Historial de sílabos con progreso
- ✅ Creador de líneas de tiempo con IA
- ✅ Interfaz moderna y motivacional

**¡Empieza a organizar tu vida académica! 🎓✨**

---

## 📚 Más Información

- **Documentación Completa:** `docs/MEJORAS_NOVIEMBRE_2025.md`
- **Resumen Ejecutivo:** `RESUMEN_MEJORAS.md`
- **Código Fuente:** `frontend/src/components/` y `backend/app/`

---

**Creado con ❤️ para estudiantes organizados y exitosos**
