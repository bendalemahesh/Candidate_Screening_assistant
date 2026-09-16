@echo off
echo =========================================
echo  Starting Recruiter AI - FastAPI Backend
echo =========================================
cd /d "%~dp0"
call .venv\Scripts\activate.bat 2>nul || echo [INFO] No .venv found, using system Python
cd App
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
pause
