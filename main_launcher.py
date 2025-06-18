import subprocess
import sys
import os

def resource_path(relative_path):
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho nela
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

target = resource_path("app/cda_webapp.py")

subprocess.Popen([sys.executable, "-m", "streamlit", "run", target])
