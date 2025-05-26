# 🧾 CDA Download Automation

This Python script automates the login, navigation, and download of CDA (Certidões de Dívida Ativa) PDFs from the **SitafeWeb** system.

It is designed for internal use at DETRAN/RO and helps save hours of repetitive work by downloading hundreds of CDAs at once.

---

## 📦 Features

- ✅ Headless download of CDA PDFs
- ✅ Reads CDA numbers from a CSV file
- ✅ Logs each attempt (success or failure)
- ✅ Avoids re-downloading already processed CDAs
- ✅ Archives downloads into timestamped folders
- ✅ Modular code, easy to expand and maintain

---

## 🛠️ Requirements

- Python 3.10 or later
- Google Chrome (latest version)
- ChromeDriver matching your Chrome version
- `python-dotenv` package (for reading credentials)

Install required packages:

```bash
pip install selenium python-dotenv
