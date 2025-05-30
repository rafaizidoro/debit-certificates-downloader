# 📄 Debit Certificates Manager (SitafeWeb Automation)

This tool automates the download of Certidões de Débito Ativa (CDAs) from the SitafeWeb system used by DETRAN/RO.  
Now with a simple and intuitive Streamlit-based interface, it’s suitable for both technical and non-technical users.

---

## 🚀 Features

- ✅ Web-based interface (no terminal required)
- ✅ Secure login using your CPF and password
- ✅ Upload `.csv` or `.txt` file with CDA numbers
- ✅ Automatic download of all CDAs as PDF
- ✅ Logs each attempt (success/failure) in a CSV file
- ✅ Saves everything to your local `Downloads/CDAs/` folder
- ✅ Downloadable execution report via the interface

---

## 🖥️ How to Run

### 1. Clone the repository:
```bash
git clone https://github.com/your-user/debit-certificates-manager.git
cd debit-certificates-manager

### 2. Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt

### 3. Run the app:

bash
Copy
Edit
streamlit run cda_webapp.py

### 📂 Input File Format
Upload a .csv or .txt file with a column named cda, for example:

.csv:

cda
01234567890
11223344556
99887766554

### 📥 Output
All CDA PDFs are downloaded into:

~/Downloads/CDAs/CDAs_YYYY-MM-DD_HH-MM-SS/
A log CSV is also saved in the same folder, containing:
CDA,Status,Timestamp,Message

### 📌 Requirements

Python 3.8+
Google Chrome installed
ChromeDriver compatible with your Chrome version (already included in the repository)

🧪 Development & Testing
If you want to run the script without Streamlit:

python debit_certificates_manager.py
Make sure to update the script to include your username, password, and CDA list path.