@echo off
echo =========================================
echo  Starting Recruiter AI - Streamlit App
echo =========================================
cd /d "%~dp0"
call .venv\Scripts\activate.bat 2>nul || echo [INFO] No .venv found, using system Python
cd App
streamlit run app.py
pause
