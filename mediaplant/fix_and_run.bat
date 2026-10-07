@echo off
title MediPlant AI - Fix & Run
echo.
echo  =============================================
echo    MediPlant AI - Fixing NumPy Crash
echo  =============================================
echo.

echo [Step 1] Uninstalling broken NumPy 2.x...
pip uninstall numpy -y

echo.
echo [Step 2] Installing stable NumPy 1.26.4 (Windows tested)...
pip install "numpy==1.26.4" --only-binary=:all:

echo.
echo [Step 3] Fixing Streamlit version (compatible with numpy 1.26)...
pip uninstall streamlit -y
pip install "streamlit==1.35.0" --quiet

echo.
echo [Step 4] Fixing Pillow to compatible version...
pip uninstall Pillow -y
pip install "Pillow==10.4.0" --only-binary=:all: --quiet

echo.
echo [Step 5] Verify NumPy works...
python -c "import numpy; print('  OK  numpy', numpy.__version__)"
if errorlevel 1 (
    echo  ERROR: NumPy still broken. Try running as Administrator.
    pause
    exit
)

echo.
echo [Step 6] Verify Streamlit works...
python -c "import streamlit; print('  OK  streamlit', streamlit.__version__)"

echo.
echo  =============================================
echo    Starting MediPlant AI...
echo    Open http://localhost:8501 in browser
echo  =============================================
echo.
streamlit run app.py --server.enableCORS=true --server.enableXsrfProtection=false
pause
