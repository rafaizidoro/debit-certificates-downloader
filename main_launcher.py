import subprocess
import sys
import os
import hashlib

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller onefile extraction
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def print_separator(title):
    print("\n" + "="*10 + f" {title} " + "="*30)

def hash_file(path):
    try:
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        return f"<Erro ao calcular hash: {e}>"

def main():
    print_separator("DIAGNÓSTICO DO LAUNCHER")
    print(f"📦 Empacotado: {'Sim' if getattr(sys, 'frozen', False) else 'Não'}")
    print(f"📁 Diretório atual: {os.getcwd()}")
    print(f"🐍 Python em uso: {sys.executable}")

    if os.environ.get("CDA_LAUNCHER_RUNNING") == "1":
        print_separator("PROTEÇÃO CONTRA LOOP")
        print("⚠️ Execução recursiva detectada. Abortando.")
        input("\nPressione Enter para fechar...")
        return
    os.environ["CDA_LAUNCHER_RUNNING"] = "1"

    # Resolve caminho do app
    target = resource_path("app/cda_webapp.py")
    print_separator("ALVO (SCRIPT STREAMLIT)")
    print(f"🎯 Caminho para app: {target}")
    print(f"📂 Existe? {'✅ Sim' if os.path.exists(target) else '❌ Não'}")
    print(f"🔒 Hash MD5: {hash_file(target)}")

    # Verifica se o launcher e o app são o mesmo arquivo
    launcher_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
    launcher_hash = hash_file(launcher_path)
    if launcher_hash == hash_file(target):
        print("🚨 O launcher e o script do Streamlit são o MESMO ARQUIVO.")
        print("💥 Isso causará execução recursiva infinita!")
        input("\nPressione Enter para fechar...")
        return
    else:
        print("✅ O launcher e o script Streamlit são arquivos distintos.")

    print_separator("EXECUTANDO STREAMLIT")

    try:
        # Caminho do Python real se empacotado, senão usa sys.executable
        if getattr(sys, 'frozen', False):
            python_executable = os.path.join(sys._MEIPASS, 'python.exe')
        else:
            python_executable = sys.executable

        subprocess.Popen([python_executable, "-m", "streamlit", "run", target])
    
    except Exception as e:
        print(f"❌ Erro ao rodar Streamlit: {e}")

    input("\n✅ Aplicação finalizada. Pressione Enter para fechar...")


if __name__ == "__main__":
    main()
