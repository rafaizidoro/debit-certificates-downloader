# 📄 STREAMLIT WEB APP FOR CDA DOWNLOADER
# THIS APP ALLOWS UPLOADING A LIST OF CDAS AND DOWNLOADING THEM VIA SITAFE AUTOMATION

# IMPORTS
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Tuple, Union
from io import BytesIO
import sys
import os
sys.path.append(os.path.dirname(__file__))

from logic_certificates_downloader import run_download_from_file

# BASE_DIR DEFINITION:
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# 🔍 VALIDATE CSV FUNCTION
def validate_csv_structure(file_obj: BytesIO, required_column: str = "cda") -> Tuple[bool, Union[pd.DataFrame, str]]:
    try:
        df = pd.read_csv(file_obj, encoding='utf-8-sig', dtype={required_column: str})
        if required_column not in df.columns:
            return False, f"❌ O arquivo precisa conter uma coluna '{required_column}'."
        df[required_column] = df[required_column].astype(str)  # 🗫️ segurança extra
        return True, df
    except Exception as e:
        return False, f"❌ Erro carregando o arquivo: {e}"

# 🔧 SETUP STREAMLIT PAGE CONFIGURATION
st.set_page_config(page_title="Download de CDAs", layout="centered", page_icon="📄")
st.title("📄 Download de CDAs")
st.markdown("Carregue sua lista de CDAs e informe suas credenciais para iniciar o download.")

# 🔐 USER CREDENTIALS
username: str = st.text_input("👤 CPF", type="default")
password: str = st.text_input("🔒 Senha do SitafeWeb", type="password")

# 📄 UPLOAD CSV FILE
uploaded_file = st.file_uploader("📂 Carregue aqui sua lista de CDAs (.txt ou .csv)", type=["txt", "csv"])
st.caption("Arraste e solte o arquivo aqui ou clique para selecionar. Tamanho máximo: 200MB.")

# 🗁 DEFINE DEFAULT DOWNLOAD FOLDER TO USER DOWNLOADS
default_download_path: str = str(Path.home() / "Downloads" / "CDAs")
st.markdown(f"📂 Os arquivos serão salvos em: `{default_download_path}`")

# 📅 CHECK IF FILE IS UPLOADED AND RUN VALIDATION
if uploaded_file is not None:
    st.success("Arquivo carregado com sucesso!")

    buffer = BytesIO(uploaded_file.read())
    is_valid, result = validate_csv_structure(buffer)
    buffer.seek(0)

    if is_valid:
        df_uploaded = result
        st.dataframe(df_uploaded[["cda"]].head(10))

        # ▶️ Show download button only if valid
        if st.button("▶️ Baixar CDAs"):
            if not username or not password:
                st.error("⚠️ Por favor, preencha todos os campos obrigatórios.")
            else:
                st.info("🔄 Iniciando serviço...")

                try:
                    # 📂 Save file temporarily
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    temp_path = os.path.join(BASE_DIR, f"temp_cdalist_{timestamp}.csv")

                    buffer.seek(0)  # ⬇️ Rewind buffer before saving
                    with open(temp_path, "wb") as f:
                        f.write(buffer.read())

                    # 📋 Status placeholder
                    status_placeholder = st.empty()
                    def update_status(index, total, cda_number):
                        status_placeholder.info(f"🔄 Processadas {index} de {total}: CDA {cda_number}...")

                    # ⚙️ Run the main automation
                    if getattr(sys, 'frozen', False):
                        os.environ["STREAMLIT_RUN"] = "1"
                    st.info("⬇️ Acessando SitafeWeb e fazendo download das CDAs...")
                    total, success_count, log_path, archive_folder = run_download_from_file(
                        file_path=temp_path,
                        username=username,
                        password=password,
                        download_dir=default_download_path,
                        update_callback=update_status
                    )

                    # 🧹 Delete temporary CSV file after processing
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                        
                    # ✅ Show results
                    st.write("✅ Processo finalizado.")
                    st.write(f"📁 Pasta de download: `{archive_folder}`")
                    st.write(f"📜 Relatório gerado: `{log_path}`")

                    try:
                        df_log = pd.read_csv(log_path)
                        st.dataframe(df_log)
                        st.subheader("📊 Relatório de Execução")                        
                        with open(log_path, "rb") as f:
                            st.download_button("⬇️ Baixar Relatório", f, file_name=os.path.basename(log_path), mime="text/csv")
                    except Exception as e:
                        st.warning(f"⚠️ Falha ao carregar log: {e}")

                    if success_count == 0:
                        st.error("❌ Nenhuma CDA foi baixada com sucesso.")
                    else:
                        st.success(f"✅ {success_count} de {total} CDAs baixadas com sucesso.")

                except Exception as e:
                    st.error(f"Erro ao executar a automação: {e}")

