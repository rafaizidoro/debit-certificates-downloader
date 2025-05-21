# 📜 CDA Download Automation Script
# 📜 This script automates the download of CDA (Certidão de Dívida Ativa) documents from a website.

# --- IMPORTS ---
import time
import os
import logging
import csv
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# --- SETUP LOGGING ---
logging.basicConfig(
    filename="log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# --- SETUP CHROME DRIVER PATH ---
chrome_driver_path = r"C:\Users\rafae\OneDrive\Documentos\Projetos TI\debit-certificates-downloader\chromedriver.exe"
service = Service(chrome_driver_path)

# --- SETUP DOWNLOAD FOLDER ---
# 📂 Change this to your desired download folder
# Define download folder
download_dir = r"C:\Users\rafae\Downloads\CDAs"

# Create folder if it doesn't exist
if not os.path.exists(download_dir):
        os.makedirs(download_dir)

# Set Chrome preferences
chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,        # 📂 Your folder here
    "download.prompt_for_download": False,             # 🚫 No popup
    "download.directory_upgrade": True,                # ⬆ If folder exists, use it
    "plugins.always_open_pdf_externally": True         # 📄 Avoid opening PDFs in browser
})

# Start Chrome with options
driver = webdriver.Chrome(service=service, options=chrome_options)


# --- DEFINE WEBDRIVER WAIT OBJECT (REUSABLE) ---
wait = WebDriverWait(driver, 10)

# Load CDAs from cdas.csv
with open("cdas.csv", newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    cda_list = [row['cda'].strip() for row in reader if row['cda'].strip()]

# Prepare output log CSV
log_file = open("output_log.csv", mode="w", newline='', encoding='utf-8')
log_writer = csv.writer(log_file)
log_writer.writerow(["CDA", "Status", "Timestamp", "Message"])

# --- OPEN WEBSITE ---
driver.get("https://sitafeweb.sefin.ro.gov.br/projudi")

# --- LOG IN ---
username_input = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
username_input.send_keys("02092091271")

password_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
password_input.send_keys("Sitafe321")

login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entrar')]")))
login_button.click()

# --- WAIT FOR MAIN DASHBOARD TO LOAD ---
wait.until(EC.presence_of_element_located((By.XPATH, "//h6[contains(text(), 'PROJUDI')]")))

# --- CLICK ON PROJUDI ---
projudi_button = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//div[contains(@class, 'text-orange')]//h6[contains(text(), 'PROJUDI')]"
)))
projudi_button.click()

# --- CLICK ON "IMPRESSÃO DE CDA" ---
impressao_cda_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Impressão de CDA")))
impressao_cda_link.click()

# --- PROCESS EACH CDA IN THE LIST AND LOGS EACH TRY ON A .CSV---
for cda in cda_list:
    try:
        logging.info(f"Processing CDA: {cda}")

        # Fill CDA input
        cda_input = wait.until(EC.visibility_of_element_located((By.NAME, "PA_NU_CDA")))
        cda_input.clear()
        cda_input.send_keys(cda)

        # Click "Pesquisar"
        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Pesquisar')]")))
        search_button.click()

        # Click "Imprimir" using JS
        download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Imprimir')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
        time.sleep(0.2)
        driver.execute_script("arguments[0].click();", download_button)

        # Log success in output_log.csv
        log_writer.writerow([f"'{cda}", "Success", datetime.now().isoformat(), "Downloaded"])
        time.sleep(1)

    except Exception as e:
        logging.error(f"Error processing CDA {cda}: {e}")
        # Log failure in output_log.csv
        log_writer.writerow([f"'{cda}", "Failed", datetime.now().isoformat(), str(e)])

    log_file.close()

# --- CLOSE BROWSER AFTER ALL CDAs ARE PROCESSED ---
driver.quit()

# --- LOG COMPLETION ---
logging.info("Finished processing all CDAs.")
