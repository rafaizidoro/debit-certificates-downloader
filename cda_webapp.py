# 📄 Streamlit Web App for CDA Manager
# This app allows uploading a list of CDAs and downloading them via Sitafe automation

import streamlit as st
import os
import pandas as pd
from datetime import datetime
from pathlib import Path
from debit_certificates_manager import run_download_from_file

st.set_page_config(page_title="Gerenciador de CDAs", layout="centered")
st.title("📄 Gerenciador de CDAs - DETRAN/RO")
st.markdown("Carregue sua lista de CDAs e informe suas credenciais para iniciar o download.")

# 🔐 User credentials
username = st.text_input("👤 CPF", type="default")
password = st.text_input("🔒 Senha do SitafeWeb", type="password")

# 📤 Upload CSV File
uploaded_file = st.file_uploader("📂 Carregue aqui sua lista de CDAs (.txt ou .csv)", type=["txt", "csv"])
st.caption("Arraste e solte o arquivo aqui ou clique para selecionar. Tamanho máximo: 200MB.")


# 📁 Define default download folder to user Downloads
default_download_path = str(Path.home() / "Downloads" / "CDAs")
st.markdown(f"🗂️ Os arquivos serão salvos em: `{default_download_path}`")

if uploaded_file is not None:
    st.success("Arquivo carregado com sucesso!")

if st.button("▶️ Baixar CDAs"):
    if not uploaded_file or not username or not password:
        st.error("⚠️ Por favor, preencha todos os campos obrigatórios.")
    else:
        st.info("🔄 Iniciando serviço...")
        try:
            # 💾 Save file temporarily
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_path = f"temp_cdalist_{timestamp}.csv"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())
            st.info("📄 Lista pronta para download.")

            # ⚙️ Run the main automation
            os.environ["STREAMLIT_RUN"] = "1"
            st.info("⬇️ Fazendo download das CDAs...")
            total, success_count, log_path, archive_folder = run_download_from_file(
                file_path=temp_path,
                username=username,
                password=password,
                download_dir=default_download_path
            )

            # 🧾 Show final paths and log
            st.write("✅ Script executado com sucesso.")
            st.write(f"📁 Pasta de download: `{archive_folder}`")
            st.write(f"📝 Log file gerado: `{log_path}`")

            try:
                df = pd.read_csv(log_path)
                st.subheader("📊 Relatório de Execução")
                st.dataframe(df)
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
