@echo off
REM ============================================
REM Script de Instalación Completa de Dependencias
REM Plataforma Integral de Rendimiento Estudiantil
REM ============================================

echo ====================================
echo INSTALACION DE DEPENDENCIAS
echo Plataforma Rendimiento Estudiantil
echo ====================================
echo.

REM Verificar que el venv está activo
python -c "import sys; sys.exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)"
if errorlevel 1 (
    echo ERROR: El entorno virtual no esta activo
    echo Por favor ejecuta: venv\Scripts\activate.bat
    pause
    exit /b 1
)

echo [1/10] Actualizando pip, setuptools y wheel...
python -m pip install --upgrade pip setuptools wheel
echo.

echo [2/10] Instalando Flask y Core...
pip install Flask==3.1.2 flask-cors==6.0.1 Werkzeug==3.1.3
echo.

echo [3/10] Instalando Database...
pip install SQLAlchemy==2.0.43 mysql-connector-python==9.4.0 PyMySQL==1.1.0 Flask-SQLAlchemy==3.1.1 Flask-Migrate==4.0.5
echo.

echo [4/10] Instalando NumPy (base para muchos paquetes)...
pip install numpy==2.2.6
echo.

echo [5/10] Instalando procesamiento de documentos...
pip install PyPDF2==3.0.1 python-docx==1.1.0 Pillow==11.3.0
pip install --no-build-isolation PyMuPDF==1.24.0
echo.

echo [6/10] Instalando OpenCV...
pip install opencv-python==4.12.0.88
REM pip install opencv-contrib-python==4.12.0.88
echo.

echo [7/10] Instalando TensorFlow y DeepFace (esto tomara varios minutos)...
pip install tensorflow==2.20.0
pip install tf-keras==2.20.1
pip install deepface==0.0.95
echo.

echo [8/10] Instalando NLP...
pip install spacy==3.7.2
echo.

echo [9/10] Instalando Audio...
pip install SpeechRecognition==3.13.0 pydub==0.25.1
echo PyAudio requiere instalacion manual - ver instrucciones
echo.

echo [10/10] Instalando el resto de dependencias...
pip install google-generativeai==0.4.6
pip install python-pptx==0.6.23 openpyxl==3.1.2
pip install python-dotenv==1.0.0 requests==2.31.0 Jinja2==3.1.6
pip install PyJWT==2.8.0 bcrypt==4.1.2 cryptography==41.0.7
pip install pytest==8.4.2 pytest-cov==7.0.0 pytest-flask==1.3.0 coverage==7.10.7
pip install colorlog==6.8.2 python-json-logger==2.0.7
pip install watchdog==4.0.0 python-dateutil==2.9.0.post0 pytz==2025.2
pip install httpx==0.26.0 aiohttp==3.9.1
pip install pandas==2.3.3 scipy==1.12.0
pip install gunicorn==23.0.0
pip install black==24.1.1 flake8==7.0.0 autopep8==2.0.4
echo.

echo ====================================
echo INSTALACION COMPLETADA
echo ====================================
echo.
echo Descargando modelo de spaCy...
python -m spacy download es_core_news_md
echo.

echo ====================================
echo RESUMEN DE INSTALACION
echo ====================================
pip list
echo.

echo ====================================
echo NOTAS IMPORTANTES:
echo ====================================
echo 1. PyAudio requiere instalacion manual para Windows
echo 2. Ejecuta: pip install pipwin
echo 3. Luego: pipwin install pyaudio
echo.
echo Presiona cualquier tecla para salir...
pause > nul