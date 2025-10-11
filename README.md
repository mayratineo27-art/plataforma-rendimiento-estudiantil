# README principal

# 🎓 Plataforma Integral de Rendimiento Estudiantil

[![Python Version](https://img.shields.io/badge/python-3.13.8-blue.svg)](https://www.python.org/downloads/)
[![Node Version](https://img.shields.io/badge/node-22.20.0-green.svg)](https://nodejs.org/)
[![Flask Version](https://img.shields.io/badge/flask-3.1.2-orange.svg)](https://flask.palletsprojects.com/)
[![React Version](https://img.shields.io/badge/react-18.x-61dafb.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)

## 📋 Descripción

Una plataforma innovadora que utiliza Inteligencia Artificial para analizar el rendimiento estudiantil a través de múltiples dimensiones: documentos académicos, interacción en tiempo real (video y audio), y generación de contenido personalizado. El sistema proporciona insights profundos sobre el estilo de aprendizaje, fortalezas, debilidades y preparación para proyectos finales como la tesis.

## 🌟 Características Principales

### Módulo 1: Análisis de Progreso Académico
- 📄 Análisis de documentos PDF y DOCX a lo largo de 10 ciclos
- 📊 Medición cuantitativa de evolución en redacción y vocabulario
- 🎯 Predicción de preparación para la tesis
- 📈 Dashboard visual de progreso

### Módulo 2: Análisis de Interacción en Tiempo Real
- 🎥 Análisis de video mediante cámara web (detección facial multirostro)
- 🎤 Captura y transcripción de audio en tiempo real
- 😊 Reconocimiento de 16 emociones contextuales
- 📊 Timeline de atención y comprensión
- 🧠 Mapeo inteligente de emociones con pesos de atención

### Módulo 3: Perfil Integral del Estudiante
- 👤 Perfil unificado consolidando todos los análisis
- 💪 Identificación automática de fortalezas y debilidades
- 🎨 Análisis del estilo de aprendizaje preferido
- 📊 Base de datos centralizada con todos los datos del estudiante

### Módulo 4: Generador de Reportes Personalizados
- 📑 Reportes dinámicos por semestre, curso o sesión
- 📊 Visualización de datos con gráficos interactivos
- 🎨 Generación automática de plantillas (PPT, DOCX)
- 🎯 Contenido 100% personalizado según el perfil del estudiante

## 🏗️ Arquitectura

```
┌─────────────────┐
│   Frontend      │  React + Tailwind CSS
│   (Usuario)     │
└────────┬────────┘
         │ REST API
┌────────▼────────┐
│    Backend      │  Python + Flask
│  (Lógica de     │
│   Negocio)      │
└────┬────┬───────┘
     │    │
     │    └─────────────┐
     │                  │
┌────▼────────┐  ┌──────▼──────────┐
│   MySQL     │  │  Servicios IA   │
│  (Datos)    │  │  - Gemini API   │
└─────────────┘  │  - DeepFace     │
                 │  - NLP/Vision   │
                 └─────────────────┘
```

## 🚀 Tecnologías

### Frontend
- **React** 18.x
- **Tailwind CSS** para estilos
- **Axios** para llamadas API
- **Chart.js** para visualizaciones
- **React Router** para navegación

### Backend
- **Python** 3.13.8
- **Flask** 3.1.2 (Framework web)
- **SQLAlchemy** (ORM)
- **Flask-CORS** para CORS
- **PyMySQL** para conexión a MySQL

### Base de Datos
- **MySQL** 8.0+

### Inteligencia Artificial
- **Google Gemini API** (Análisis de texto, generación de contenido)
- **DeepFace** (Reconocimiento facial y emociones)
- **OpenCV** (Procesamiento de video)
- **SpeechRecognition** + **Pydub** (Audio y transcripción)
- **spaCy** / **NLTK** (NLP opcional)

### Testing
- **Pytest** (Tests unitarios y funcionales)
- **Coverage** (Cobertura de código)

## 📦 Instalación

### Prerequisitos

Asegúrate de tener instalado:
- Python 3.13.8
- Node.js 22.20.0
- npm 10.9.3
- MySQL 8.0+
- Git 2.51.0+

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/plataforma-rendimiento-estudiantil.git
cd plataforma-rendimiento-estudiantil
```

### 2. Configurar el Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
cp .env.example .env

# Editar .env con tus credenciales
nano .env
```

### 3. Configurar la Base de Datos

```bash
# Crear la base de datos MySQL
mysql -u root -p
CREATE DATABASE rendimiento_estudiantil;
exit;

# Ejecutar migraciones
flask db upgrade
```

### 4. Configurar el Frontend

```bash
cd ../frontend

# Instalar dependencias
npm install

# Copiar archivo de configuración
cp .env.example .env

# Editar .env con la URL del backend
nano .env
```

## ▶️ Ejecución

### Desarrollo

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # o venv\Scripts\activate en Windows
flask run
# El servidor correrá en http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
# La aplicación correrá en http://localhost:3000
```

### Producción

```bash
# Ver guía completa en docs/guias/despliegue.md
```

## 🧪 Testing

### Backend
```bash
cd backend
pytest
pytest --cov=app tests/  # Con cobertura
```

### Frontend
```bash
cd frontend
npm test
npm run test:coverage
```

## 📚 Documentación

- [Arquitectura General](docs/arquitectura/arquitectura_general.md)
- [Módulo 1: Análisis de Progreso](docs/modulos/modulo1_analisis_progreso.md)
- [Módulo 2: Interacción Tiempo Real](docs/modulos/modulo2_interaccion_tiempo_real.md)
- [Módulo 3: Perfil Integral](docs/modulos/modulo3_perfil_integral.md)
- [Módulo 4: Reportes Personalizados](docs/modulos/modulo4_reportes_personalizados.md)
- [API Endpoints](docs/api/endpoints.md)
- [Guía de Instalación Completa](docs/guias/instalacion.md)

## 🔑 Variables de Entorno

### Backend (.env)
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=tu-clave-secreta-aqui

# Base de Datos
DB_HOST=localhost
DB_PORT=3306
DB_NAME=rendimiento_estudiantil
DB_USER=root
DB_PASSWORD=tu-password

# Google Gemini API
GEMINI_API_KEY=tu-api-key-de-gemini

# Configuración de archivos
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=50MB
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_ENVIRONMENT=development
```

## 🤝 Contribución

Este es un proyecto académico en desarrollo activo. Contribuciones, issues y sugerencias son bienvenidas.

## 📝 Roadmap

### Fase 1: Fundación (Semanas 1-2) ✅
- [x] Estructura del proyecto
- [x] Configuración inicial
- [ ] Diseño de base de datos

### Fase 2: Módulo 1 (Semanas 3-4)
- [ ] Backend: Procesamiento de documentos
- [ ] Backend: Análisis de texto con Gemini
- [ ] Frontend: Interfaz de subida de archivos
- [ ] Frontend: Dashboard de progreso

### Fase 3: Módulo 2 (Semanas 5-7)
- [ ] Backend: Captura de video y audio
- [ ] Backend: Análisis de emociones con DeepFace
- [ ] Backend: Transcripción y análisis de audio
- [ ] Frontend: Interfaz de sesión en tiempo real

### Fase 4: Módulo 3 (Semanas 8-9)
- [ ] Backend: Agregación de datos
- [ ] Backend: Generación de perfil con IA
- [ ] Frontend: Vista de perfil integral

### Fase 5: Módulo 4 (Semanas 10-11)
- [ ] Backend: Generación de reportes
- [ ] Backend: Creación de plantillas PPT/DOCX
- [ ] Frontend: Interfaz de generación de reportes
- [ ] Frontend: Visualización de datos

### Fase 6: Integración y Testing (Semanas 12-13)
- [ ] Integración completa de módulos
- [ ] Testing exhaustivo
- [ ] Optimización de rendimiento
- [ ] Documentación final

### Fase 7: Despliegue (Semana 14)
- [ ] Configuración de servidor
- [ ] Despliegue en producción
- [ ] Monitoreo y ajustes

## 👥 Equipo

Proyecto desarrollado con dedicación, constancia y optimismo.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 📧 Contacto

Para preguntas o sugerencias sobre el proyecto, por favor abre un issue en GitHub.

---

⭐️ **"El éxito es la suma de pequeños esfuerzos repetidos día tras día"**