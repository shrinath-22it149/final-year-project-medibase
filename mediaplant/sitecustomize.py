"""Auto-loaded by Python - suppresses NumPy MINGW warnings before any import."""
import warnings
import os
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", message=".*MINGW.*")
warnings.filterwarnings("ignore", message=".*invalid value.*")
warnings.filterwarnings("ignore", message=".*exp2.*")
warnings.filterwarnings("ignore", message=".*nextafter.*")
warnings.filterwarnings("ignore", message=".*log10.*")
os.environ.setdefault("PYTHONWARNINGS", "ignore::RuntimeWarning")
