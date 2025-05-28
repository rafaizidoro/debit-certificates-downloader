# Gerenciador de CDAs - DETRAN/RO
# This is a Streamlit app that allows users to upload a list of CDAs (Certificados de Débito)
# and automate their download through Sitafe via the 'debit_certificates_manager' module.

import streamlit as st
import os
import pandas as pd
from debit_certificates_manager import run_download_from_file
from datetime import datetime

# Generate a timestamp for file uniqueness
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Set Streamlit page configuration
st.set_page_config(page_title="Gerenciador de CDAs", layout="centered")

# Page title
st.title("📄 Gerenciador de CDAs - DETRAN/RO")

# Instructional text
st.markdown("Carregue sua lista de CDAs abaixo para iniciar o download.")

# File uploader for .csv or .txt files
uploaded_file = st.file_uploader("📂 Upload da lista de CDAs (.txt ou .csv)", type=["txt", "csv"])

# Notify user after upload
if uploaded_file is not None:
    st.success("Arquivo carregado com sucesso!")

# Main action button
if st.button("▶️ Baixar CDAs"):
    if uploaded_file is None:
        st.error("Você precisa carregar um arquivo antes de iniciar.")
    else:
        st.info("🔄 Iniciando...")
    
        try:
            # 💾 Save uploaded file to a temporary local path
            st.write("📂 Carregando lista de CDAs...")
            temp_path = f"temp_cdalist_{timestamp}.csv"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())

            # ⚙️ Run the automation and retrieve result summary
            st.write("📥 Iniciando o download...")
            os.environ["STREAMLIT_RUN"] = "1"
            total, success_count, log_path, archive_folder = run_download_from_file(temp_path)
            
            # 📁 Display paths used
            st.write("✅ Finalizado.")
            st.write(f"📁 Pasta de download: `{archive_folder}`")
            st.write(f"📝 Log file gerado: `{log_path}`")
            
            # 📊 Load and display the resulting CSV log
            try:
                df = pd.read_csv(log_path)
                st.subheader("📊 Relatório de Execução")
                st.dataframe(df)
                with open(log_path, "rb") as f:
                    st.download_button("⬇️ Baixar Relatório", f, file_name=os.path.basename(log_path), mime="text/csv")
            except Exception as e:
                st.warning(f"⚠️ Falha ao carregar log: {e}")

            
            # ✅ User feedback based on results
            if success_count == 0:
                st.error("❌ Nenhuma CDA foi baixada com sucesso.")
            else:
                st.success(f"✅ {success_count} de {total} CDAs baixadas com sucesso.")

        except Exception as e:
            # Handle unexpected failure during automation
            st.error(f"Erro ao executar a automação: {e}")
