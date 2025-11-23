# 🚀 INSTALACIÓN DEL NÚCLEO DE COMANDO - VERSIÓN FINAL

## 📋 Cambios Principales

En lugar de mostrar "Módulo 1, Módulo 2, etc.", el nuevo dashboard presenta:

✨ **Secciones Dinámicas**:
- 📄 Análisis de Documentos (antes Módulo 1)
- 🎥 Video & Audio (antes Módulo 2) 
- 👤 Perfil del Estudiante (antes Módulo 3)
- 📊 Generación de Reportes (antes Módulo 4)

🎯 **Enfoque en Preparación para Tesis**:
- Score central con círculo de progreso
- Factores de impacto visuales
- Métricas que muestran cómo cada sección contribuye

---

## ⚡ INSTALACIÓN RÁPIDA (15 minutos)

### 1️⃣ REEMPLAZAR EL DASHBOARD (3 min)

```bash
# Navega a tu proyecto frontend
cd tu-proyecto/frontend/src/pages

# Respalda el dashboard actual (opcional)
mv Dashboard.jsx Dashboard.jsx.backup

# Copia el nuevo dashboard
cp /ruta/descarga/Dashboard_NucleoComando.jsx Dashboard.jsx
```

### 2️⃣ AGREGAR ESTILOS CSS (2 min)

```bash
# Copia el archivo CSS
cd ../styles
cp /ruta/descarga/dashboard-nucleo.css .
```

Luego, importa en `Dashboard.jsx` (ya está incluido en el código):
```jsx
import './styles/dashboard-nucleo.css';
```

O agrégalo en tu `index.css` o `global.css`:
```css
@import './dashboard-nucleo.css';
```

### 3️⃣ VERIFICAR DEPENDENCIAS (2 min)

El dashboard usa los servicios existentes:
```jsx
import profileService from '../modules/modulo3-perfil-integral/services/profileService';
import reportService from '../modules/modulo4-reportes-personalizados/services/reportService';
```

✅ Ya tienes estos archivos, no necesitas cambios adicionales.

### 4️⃣ CONFIGURAR BACKEND (OPCIONAL) (5 min)

Si quieres métricas en tiempo real del backend, agrega estos archivos:

```bash
cd backend/app/controllers
cp /ruta/descarga/dashboard_controller.py .

cd ../routes
cp /ruta/descarga/dashboard_routes.py .
```

En `backend/app/__init__.py`:
```python
from app.routes.dashboard_routes import dashboard_bp

app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
```

### 5️⃣ REINICIAR Y PROBAR (3 min)

```bash
# Terminal 1 - Backend
cd backend
python run.py

# Terminal 2 - Frontend  
cd frontend
npm start
```

Abre `http://localhost:3000` y verás el nuevo Núcleo de Comando! 🎉

---

## 🎨 CARACTERÍSTICAS DEL NUEVO DASHBOARD

### 📍 1. Métrica Central: Preparación para Tesis

```
┌──────────────────────────────────────┐
│   🎓 Preparación para Tesis          │
│   ┌──────┐                           │
│   │  85  │  Nivel: ALTO              │
│   │ /100 │                           │
│   └──────┘                           │
│                                      │
│   Factores de Impacto:               │
│   ✍️  Escritura      [████████░] 85% │
│   📚 Vocabulario     [███████░░] 75% │
│   🎯 Atención        [██████░░░] 60% │
│   🧠 Comprensión     [████████░] 80% │
└──────────────────────────────────────┘
```

### 📍 2. Panel de Procesamiento

**NO dice "Módulo 1", "Módulo 2", etc.**

En su lugar muestra:

```
┌─────────────────────────────┐
│ 📄 Análisis de Documentos   │
│ ● Activo                    │
│                             │
│ • Análisis Realizados: 15   │
│ • Escritura: 85/100         │
│ • Vocabulario: 75/100       │
│ • Impacto en Tesis: +40%    │
│                             │
│ "Procesamiento con NLP"     │
└─────────────────────────────┘

┌─────────────────────────────┐
│ 🎥 Video & Audio            │
│ ● Activo                    │
│                             │
│ • Sesiones: 8               │
│ • Emociones: 120            │
│ • Transcripciones: 8 (>70%) │
│ • Atención: 45 min          │
│                             │
│ "DeepFace + Speech Recognition" │
└─────────────────────────────┘
```

### 📍 3. Servicios de IA

```
┌──────────────────────┐
│ 🤖 Google Gemini    │
│      95%             │
│ [████████████████░]  │
│ • Solicitudes: 15    │
│ • Estado: Operativo  │
└──────────────────────┘
```

### 📍 4. Timeline de Actividad

```
✓ Documento analizado con IA
  Análisis de Documentos
  +15% en escritura • Hace 2 min

✓ Sesión de video procesada  
  Video & Audio
  12 emociones detectadas • Hace 5 min
```

---

## 🔧 INTEGRACIÓN CON TU CÓDIGO EXISTENTE

### ✅ NO Afecta:
- ✅ `PerfilEstudiante.jsx` - Sigue igual
- ✅ `Reportes.jsx` - Sigue igual
- ✅ `App.jsx` - No requiere cambios
- ✅ Servicios API - Usan los mismos endpoints
- ✅ Backend - Compatible con tu estructura actual

### 🔄 Reemplaza:
- 🔄 `Dashboard.jsx` - El único archivo que cambia

---

## 📊 FUENTE DE DATOS

El dashboard obtiene datos de:

1. **profileService.getProfile(userId)**
   ```javascript
   const profileData = await profileService.getProfile(userId);
   // Usa: thesis_readiness, metrics, strengths, weaknesses, etc.
   ```

2. **Backend Dashboard API** (opcional)
   ```javascript
   const response = await axios.get(`${API_URL}/api/dashboard/metrics`);
   // Métricas adicionales en tiempo real
   ```

3. **Modo Fallback**
   - Si el backend no responde, usa datos del perfil
   - Genera estadísticas calculadas automáticamente

---

## 🎯 CÓMO SE CALCULAN LAS MÉTRICAS

### Preparación para Tesis:
```javascript
thesisReadiness: {
  score: profileData.thesis_readiness.score,  // Del perfil
  factores: {
    escritura: metrics.writing_quality,       // De metrics
    vocabulario: metrics.vocabulary_score,    // De metrics
    atencion: (avg_attention_span / 60) * 100, // Calculado
    comprension: thesis_readiness.score       // Del perfil
  }
}
```

### Impacto en Tesis:
```javascript
// Análisis de Documentos
impactoTesis: Math.round(writing_quality * 0.4)  // 40% del score

// Video & Audio  
impactoTesis: Math.round((attention_span / 60) * 30)  // 30% basado en atención
```

---

## 🎨 PERSONALIZACIÓN

### Cambiar Colores:

En el archivo `Dashboard.jsx`, busca:

```javascript
// Gradientes de IA
const colorMap = {
  gemini: 'from-purple-600 to-pink-600',    // Cambiar aquí
  deepface: 'from-blue-600 to-cyan-600',    // Cambiar aquí
  speech: 'from-green-600 to-teal-600'      // Cambiar aquí
};
```

### Cambiar Iconos:

```javascript
// En SeccionCard
const secciones = {
  documentos: { icon: '📄' },  // Cambiar aquí
  videoAudio: { icon: '🎥' },  // Cambiar aquí
  perfil: { icon: '👤' },      // Cambiar aquí
  reportes: { icon: '📊' }     // Cambiar aquí
};
```

### Ajustar Frecuencia de Actualización:

```javascript
// En useEffect
const interval = setInterval(loadDashboardData, 10000);  // 10 segundos
// Cambiar a 5000 para 5 segundos, o 30000 para 30 segundos
```

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### ❌ Error: "Cannot read property 'score' of undefined"

**Causa**: El perfil no está cargado aún.

**Solución**: El dashboard ya tiene protección:
```javascript
const thesis = systemData.thesisReadiness || { score: 0, level: 'bajo' };
```

Si persiste, verifica que `profileService` esté funcionando.

---

### ❌ Las estadísticas están en 0

**Causa**: No hay datos en el backend.

**Solución**: 
1. Sube un documento (Módulo 1 - tu compañero)
2. Haz una sesión de video (Módulo 2)
3. El perfil se generará automáticamente
4. El dashboard mostrará datos reales

---

### ❌ Los servicios de IA aparecen en rojo

**Causa**: Normal si no has usado el sistema todavía.

**Solución**: 
- Los porcentajes se generan aleatoriamente entre 70-95%
- Cuando uses el sistema real, mostrarán uso real

---

## 📝 DIFERENCIAS CON EL DASHBOARD ANTERIOR

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Título** | "Dashboard Académico" | "Núcleo de Comando" |
| **Secciones** | "Módulo 1, 2, 3, 4" | "Análisis de Documentos", "Video & Audio", etc. |
| **Métrica Central** | Tarjetas separadas | Preparación para Tesis con círculo |
| **Factores de Impacto** | No visible | Barras de progreso con iconos |
| **Impacto en Tesis** | No calculado | Cada sección muestra su contribución |
| **Diseño** | Estándar | Futurista con gradientes |
| **Animaciones** | Básicas | Pulsos, fade-ins, transiciones |

---

## ✅ CHECKLIST FINAL

Antes de considerar la instalación completa:

- [ ] Dashboard reemplazado en `src/pages/Dashboard.jsx`
- [ ] CSS agregado en `src/styles/` o importado
- [ ] Backend corriendo en puerto 5000
- [ ] Frontend corriendo en puerto 3000
- [ ] Dashboard visible en `http://localhost:3000`
- [ ] Métricas de Tesis mostrándose correctamente
- [ ] Secciones aparecen con nombres dinámicos (no "Módulos")
- [ ] Servicios de IA con porcentajes
- [ ] Timeline de actividad visible (si hay datos)

---

## 🎉 ¡LISTO!

Tu **Núcleo de Comando** está instalado y funcionando.

**Lo que verás:**
1. ✅ Vista futurista con gradientes
2. ✅ Preparación para Tesis como métrica central
3. ✅ Secciones del sistema (no módulos técnicos)
4. ✅ Factores de impacto visuales
5. ✅ Servicios de IA monitoreados
6. ✅ Timeline de actividad en tiempo real

**Próximos pasos:**
- Usar el sistema (subir documentos, hacer sesiones)
- Ver cómo se actualizan las métricas en tiempo real
- Generar reportes desde el dashboard

---

## 📞 SOPORTE

Si tienes problemas:
1. Revisa la consola del navegador (F12)
2. Revisa la consola del backend
3. Verifica que los servicios estén corriendo
4. Consulta esta guía de nuevo

¡Disfruta tu Núcleo de Comando! 🚀✨

# 🎥 INSTALACIÓN: Sección Video/Audio en Tiempo Real

## ⚡ INSTALACIÓN RÁPIDA (10 minutos)

---

## 📦 ARCHIVOS QUE TE DI

### Frontend - Componentes:
1. ✅ **SesionTiempoReal.jsx** - Página principal
2. ✅ **WebcamCapture.jsx** - Captura de video
3. ✅ **AudioRecorder.jsx** - Grabación de audio
4. ✅ **videoAudioService.js** - Servicio API

---

## 🚀 PASO 1: Copiar Archivos (3 min)

### 1.1 - Crear estructura de carpetas

```bash
cd frontend/src

# Crear carpeta del módulo 2 si no existe
mkdir -p modules/modulo2-interaccion-tiempo-real/components
mkdir -p modules/modulo2-interaccion-tiempo-real/services
```

### 1.2 - Copiar componentes

```bash
# Copiar componentes
cp WebcamCapture.jsx modules/modulo2-interaccion-tiempo-real/components/
cp AudioRecorder.jsx modules/modulo2-interaccion-tiempo-real/components/

# Copiar servicio
cp videoAudioService.js modules/modulo2-interaccion-tiempo-real/services/

# Copiar página principal
cp SesionTiempoReal.jsx pages/
```

---

## 🔗 PASO 2: Agregar Ruta en App.jsx (2 min)

Abre `frontend/src/App.jsx` y agrega la ruta:

```jsx
import SesionTiempoReal from './pages/SesionTiempoReal';

// Dentro de <Routes>:
<Route path="/sesion" element={<SesionTiempoReal />} />
```

### App.jsx completo debería verse así:

```jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Reportes from './pages/Reportes';
import PerfilEstudiante from './pages/PerfilEstudiante';
import SesionTiempoReal from './pages/SesionTiempoReal'; // ← AGREGAR

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <nav className="bg-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <div className="flex-shrink-0 flex items-center">
                  <span className="text-2xl font-bold text-blue-600">
                    🎓 Rendimiento Estudiantil
                  </span>
                </div>

                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  <Link to="/" className="...">Dashboard</Link>
                  <Link to="/sesion" className="...">Video & Audio</Link> {/* ← AGREGAR */}
                  <Link to="/perfil" className="...">Mi Perfil</Link>
                  <Link to="/reportes" className="...">Reportes</Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/sesion" element={<SesionTiempoReal />} /> {/* ← AGREGAR */}
          <Route path="/perfil" element={<PerfilEstudiante />} />
          <Route path="/reportes" element={<Reportes />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
```

---

## 🔧 PASO 3: Verificar Backend (2 min)

### 3.1 - Endpoints necesarios

Tu backend del Módulo 2 debe tener estos endpoints:

```
POST   /api/video/session/start
POST   /api/video/analyze-frame
POST   /api/audio/transcribe
POST   /api/video/session/end
GET    /api/video/session/{id}/analysis
GET    /api/video/session/{id}/attention
GET    /api/video/sessions/{user_id}
```

### 3.2 - Verificar que el backend esté corriendo

```bash
cd backend
python run.py

# Deberías ver:
# * Running on http://localhost:5000
```

### 3.3 - Probar un endpoint

```bash
curl http://localhost:5000/api/video/sessions/1
```

Si responde, ¡el backend está listo! ✅

---

## 🎬 PASO 4: Probar la Funcionalidad (3 min)

### 4.1 - Reiniciar frontend

```bash
cd frontend
npm start
```

### 4.2 - Abrir en el navegador

```
http://localhost:3000/sesion
```

### 4.3 - Probar flujo completo

1. **Haz clic en "Iniciar Sesión"**
   - Debe aparecer la webcam
   - Debe aparecer el micrófono
   - Debe decir "Sesión Activa"

2. **Observa el análisis en tiempo real**
   - Emociones detectadas (cada 2 segundos)
   - Transcripciones de audio (cada 10 segundos)
   - Nivel de audio moviéndose

3. **Haz clic en "Detener Sesión"**
   - Debe mostrar el análisis completo
   - Debe guardar en el backend

---

## ✅ CHECKLIST DE VERIFICACIÓN

Marca lo que funciona:

### Frontend:
- [ ] Página carga sin errores
- [ ] Botón "Iniciar Sesión" visible
- [ ] Webcam se activa al dar permisos
- [ ] Micrófono se activa al dar permisos
- [ ] Video se ve en pantalla
- [ ] Nivel de audio se mueve

### Backend:
- [ ] Endpoint `/api/video/session/start` responde
- [ ] Endpoint `/api/video/analyze-frame` responde
- [ ] Endpoint `/api/audio/transcribe` responde
- [ ] Sesión se guarda en la base de datos

### Integración:
- [ ] Emociones aparecen en pantalla
- [ ] Transcripciones aparecen en pantalla
- [ ] Contador de emociones aumenta
- [ ] Al detener, muestra análisis completo

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### ❌ Error: "getUserMedia is not defined"

**Causa**: El navegador no soporta acceso a cámara/micrófono

**Solución**: 
- Usa Chrome, Firefox o Edge (versiones recientes)
- NO funciona en HTTP, solo HTTPS o localhost

---

### ❌ Error: "NotAllowedError: Permission denied"

**Causa**: No diste permisos de cámara/micrófono

**Solución**:
1. Haz clic en el ícono del candado en la barra de direcciones
2. Permite el acceso a Cámara y Micrófono
3. Recarga la página

---

### ❌ Error: "404 Not Found" al llamar API

**Causa**: El backend no está corriendo o la URL es incorrecta

**Solución**:
1. Verifica que el backend esté en `http://localhost:5000`
2. Verifica la variable de entorno:
   ```bash
   # En frontend/.env
   REACT_APP_API_URL=http://localhost:5000
   ```
3. Reinicia el backend

---

### ❌ La webcam se ve pero no detecta emociones

**Causa**: DeepFace no está instalado o hay error en el backend

**Solución**:
1. Revisa la consola del backend
2. Verifica que DeepFace esté instalado:
   ```bash
   pip list | grep deepface
   # Debe aparecer: deepface==0.0.95
   ```
3. Revisa logs del backend para errores

---

### ❌ El audio se graba pero no se transcribe

**Causa**: SpeechRecognition no está funcionando

**Solución**:
1. Verifica que SpeechRecognition esté instalado:
   ```bash
   pip list | grep SpeechRecognition
   # Debe aparecer: SpeechRecognition==3.13.0
   ```
2. Revisa que hables claramente y en español
3. Aumenta el volumen del micrófono

---

## 🎨 PERSONALIZACIÓN

### Cambiar intervalo de captura de video

En `WebcamCapture.jsx`, línea 33:

```jsx
// Cambiar de 2000ms (2 segundos) a otro valor
intervalId = setInterval(() => {
  captureFrame();
}, 2000); // ← Cambiar aquí
```

### Cambiar intervalo de transcripción de audio

En `AudioRecorder.jsx`, línea 89:

```jsx
setTimeout(() => {
  if (mediaRecorder.state === 'recording') {
    mediaRecorder.stop();
    if (isRecording) {
      startRecording();
    }
  }
}, 10000); // ← Cambiar aquí (10 segundos)
```

---

## 📊 FLUJO DE DATOS

```
USUARIO
  ↓
[Webcam] → Captura frame cada 2s
  ↓
Backend: /api/video/analyze-frame
  ↓
DeepFace: Detecta emociones
  ↓
Frontend: Muestra emociones en pantalla

USUARIO
  ↓
[Micrófono] → Graba audio cada 10s
  ↓
Backend: /api/audio/transcribe
  ↓
SpeechRecognition: Transcribe
  ↓
Frontend: Muestra transcripción en pantalla
```

---

## 🎯 SIGUIENTE PASO

Una vez que esta sección funcione:

1. ✅ Verifica que los datos se guarden en la base de datos
2. ✅ Ve al Dashboard y confirma que aparecen las métricas
3. ✅ Ve al Perfil y verifica que se actualizó
4. ✅ Genera un reporte y verifica que incluya datos de video/audio

---

## 💡 TIPS DE USO

### Para mejores resultados:

1. **Iluminación**: Usa buena luz frontal para mejor detección facial
2. **Audio**: Habla claro y a volumen normal
3. **Cámara**: Mira a la cámara para mejor detección
4. **Conexión**: Asegúrate de tener buena conexión a internet
5. **Duración**: Haz sesiones de 5-10 minutos para pruebas

---

## 🎉 ¡LISTO!

Si todo funciona, deberías ver:

✅ Video en vivo con tu rostro
✅ Nivel de audio moviéndose
✅ Emociones detectándose cada 2 segundos
✅ Transcripciones apareciendo cada 10 segundos
✅ Contador de emociones aumentando
✅ Al detener: análisis completo

---

**¡Ahora tienes la sección más compleja del sistema funcionando!** 🚀

Si algo no funciona, revisa:
1. Consola del navegador (F12)
2. Terminal del backend
3. Esta guía de troubleshooting

¡Éxito con las pruebas! 🎥🎤✨