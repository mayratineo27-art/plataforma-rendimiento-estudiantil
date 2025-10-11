@echo off
REM ============================================
REM Completar Instalación - Paquetes Faltantes
REM ============================================

echo ====================================
echo COMPLETANDO INSTALACION
echo ====================================
echo.

echo [1/4] Instalando spaCy...
pip install spacy==3.7.2
echo.

echo [2/4] Descargando modelo de spaCy en espanol...
python -m spacy download es_core_news_md
echo.

echo [3/4] Instalando Google Gemini API...
pip install google-generativeai==0.4.6
echo.

echo [4/4] Intentando instalar PyAudio...
pip install pipwin
pipwin install pyaudio
echo.

echo ====================================
echo VERIFICACION FINAL
echo ====================================
echo.

echo Verificando imports criticos...
echo.

python -c "import flask; print('[OK] Flask:', flask.__version__)"
python -c "import sqlalchemy; print('[OK] SQLAlchemy:', sqlalchemy.__version__)"
python -c "import cv2; print('[OK] OpenCV:', cv2.__version__)"
python -c "import tensorflow; print('[OK] TensorFlow:', tensorflow.__version__)"
python -c "import deepface; print('[OK] DeepFace instalado')"
python -c "import spacy; print('[OK] spaCy:', spacy.__version__)"
python -c "import google.generativeai as genai; print('[OK] Google Gemini instalado')"
python -c "import PyPDF2; print('[OK] PyPDF2:', PyPDF2.__version__)"
python -c "from pptx import Presentation; print('[OK] python-pptx instalado')"
python -c "import pandas; print('[OK] Pandas:', pandas.__version__)"
python -c "import docx; print('[OK] python-docx instalado')"
python -c "import speech_recognition; print('[OK] SpeechRecognition:', speech_recognition.__version__)"
python -c "import pydub; print('[OK] Pydub instalado')"

echo.
echo Intentando importar PyAudio...
python -c "import pyaudio; print('[OK] PyAudio instalado')" 2>nul || echo [WARN] PyAudio no instalado - instalar manualmente si es necesario

echo.
echo ====================================
echo INSTALACION COMPLETA
echo ====================================
echo.
echo Paquetes instalados:
pip list | find /C "Package"
echo.
echo Para ver la lista completa: pip list
echo.
pause