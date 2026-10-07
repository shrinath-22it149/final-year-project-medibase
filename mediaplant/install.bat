@echo off
title MediPlant AI Installer
echo.
echo  =============================================
echo    MediPlant AI - Package Installer
echo    Python 3.13 + Windows Compatible
echo  =============================================
echo.

python -m pip install --upgrade pip --quiet

echo [1/9] Uninstalling any broken packages...
pip uninstall numpy Pillow streamlit -y --quiet 2>nul

echo [2/9] Installing NumPy 1.26.4 (stable Windows build)...
pip install "numpy==1.26.4" --only-binary=:all: --quiet
if errorlevel 1 (
    echo  ERROR: NumPy install failed. Try running as Administrator.
    pause & exit
)
python -c "import numpy; print('  OK  numpy', numpy.__version__)"

echo [3/9] Installing Pillow...
pip install "Pillow==10.4.0" --only-binary=:all: --quiet

echo [4/9] Installing Streamlit...
pip install "streamlit==1.35.0" --quiet

echo [5/9] Installing TensorFlow...
pip install "tensorflow>=2.20.0" --quiet

echo [6/9] Installing OpenCV...
pip install "opencv-python-headless==4.10.0.84" --quiet

echo [7/9] Installing data/chart libraries...
pip install "pandas==2.2.3" "plotly==5.24.1" "matplotlib==3.9.4" --quiet
pip install "scikit-learn==1.5.2" "scipy==1.14.1" "seaborn==0.13.2" --quiet

echo [8/9] Installing utilities...
pip install "fpdf2==2.8.1" "bcrypt==4.2.1" "PyYAML==6.0.2" --quiet

echo [9/9] Installing AI chatbot library...
pip install "google-generativeai==0.8.3" --quiet

echo.
echo  ============ Verification ============
python -c "import numpy;     print('  OK  numpy',     numpy.__version__)"
python -c "import streamlit; print('  OK  streamlit', streamlit.__version__)"
python -c "import PIL;       print('  OK  Pillow',    PIL.__version__)"
python -c "import pandas;    print('  OK  pandas',    pandas.__version__)"
python -c "import plotly;    print('  OK  plotly',    plotly.__version__)"
python -c "import cv2;       print('  OK  opencv',    cv2.__version__)"
python -c "import fpdf;      print('  OK  fpdf2')"
echo.
echo  =============================================
echo    Done! Now double-click run.bat to start
echo  =============================================
pause
