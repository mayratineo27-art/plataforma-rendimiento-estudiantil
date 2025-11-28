@echo off
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║         REINICIAR BACKEND CON NUEVO ENDPOINT                  ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo 🔴 INSTRUCCIONES:
echo.
echo 1. Ve a la terminal donde está corriendo el backend
echo 2. Presiona Ctrl+C para DETENERLO
echo 3. Ejecuta este archivo: reiniciar_backend.bat
echo.
echo O ejecuta manualmente:
echo    cd backend
echo    python run.py
echo.
echo Cuando veas esto, estará listo:
echo    ✅ WritingEvaluator disponible
echo    ✅ Academic routes: /api/academic
echo    POST /api/academic/tools/evaluate-writing
echo.
pause
cd /d "%~dp0"
cd backend
python run.py
