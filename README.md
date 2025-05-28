### 📄 Gerenciador de CDAs - DETRAN/RO

This project automates the download of Certidões de Dívida Ativa (CDAs) from the Sitafe system via both command-line and a user-friendly Streamlit web interface.

#### Features:
- Automates login and navigation in Sitafe system
- Downloads multiple CDA PDFs using a `.csv` or `.txt` list
- Displays progress and final log report in Streamlit
- Organizes output in timestamped folders (e.g. `downloads/CDAs_2025-05-28_14-52-00/`)
- Logs each execution to a separate `.csv` report

#### How to Use

**1. Set up environment variables** (via `.env`):
```env
SITAFE_USERNAME=your_username
SITAFE_PASSWORD=your_password
CHROMEDRIVER_PATH=path_to_chromedriver.exe
DOWNLOAD_DIR=downloads
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run the web app:**
```bash
streamlit run cda_webapp.py
```

**4. Use the interface to upload a list of CDAs and start downloading.**

The resulting PDFs and log report will be saved in a new timestamped folder inside `DOWNLOAD_DIR`.