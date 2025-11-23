# 🔐 Configuración del Archivo .env

## ✅ Tu Configuración Actual

Tu archivo `.env` **ya está configurado** con Gemini API. Aquí está lo que tienes:

```env
GEMINI_API_KEY=AIzaSyDapoY4GA-44d3CFpg1KkPrebdJfBmxV94
GEMINI_MODEL=gemini-2.5-flash
```

### ¿Qué significa esto?

- ✅ **GEMINI_API_KEY**: Tu clave de API de Google Gemini (ya configurada)
- ✅ **GEMINI_MODEL**: El modelo a usar (`gemini-2.5-flash` es el más rápido y recomendado)
- ✅ **GEMINI_MAX_TOKENS**: Máximo de tokens por respuesta (8192)
- ✅ **GEMINI_TEMPERATURE**: Creatividad del modelo (0.7 es balanceado)

### Modelos Disponibles

- **gemini-2.5-flash** ⚡ - El más rápido (RECOMENDADO)
- **gemini-2.5-pro** 🧠 - Más preciso pero más lento
- **gemini-2.0-flash** - Versión anterior rápida
- **gemini-flash-latest** - Siempre el último flash

**Nota:** Los modelos `gemini-pro` y `gemini-1.5-flash` ya no están disponibles en la API actual.

---

## 🆕 Si Necesitas una Nueva API Key

### 1. Obtener tu propia API Key de Google Gemini

1. **Ve a Google AI Studio:**
   - URL: https://makersuite.google.com/app/apikey
   - O: https://aistudio.google.com/app/apikey

2. **Inicia sesión** con tu cuenta de Google

3. **Click en "Get API Key"** o "Create API Key"

4. **Copia la clave** que se genera (empieza con `AIza...`)

### 2. Actualizar tu archivo .env

Abre `backend/.env` y reemplaza la línea:

```env
GEMINI_API_KEY=tu_nueva_api_key_aqui
```

---

## 🔍 Verificar que Funciona

### Opción 1: Usando el script de prueba

```bash
cd backend
python test_nodo_digital.py
```

Deberías ver:
```
✅ GEMINI_API_KEY configurada (AIzaSyDapo...)
```

### Opción 2: Prueba manual en Python

```bash
cd backend
python
```

Luego ejecuta:

```python
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()

# Obtener la API key
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key cargada: {api_key[:10]}..." if api_key else "❌ No encontrada")

# Configurar y probar
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Di hola")
    print(f"✅ Respuesta de Gemini: {response.text}")
```

Si todo funciona, verás:
```
API Key cargada: AIzaSyDapo...
✅ Respuesta de Gemini: ¡Hola! 👋
```

---

## ⚠️ Problemas Comunes

### Error: "GEMINI_API_KEY no encontrada"

**Causa:** El archivo `.env` no se está cargando

**Solución:**
1. Verifica que el archivo se llama exactamente `.env` (no `.env.txt`)
2. Verifica que está en la carpeta `backend/`
3. Reinicia el servidor backend

### Error: "Invalid API Key"

**Causa:** La API key es inválida o caducó

**Solución:**
1. Genera una nueva en https://aistudio.google.com/app/apikey
2. Actualiza `GEMINI_API_KEY` en `.env`
3. Reinicia el backend

### Error: "Resource exhausted"

**Causa:** Has excedido el límite gratuito de la API

**Solución:**
1. Espera unos minutos (los límites se resetean)
2. Considera usar `gemini-1.5-flash` en lugar de `gemini-1.5-pro` (más económico)
3. Revisa tu uso en: https://aistudio.google.com/app/apikey

### El backend no carga las variables

**Causa:** `python-dotenv` no está instalado

**Solución:**
```bash
cd backend
pip install python-dotenv
```

---

## 📋 Variables Requeridas vs Opcionales

### ✅ OBLIGATORIAS (El sistema no funcionará sin estas)

```env
# Base de datos
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=rendimiento_estudiantil

# Gemini (para IA)
GEMINI_API_KEY=tu_api_key

# Flask
SECRET_KEY=alguna_clave_segura
```

### 📦 OPCIONALES (El sistema funciona sin estas)

```env
# Configuración del modelo (usa defaults si no están)
GEMINI_MODEL=gemini-1.5-flash
GEMINI_MAX_TOKENS=8192
GEMINI_TEMPERATURE=0.7

# Configuración de archivos (usa defaults)
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=50MB

# CORS (usa defaults)
CORS_ORIGINS=http://localhost:3000
```

---

## 🚀 Inicio Rápido

### Si es tu primera vez:

1. **Copia el archivo de ejemplo:**
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Edita `.env` con tus datos:**
   ```env
   DB_PASSWORD=tu_password_mysql
   GEMINI_API_KEY=tu_api_key_de_gemini
   ```

3. **Verifica la configuración:**
   ```bash
   python test_nodo_digital.py
   ```

4. **Inicia el backend:**
   ```bash
   python run.py
   ```

---

## 🎯 Tu Configuración Actual

Basado en tu `.env` actual:

| Variable | Valor | Estado |
|----------|-------|--------|
| **GEMINI_API_KEY** | AIzaSyDapo...V94 | ✅ Configurada |
| **GEMINI_MODEL** | gemini-1.5-flash | ✅ Configurado |
| **DB_HOST** | localhost | ✅ Configurado |
| **DB_USER** | root | ✅ Configurado |
| **DB_PASSWORD** | ADMIN | ✅ Configurado |
| **DB_NAME** | rendimiento_estudiantil | ✅ Configurado |

**Todo está listo para usar!** 🎉

---

## 📞 ¿Necesitas Ayuda?

### Verificar que Gemini funciona:

```bash
cd backend
python -c "from app.services.academic.study_tools import StudyToolsService; print('✅ Gemini OK')"
```

### Ver todas las variables cargadas:

```bash
cd backend
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('Variables:', [k for k in os.environ.keys() if 'GEMINI' in k or 'DB_' in k])"
```

---

## 🔒 Seguridad

### ⚠️ IMPORTANTE:

1. **Nunca** compartas tu `GEMINI_API_KEY` públicamente
2. **Nunca** subas el archivo `.env` a GitHub
3. El archivo `.gitignore` ya está configurado para ignorar `.env`
4. Usa `.env.example` como plantilla (sin datos sensibles)

### Si expones tu API Key por error:

1. Ve a https://aistudio.google.com/app/apikey
2. Elimina la clave comprometida
3. Genera una nueva
4. Actualiza tu `.env`

---

¡Tu sistema está correctamente configurado con Gemini API! 🚀
