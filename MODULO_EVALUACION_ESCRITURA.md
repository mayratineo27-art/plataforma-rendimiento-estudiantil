# 📝 Módulo de Evaluación de Escritura con IA

## Descripción General

Nuevo módulo integrado en el **Nodo Digital** que permite a los estudiantes subir documentos de escritura y recibir evaluación automática detallada usando **Gemini AI**.

### Características Principales

✅ **Evaluación Automática**: Análisis de gramática, coherencia, vocabulario y estructura  
✅ **Comparación de Versiones**: Sube versión anterior para ver tu progreso  
✅ **Reportes Detallados**: Scores, fortalezas, debilidades y recomendaciones específicas  
✅ **Múltiples Formatos**: Soporta TXT, PDF, DOCX y Markdown  
✅ **Métricas Avanzadas**: Conteo de palabras, legibilidad, vocabulario único  
✅ **Interfaz Intuitiva**: Diseño moderno con visualización clara de resultados  

---

## 🏗️ Arquitectura del Sistema

### Backend (Python/Flask)

#### 1. Servicio de Evaluación
**Archivo**: `backend/app/services/academic/writing_evaluator.py`

**Responsabilidades**:
- Extraer texto de diferentes formatos (TXT, PDF, DOCX)
- Calcular métricas básicas (palabras, oraciones, vocabulario, legibilidad)
- Comunicarse con Gemini AI para análisis profundo
- Generar reportes estructurados en JSON

**Métodos Principales**:

```python
# Extrae texto de un archivo
WritingEvaluator.extract_text(file_path: str) -> str

# Calcula métricas básicas
WritingEvaluator.calculate_basic_metrics(text: str) -> Dict

# Evalúa con IA (con/sin comparación)
WritingEvaluator.evaluate_with_ai(
    text: str, 
    previous_text: Optional[str] = None
) -> Dict

# Genera reporte completo
WritingEvaluator.generate_report(
    current_file: str,
    previous_file: Optional[str] = None,
    metadata: Optional[Dict] = None
) -> Dict
```

**Métricas Calculadas**:
- `word_count`: Total de palabras
- `sentence_count`: Total de oraciones
- `paragraph_count`: Total de párrafos
- `vocabulary_size`: Palabras únicas
- `long_word_count`: Palabras complejas (>7 caracteres)
- `avg_words_per_sentence`: Promedio palabras/oración
- `vocabulary_richness`: % de vocabulario único
- `readability_score`: Índice de legibilidad Flesch (0-100)

**Evaluación con IA (Gemini)**:
- `overall_score`: Puntuación general (0-100)
- `grammar_score`: Gramática y ortografía
- `coherence_score`: Coherencia y cohesión
- `vocabulary_score`: Riqueza de vocabulario
- `structure_score`: Organización del texto
- `strengths`: Lista de fortalezas
- `weaknesses`: Lista de áreas de mejora
- `recommendations`: Recomendaciones específicas
- `summary`: Resumen ejecutivo

Si se proporciona versión anterior, también incluye:
- `improvement_percentage`: % de mejora
- `improvements_made`: Lista de mejoras específicas

#### 2. Endpoint REST API
**Archivo**: `backend/app/routes/academic_routes.py`

**Ruta**: `POST /api/academic/tools/evaluate-writing`

**Parámetros** (multipart/form-data):
- `document` (File, requerido): Archivo actual a evaluar
- `previous_document` (File, opcional): Versión anterior para comparar
- `user_id` (int, opcional): ID del usuario
- `course_id` (int, opcional): ID del curso relacionado

**Respuesta Exitosa** (200):
```json
{
  "message": "Evaluación completada",
  "report": {
    "evaluated_at": "2025-11-28T10:30:00",
    "file_name": "ensayo_final.pdf",
    "metrics": {
      "current": {
        "word_count": 1250,
        "sentence_count": 45,
        "vocabulary_size": 380,
        "readability_score": 72.5
      },
      "previous": { /* si existe */ }
    },
    "evaluation": {
      "overall_score": 85,
      "grammar_score": 90,
      "coherence_score": 80,
      "vocabulary_score": 85,
      "structure_score": 88,
      "strengths": [...],
      "weaknesses": [...],
      "recommendations": [...],
      "summary": "..."
    }
  }
}
```

**Errores Posibles**:
- `400`: No se envió documento o formato inválido
- `503`: Servicio de evaluación no disponible
- `500`: Error interno al procesar

#### 3. Almacenamiento de Archivos
**Carpeta**: `backend/uploads/writing/`

**Convención de nombres**:
```
current_YYYYMMDD_HHMMSS_nombre_original.ext
previous_YYYYMMDD_HHMMSS_nombre_original.ext
```

Los archivos se guardan con timestamp único para evitar colisiones.

---

### Frontend (React)

#### 1. Componente Principal
**Archivo**: `frontend/src/components/WritingEvaluator.jsx`

**Props**:
- `userId` (number, default: 1): ID del usuario actual
- `courseId` (number, optional): ID del curso relacionado

**Estados Internos**:
```javascript
const [currentFile, setCurrentFile] = useState(null);
const [previousFile, setPreviousFile] = useState(null);
const [loading, setLoading] = useState(false);
const [report, setReport] = useState(null);
const [error, setError] = useState(null);
```

**Flujo de Usuario**:
1. Usuario selecciona documento actual (obligatorio)
2. Usuario selecciona documento anterior (opcional)
3. Usuario hace click en "Evaluar mi Escritura"
4. Sistema muestra loading mientras procesa
5. Sistema muestra reporte detallado con visualizaciones

**Visualizaciones del Reporte**:
- **Score General**: Tarjeta grande con puntuación 0-100
- **Badge de Mejora**: Si hay versión anterior, muestra % de progreso
- **Grid de Scores**: 4 métricas principales (gramática, coherencia, vocabulario, estructura)
- **Métricas del Documento**: Palabras, oraciones, vocabulario, legibilidad
- **Fortalezas**: Lista con checkmarks verdes
- **Áreas de Mejora**: Lista con alertas naranjas
- **Mejoras Realizadas**: Si hay comparación, lista de cambios positivos
- **Recomendaciones**: Sugerencias específicas con íconos de bombilla
- **Resumen**: Texto narrativo del análisis

#### 2. Integración con Dashboard
**Archivo**: `frontend/src/pages/AcademicDashboard.jsx`

Nueva pestaña "Escritura" agregada con ícono FileCheck.

**Posición**: 7ma pestaña, después de "Evolución"

---

## 🚀 Cómo Usar

### Para Usuarios

1. **Accede al Nodo Digital**
   - Ve a http://localhost:3000/analisis
   - Click en la pestaña "📝 Escritura"

2. **Sube tu Documento**
   - Click en el área de carga para seleccionar tu archivo
   - Formatos aceptados: `.txt`, `.pdf`, `.docx`, `.md`
   - Tamaño máximo recomendado: 10 MB

3. **Opcional: Sube Versión Anterior**
   - Si quieres ver tu progreso, sube una versión anterior
   - Debe ser del mismo tipo de documento

4. **Evalúa**
   - Click en "Evaluar mi Escritura"
   - Espera 10-30 segundos (depende del tamaño)

5. **Revisa tu Reporte**
   - Score general y por categorías
   - Métricas detalladas
   - Fortalezas y debilidades
   - Recomendaciones específicas

6. **Evalúa Otro**
   - Click en "Evaluar Otro Documento" para empezar de nuevo

### Para Desarrolladores

#### Instalar Dependencias Adicionales (Backend)

Si aún no están instaladas:

```bash
cd backend
pip install python-docx  # Para soporte DOCX
```

Las demás dependencias (PyPDF2/pdfplumber, google-generativeai) ya están instaladas.

#### Verificar que el Backend está Corriendo

```bash
cd backend
python run.py
```

Deberías ver en consola:
```
✅ WritingEvaluator disponible
```

#### Verificar que el Frontend está Corriendo

```bash
cd frontend
npm start
```

Navega a http://localhost:3000/analisis y verifica que existe la pestaña "Escritura".

#### Probar el Endpoint Directamente (Postman/cURL)

```bash
curl -X POST http://localhost:5000/api/academic/tools/evaluate-writing \
  -F "document=@mi_documento.txt" \
  -F "user_id=1"
```

---

## 🔧 Configuración

### Variables de Entorno (Backend)

Archivo: `backend/.env`

```env
# API de Gemini (requerido)
GEMINI_API_KEY=AIzaSyCsfK6eb3KIyF3DkKUhFoPI5OQEva676AY
GEMINI_MODEL=gemini-2.0-flash-exp

# Flask
FLASK_DEBUG=True
```

### Personalizar Prompts de Evaluación

Edita `backend/app/services/academic/writing_evaluator.py`, método `evaluate_with_ai()`.

Los prompts actuales están optimizados para:
- Español académico
- Escritura universitaria
- Feedback constructivo y específico

---

## 📊 Ejemplos de Uso

### Ejemplo 1: Evaluar Ensayo Simple

**Entrada**:
```
Archivo: ensayo_clima.txt (800 palabras)
```

**Salida**:
```json
{
  "overall_score": 78,
  "grammar_score": 85,
  "coherence_score": 70,
  "vocabulary_score": 80,
  "structure_score": 75,
  "strengths": [
    "Vocabulario técnico apropiado",
    "Ideas bien fundamentadas"
  ],
  "weaknesses": [
    "Falta de conectores entre párrafos",
    "Conclusión muy breve"
  ],
  "recommendations": [
    "Usar conectores: sin embargo, por lo tanto, además",
    "Ampliar la conclusión con implicaciones"
  ]
}
```

### Ejemplo 2: Comparar Versiones

**Entrada**:
```
Archivo actual: ensayo_v2.pdf (1200 palabras)
Archivo anterior: ensayo_v1.pdf (900 palabras)
```

**Salida adicional**:
```json
{
  "improvement_percentage": 18,
  "improvements_made": [
    "Corrigió 5 errores ortográficos",
    "Mejoró la introducción con contexto histórico",
    "Añadió 3 ejemplos concretos",
    "Vocabulario más variado: 300 → 420 palabras únicas"
  ]
}
```

---

## 🐛 Troubleshooting

### Error: "Servicio de evaluación de escritura no disponible"

**Causa**: WritingEvaluator no se pudo importar en el backend.

**Solución**:
1. Verifica que existe `backend/app/services/academic/writing_evaluator.py`
2. Reinicia el backend
3. Revisa la consola del backend para ver el error específico

### Error: "Formato no soportado"

**Causa**: Archivo con extensión no permitida.

**Solución**: Usa solo `.txt`, `.pdf`, `.docx` o `.md`

### Error: "No se pudo extraer texto del PDF"

**Causa**: PDF con imágenes escaneadas o protegido.

**Solución**: Convierte el PDF a texto plano o usa un PDF generado digitalmente.

### Scores muy bajos sin razón aparente

**Causa**: El modelo de IA puede ser muy crítico o el texto es muy corto.

**Solución**:
- Asegúrate de que el documento tiene al menos 200 palabras
- Revisa el `summary` para entender la evaluación
- Los scores de fallback (sin IA) son conservadores

### No aparece la pestaña "Escritura"

**Causa**: Frontend no se recargó después de los cambios.

**Solución**:
1. Haz Ctrl+Shift+R para recargar sin caché
2. Verifica que no hay errores en la consola del navegador (F12)
3. Si persiste, reinicia el servidor de desarrollo de React

---

## 🔒 Seguridad

### Validaciones Implementadas

✅ **Extensión de archivo**: Solo formatos permitidos  
✅ **Nombres únicos**: Timestamp para evitar colisiones  
✅ **Límite de tamaño**: (Configurable en el frontend/backend)  
✅ **Sanitización**: Los nombres de archivo se limpian automáticamente  

### Recomendaciones Adicionales

Para producción, considera:
- Límite de tamaño de archivo (ej: 10 MB)
- Rate limiting por usuario
- Escaneo antivirus de archivos subidos
- Eliminar archivos después de procesarlos
- Autenticación/autorización robusta

---

## 📈 Métricas y Performance

### Tiempos de Respuesta Típicos

- **Archivo TXT (1000 palabras)**: 5-10 segundos
- **Archivo PDF (5 páginas)**: 10-20 segundos
- **Archivo DOCX (3000 palabras)**: 15-30 segundos

Los tiempos dependen de:
- Tamaño del archivo
- Velocidad de la API de Gemini
- Carga del servidor

### Uso de Tokens (Gemini)

- **Sin comparación**: ~1000-2000 tokens por evaluación
- **Con comparación**: ~2000-4000 tokens por evaluación

Monitorea tu cuota de la API de Gemini en: https://aistudio.google.com/apikey

---

## 🛠️ Extensiones Futuras

Ideas para mejorar el módulo:

1. **Guardar Historial de Evaluaciones**
   - Tabla en BD para guardar reportes
   - Ver evolución a lo largo del tiempo

2. **Comparación Múltiple**
   - Permitir comparar 3+ versiones
   - Gráficos de progreso

3. **Estilos de Evaluación**
   - Académico formal
   - Creativo/literario
   - Técnico/científico

4. **Exportar Reportes**
   - PDF con diseño profesional
   - Compartir por email

5. **Corrección Inline**
   - Mostrar errores específicos en el texto
   - Sugerencias de corrección en tiempo real

6. **Integración con Cursos**
   - Vincular evaluaciones a tareas específicas
   - Rúbricas personalizadas por profesor

---

## 📝 Changelog

### Versión 1.0.0 (2025-11-28)

**Añadido**:
- ✅ Servicio completo de evaluación de escritura
- ✅ Endpoint REST API para subir y evaluar documentos
- ✅ Componente React con interfaz intuitiva
- ✅ Soporte para TXT, PDF, DOCX, MD
- ✅ Comparación de versiones con cálculo de mejora
- ✅ Métricas avanzadas (legibilidad, vocabulario, etc.)
- ✅ Evaluación con Gemini AI
- ✅ Fallback heurístico si IA no disponible
- ✅ Visualización detallada de reportes
- ✅ Integración con pestaña "Escritura" en Nodo Digital

---

## 👥 Créditos

- **Backend**: Python, Flask, SQLAlchemy, Google Gemini AI
- **Frontend**: React, Tailwind CSS, Lucide Icons
- **Procesamiento de archivos**: PyPDF2, python-docx
- **Análisis de texto**: Heurísticas propias + Gemini AI

---

## 📞 Soporte

Para problemas o preguntas:
1. Revisa esta documentación
2. Verifica los logs del backend (debug=True)
3. Revisa la consola del navegador (F12)
4. Contacta al equipo de desarrollo

---

**¡Ahora los estudiantes pueden mejorar su escritura con feedback instantáneo! 🎉**
