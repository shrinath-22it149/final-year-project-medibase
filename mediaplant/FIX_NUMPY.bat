@echo off
title Fix + Run MediPlant AI
cd /d "%~dp0"
color 0E

echo  ================================================
echo    MediPlant AI - Install Fix
echo  ================================================
echo.

echo [1/5] Installing compatible NumPy for Python 3.13...
pip install "numpy>=2.1.0" --only-binary=:all: --quiet
python -c "import numpy; print('  numpy', numpy.__version__, '- OK')"
if errorlevel 1 (
    pip install numpy --only-binary=:all: --quiet
    python -c "import numpy; print('  numpy installed')"
)

echo [2/5] Installing Pillow...
pip install "Pillow>=10.4.0" --only-binary=:all: --quiet
python -c "import PIL; print('  Pillow', PIL.__version__, '- OK')"

echo [3/5] Installing Streamlit...
pip install "streamlit>=1.40.0" --quiet
python -c "import streamlit; print('  streamlit', streamlit.__version__, '- OK')"

echo [4/5] Installing remaining packages...
pip install "pandas>=2.2.0" --only-binary=:all: --quiet
pip install "plotly>=5.24.0" --quiet
pip install "matplotlib>=3.9.0" --only-binary=:all: --quiet
pip install "scikit-learn>=1.5.0" --only-binary=:all: --quiet
pip install "scipy>=1.14.0" --only-binary=:all: --quiet
pip install "seaborn>=0.13.2" --quiet
pip install "fpdf2>=2.8.0" --quiet
pip install "bcrypt>=4.2.0" --quiet
pip install "PyYAML>=6.0.2" --quiet
pip install "opencv-python-headless>=4.10.0" --quiet
pip install "google-generativeai>=0.8.0" --quiet

echo [5/5] Verifying all key imports...
python -c "
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import streamlit
import PIL
import plotly
import cv2
print('  numpy     :', np.__version__)
print('  streamlit :', streamlit.__version__)
print('  pandas    :', pd.__version__)
print('  Pillow    :', PIL.__version__)
print('  plotly    :', plotly.__version__)
print('  opencv    :', cv2.__version__)
print()
print('  ALL PACKAGES OK!')
"

echo.
echo  ================================================
echo    Starting MediPlant AI...
echo    Open browser: http://localhost:8501
echo  ================================================
echo.

set PYTHONWARNINGS=ignore::RuntimeWarning
set TF_CPP_MIN_LOG_LEVEL=3
set PYTHONPATH=%~dp0
streamlit run app.py --logger.level=error
pause
