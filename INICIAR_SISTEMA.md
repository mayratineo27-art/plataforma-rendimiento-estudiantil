# 🚀 GUÍA DE INICIO - Plataforma de Rendimiento Estudiantil

## ⚠️ PROBLEMA ACTUAL

El error **"Unexpected token '<', '<!doctype'... is not valid JSON"** ocurre porque:

1. **El backend (Flask) NO está ejecutándose** en `http://localhost:5000`
2. El frontend intenta hacer peticiones API pero no encuentra el servidor
3. El navegador devuelve una página HTML de error en lugar de JSON

## ✅ SOLUCIÓN: Iniciar el Backend

### Opción 1: Usar el script automatizado (Recomendado)

#### En PowerShell:
```powershell
cd backend
.\iniciar_backend.ps1
```

#### En CMD:
```cmd
cd backend
iniciar_backend.bat
```

### Opción 2: Inicio manual

```powershell
# 1. Ir al directorio backend
cd backend

# 2. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# 3. Instalar dependencias (si no lo hiciste antes)
pip install -r requirements.txt

# 4. Iniciar el servidor
python run.py
```

## 📋 VERIFICACIÓN

Después de iniciar el backend, deberías ver:

```
╔══════════════════════════════════════════════════════════════╗
║  Plataforma Integral de Rendimiento Estudiantil             ║
║  Backend Server Starting...                                  ║
╚══════════════════════════════════════════════════════════════╝

🚀 Servidor corriendo en: http://localhost:5000
🔧 Modo: development

✓ Usando servidor Waitress

📦 Registrando blueprints...
   ✅ Academic routes: /api/academic
   ✅ Video routes: /api/video
   ✅ Audio routes: /api/audio
   ...
```

## 🧪 PROBAR LA CONEXIÓN

Abre tu navegador en: **http://localhost:5000/health**

Deberías ver:
```json
{
  "status": "healthy",
  "service": "backend",
  "database": "connected",
  "python_version": "3.13.8",
  "flask_version": "OK"
}
```

## 🎯 USO DEL SISTEMA COMPLETO

### 1. Iniciar el Backend (Terminal 1)
```powershell
cd backend
.\iniciar_backend.ps1
```
Espera a ver "Servidor corriendo en: http://localhost:5000"

### 2. Iniciar el Frontend (Terminal 2)
```powershell
cd frontend
npm start
```
Espera a que abra automáticamente en http://localhost:3000

### 3. Acceder a la Aplicación

Ve a: **http://localhost:3000/analisis**

Ahora podrás:
- ✅ Crear cursos sin errores
- ✅ Generar líneas de tiempo con IA
- ✅ Usar todas las herramientas de análisis
- ✅ Subir y procesar PDFs

## 🔧 REQUISITOS PREVIOS

### Base de Datos MySQL
Asegúrate de que MySQL esté ejecutándose y la base de datos exista:

```sql
CREATE DATABASE IF NOT EXISTS rendimiento_estudiantil;
```

### Variables de Entorno
El archivo `backend/.env` debe tener:

```env
DB_HOST=localhost
DB_NAME=rendimiento_estudiantil
DB_USER=root
DB_PASSWORD=TU_PASSWORD

GEMINI_API_KEY=TU_API_KEY_DE_GOOGLE
GEMINI_MODEL=gemini-2.5-flash
```

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "No module named 'flask'"
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Error: "Can't connect to MySQL server"
1. Verifica que MySQL esté ejecutándose
2. Revisa las credenciales en `backend/.env`
3. Crea la base de datos si no existe

### Error: "GEMINI_API_KEY no encontrada"
1. Obtén una API Key de Google AI Studio: https://makersuite.google.com/app/apikey
2. Agrégala al archivo `backend/.env`

### El frontend no puede conectarse al backend
1. Verifica que el backend esté ejecutándose (`http://localhost:5000/health`)
2. Asegúrate de que el puerto 5000 no esté ocupado
3. Revisa que `frontend/package.json` tenga: `"proxy": "http://localhost:5000"`

## 📦 ESTRUCTURA DE CARPETAS

```
plataforma-rendimiento-estudiantil/
├── backend/
│   ├── venv/                    # Entorno virtual Python
│   ├── app/                     # Código de la aplicación
│   ├── run.py                   # Punto de entrada
│   ├── .env                     # Variables de entorno
│   ├── iniciar_backend.ps1     # Script de inicio (PowerShell)
│   └── iniciar_backend.bat     # Script de inicio (CMD)
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json            # Configuración con proxy
└── INICIAR_SISTEMA.md          # Esta guía
```

## 🎓 FLUJO DE TRABAJO TÍPICO

1. **Sesión de trabajo nueva:**
   - Terminal 1: `cd backend && .\iniciar_backend.ps1`
   - Terminal 2: `cd frontend && npm start`
   - Navegar a http://localhost:3000/analisis

2. **Detener los servicios:**
   - Presiona `Ctrl + C` en ambos terminales

3. **Reiniciar después de cambios en el código:**
   - Backend: `Ctrl + C` y volver a ejecutar `python run.py`
   - Frontend: Se recarga automáticamente (hot reload)

## ✨ CARACTERÍSTICAS PRINCIPALES

- 📚 Gestión de cursos y tareas
- 🤖 Herramientas de IA (mapas mentales, resúmenes, líneas de tiempo)
- 📄 Análisis de syllabi con extracción automática de tareas
- ⏱️ Sistema de cronometraje por proyectos
- 📊 Gráficos de evolución de tiempo de estudio
- 📥 Exportación a PDF

---

**¿Necesitas ayuda?** Revisa los logs de error en ambos terminales para más información.
