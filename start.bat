@echo off
echo ==========================================
echo   Kokborok NLP App - Starting Servers
echo ==========================================

echo.
echo [1/2] Starting Backend (Flask API on port 5000)...
start "Backend - Flask API" cmd /k "cd /d K:\model\content\xlm_pos_model_phase3\final\backend && python app.py"

echo.
echo [2/2] Starting Frontend (HTTP server on port 8001)...
timeout /t 3 /nobreak >nul
start "Frontend - HTTP Server" cmd /k "cd /d K:\model\content\xlm_pos_model_phase3\final\frontend && python -m http.server 8001"

echo.
echo ==========================================
echo   Both servers starting!
echo.
echo   Wait ~30 seconds for model to load, then:
echo   Open http://localhost:8001 in your browser
echo ==========================================
pause
