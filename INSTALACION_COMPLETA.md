# 📦 Guía de Instalación Completa
## Plataforma Integral de Rendimiento Estudiantil

### Última actualización: Diciembre 2025
**Incluye:** Módulo de Líneas de Tiempo por Temas de Cursos

---

## 📋 Requisitos Previos

### Software Necesario

1. **Python 3.10 o superior**
   - Descargar: https://www.python.org/downloads/
   - ⚠️ En Windows: Marcar "Add Python to PATH" durante instalación

2. **Node.js 16+ y npm**
   - Descargar: https://nodejs.org/

3. **MySQL 8.0+**
   - Descargar: https://dev.mysql.com/downloads/mysql/

4. **Git**
   - Descargar: https://git-scm.com/downloads

### Verificar Instalaciones

```bash
# Verificar versiones
python --version   # o py --version en Windows
node --version
npm --version
mysql --version
git --version
```

---

## 🚀 Instalación Paso a Paso

### 1. Clonar el Repositorio

```bash
git clone https://github.com/mayratineo27-art/plataforma-rendimiento-estudiantil.git
cd plataforma-rendimiento-estudiantil
```

### 2. Configurar Base de Datos

#### Crear Base de Datos

```bash
# Iniciar sesión en MySQL
mysql -u root -p

# Crear base de datos
CREATE DATABASE plataforma_estudiantil CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Crear usuario (opcional pero recomendado)
CREATE USER 'plataforma_user'@'localhost' IDENTIFIED BY 'tu_password_seguro';
GRANT ALL PRIVILEGES ON plataforma_estudiantil.* TO 'plataforma_user'@'localhost';
FLUSH PRIVILEGES;

# Salir
exit;
```

#### Aplicar Migraciones

```bash
# Migración principal
mysql -u root -p plataforma_estudiantil < database/migrations/mejoras_gestion_2025_11_23.sql

# Verificar tablas creadas
mysql -u root -p -e "USE plataforma_estudiantil; SHOW TABLES;"
```

### 3. Configurar Backend

#### Instalar Dependencias Python

```bash
cd backend

# Crear entorno virtual
python -m venv venv
# O en Windows: py -m venv venv

# Activar entorno virtual
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

#### Configurar Variables de Entorno

Crear archivo `.env` en la carpeta `backend/`:

```bash
# backend/.env

# Base de Datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_password_mysql
DB_NAME=plataforma_estudiantil

# Seguridad
SECRET_KEY=tu_clave_secreta_muy_segura_aqui
JWT_SECRET_KEY=otra_clave_secreta_para_jwt

# Google Gemini API (para análisis de documentos)
GEMINI_API_KEY=tu_api_key_de_google_gemini

# Flask
FLASK_ENV=development
FLASK_DEBUG=True

# Archivos
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216

# Logging
LOG_LEVEL=INFO
```

#### Ejecutar Migraciones Adicionales

```bash
# Asegurarse de estar en la carpeta backend con venv activado
python add_course_topic_to_timeline.py
# O en Windows: py add_course_topic_to_timeline.py

# Deberías ver: ✓ Columna 'course_topic' añadida exitosamente
```

### 4. Configurar Frontend

```bash
cd ../frontend

# Instalar dependencias (incluye jwt-decode)
npm install

# Verificar que no haya errores
```

#### Configurar Variables de Entorno (Opcional)

Crear archivo `.env` en la carpeta `frontend/`:

```bash
# frontend/.env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_ENV=development
```

---

## ▶️ Ejecutar la Aplicación

### Opción 1: Usando Scripts (Recomendado)

#### Windows

```bash
# Terminal 1 - Backend
cd backend
.\iniciar_backend.bat

# Terminal 2 - Frontend
cd frontend
npm start
```

#### Linux/Mac

```bash
# Terminal 1 - Backend
cd backend
source venv/bin/activate
python run.py

# Terminal 2 - Frontend
cd frontend
npm start
```

### Opción 2: Manual

#### Backend (Puerto 5000)

```bash
cd backend
# Activar venv si no está activado
python run.py
```

#### Frontend (Puerto 3000)

```bash
cd frontend
npm start
```

---

## 🧪 Verificar Instalación

### 1. Backend - Health Check

Abrir navegador o usar curl:
```bash
curl http://localhost:5000/api/health
```

Respuesta esperada:
```json
{
  "status": "ok",
  "timestamp": "2025-12-01T..."
}
```

### 2. Frontend - Acceder a la Aplicación

Abrir navegador en: **http://localhost:3000**

### 3. Crear Usuario de Prueba

```bash
cd backend
python create_user.py
```

O registrarse desde la interfaz: **http://localhost:3000/register**

### 4. Probar Nueva Funcionalidad

1. Iniciar sesión
2. Navegar a **"📄 Nodo Digital"** en el menú principal
3. Hacer clic en la pestaña **"Temas"**
4. Crear una línea de tiempo de prueba

---

## 🔧 Solución de Problemas Comunes

### Error: "python no se reconoce"

**Windows:** Usa `py` en lugar de `python`
```bash
py --version
py -m venv venv
```

### Error: "Cannot find module 'jwt-decode'"

```bash
cd frontend
npm install jwt-decode
```

### Error: "Access denied for user"

Verificar credenciales en `backend/.env`:
```bash
DB_USER=root
DB_PASSWORD=tu_password_correcto
```

### Error: "Column 'course_topic' doesn't exist"

Ejecutar migración:
```bash
cd backend
python add_course_topic_to_timeline.py
```

### Error: "Port 5000 already in use"

```bash
# Windows - Encontrar proceso
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Error: "npm vulnerabilities"

```bash
cd frontend
npm audit fix
# O ignorar si no son críticas
```

### Error: Base de datos no conecta

Verificar MySQL:
```bash
# Windows
net start MySQL80

# Linux
sudo systemctl start mysql

# Verificar conexión
mysql -u root -p -e "SELECT 1;"
```

---

## 📚 Dependencias Principales

### Backend (Python)

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| Flask | 3.1.2 | Framework web |
| SQLAlchemy | 2.0.43 | ORM base de datos |
| PyJWT | 2.8.0 | Autenticación JWT |
| google-generativeai | 0.4.6 | API Gemini |
| deepface | 0.0.95 | Reconocimiento facial |
| python-docx | 1.1.0 | Procesamiento documentos |

### Frontend (Node.js)

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| react | 18.2.0 | Framework UI |
| react-router-dom | 6.21.1 | Enrutamiento |
| axios | 1.6.2 | Cliente HTTP |
| jwt-decode | 4.0.0 | Decodificar tokens JWT |
| tailwindcss | 3.4.0 | Estilos CSS |
| recharts | 2.10.3 | Gráficos |

---

## 🎯 Próximos Pasos

1. **Configurar API de Gemini**
   - Obtener clave: https://makersuite.google.com/app/apikey
   - Añadir a `backend/.env`

2. **Explorar Funcionalidades**
   - 📚 Gestión de Cursos
   - 📝 Evaluación de Escritura
   - 📊 Análisis con IA
   - 📅 Líneas de Tiempo de Temas (Pestaña "Temas" en Nodo Digital)

3. **Leer Documentación**
   - `LINEAS_TIEMPO_TEMAS_CURSOS.md` - Nueva funcionalidad
   - `MODULO_EVALUACION_ESCRITURA.md` - Evaluación documentos
   - `GUIA_NODO_DIGITAL.md` - Módulo académico

---

## 🆘 Soporte

### Problemas Conocidos

Ver archivo: `SOLUCION_ERRORES.md`

### Reportar Bugs

1. Verificar logs:
   - Backend: `backend/logs/`
   - Frontend: Consola del navegador (F12)

2. Crear issue en GitHub con:
   - Descripción del error
   - Pasos para reproducir
   - Logs relevantes
   - Sistema operativo y versiones

---

## 📄 Licencia

Ver archivo `LICENSE` en el repositorio.

---

## ✅ Checklist de Instalación

- [ ] Python 3.10+ instalado y en PATH
- [ ] Node.js 16+ instalado
- [ ] MySQL 8.0+ instalado y ejecutándose
- [ ] Repositorio clonado
- [ ] Base de datos creada
- [ ] Migraciones aplicadas (incluyendo course_topic)
- [ ] Backend: venv creado y dependencias instaladas
- [ ] Backend: archivo .env configurado
- [ ] Frontend: dependencias instaladas (npm install)
- [ ] Backend ejecutándose en puerto 5000
- [ ] Frontend ejecutándose en puerto 3000
- [ ] Usuario de prueba creado
- [ ] Nueva funcionalidad de temas probada

**¡Felicidades! 🎉 El sistema está listo para usar.**
