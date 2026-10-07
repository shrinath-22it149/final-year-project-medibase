@echo off
title MediPlant AI (Medibase)
cd /d "%~dp0"

REM Suppress runtime warnings at OS level
set PYTHONWARNINGS=ignore
set TF_CPP_MIN_LOG_LEVEL=3
set TF_ENABLE_ONEDNN_OPTS=0
set MPLBACKEND=Agg

echo =============================================
echo   🌿 MediPlant AI (Medibase) - Starting...
echo   Open: http://localhost:8501
echo =============================================
echo.

if exist "venv\Scripts\streamlit.exe" (
    call venv\Scripts\activate.bat
    streamlit run app.py --logger.level=error
) else (
    streamlit run app.py --logger.level=error
)
pause
