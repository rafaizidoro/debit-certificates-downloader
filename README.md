# Gerenciador de CDAs (DEBT CERTIFICATES MANAGER)

This tool automates the download of Certidões de Dívida Ativa (CDAs) from the SitafeWeb system used by DETRAN/RO.  
It now includes a standalone Windows executable with a graphical interface powered by Streamlit, making it accessible to both technical and non-technical users.

---

## 🚀 Features

- ✅ Desktop GUI with Streamlit (no terminal required)
- ✅ Secure login with CPF and password
- ✅ Upload a `.csv` file containing CDA numbers
- ✅ Automated downloads of CDA PDFs from SitafeWeb
- ✅ Logging of all results (success/failure) in a CSV report
- ✅ Automatic folder creation and archiving of downloads
- ✅ Final report with log and download summary

---

## 🧑‍💻 How to Use the Standalone Executable

1. Download `GerenciadorCDAs.exe` from the [Releases](https://github.com/your-user/debit-certificates-manager/releases) page.
2. Double-click to open.
3. The terminal will display diagnostics and automatically launch the Streamlit interface in your browser.
4. Upload your CSV file and log in to start the automation.
5. Once complete, downloaded files and logs will be saved in a folder named `CDAs_<timestamp>`.

---

## 📂 Input File Format

Upload a `.csv` file with a header `cda`, like:

```csv
cda
01234567890
99887766554