# 📜 CDA Download Automation Script
# 📜 This script automates the download of CDA (Certidão de Dívida Ativa) documents from a website.

print("Starting Script...")

# --- IMPORTS ---
import time
import os
import logging
import csv
import shutil
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
# Notify the user about the download folder status
if os.path.exists(download_dir):
    print(f"📁 Download folder found: {download_dir}")
else:
    print(f"📁 Download folder not found. It will be created: {download_dir}")
    os.makedirs(download_dir, exist_ok=True)

print("🔄 Starting services...")
# Chrome options, driver setup, WebDriverWait, etc.

# --- SET CHROME PREFERENCES ---
chrome_options = Options()
chrome_options.add_argument("--log-level=3")  # Suppress most logs
chrome_options.add_argument("--headless=new") # Run in headless mode (no GUI)
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
with open("cdas.csv", encoding='utf-8-sig', newline='') as file:
    reader = csv.DictReader(file)
    cda_list = [row['cda'].strip() for row in reader if row['cda'].strip()]

# --- OPEN WEBSITE ---
driver.get("https://sitafeweb.sefin.ro.gov.br/projudi")

print("🔐 Logging into Sitafe...")

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
impressao_cda_link = wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(., 'CDA')]"))
)
driver.execute_script("arguments[0].click();", impressao_cda_link)

# --- CDA DOWNLOAD SECTION ---
max_retries = 2

# --- CHECK IF OUTPUT LOG EXISTS ---
processed_successfully = set()
try:
    with open("output_log.csv", mode="r", newline='', encoding="utf-8") as existing_log:
        reader = csv.DictReader(existing_log)
        for row in reader:
            if row["Status"] == "Success":
                cleaned_cda = row["CDA"].replace("'", "").strip()
                processed_successfully.add(cleaned_cda)
except FileNotFoundError:
    pass

# --- BUILD LIST OF CDAs TO PROCESS ---
cda_list_to_process = []

for cda in cda_list:
    if cda in processed_successfully:
        print(f"[SKIPPED] CDA {cda} already marked as Success in log.")
    else:
        cda_list_to_process.append(cda)

total_cdAs = len(cda_list_to_process)
print(f"📥 Starting downloads ({total_cdAs} CDAs)...")

# --- OPEN OUTPUT LOG AND START PROCESSING ---
with open("output_log.csv", mode="a", newline='', encoding='utf-8') as log_file:
    log_writer = csv.writer(log_file)

    # Write header only if the file was just created
    if os.stat("output_log.csv").st_size == 0:
        log_writer.writerow(["CDA", "Status", "Timestamp", "Message"])

    for index, cda in enumerate(cda_list_to_process, start=1):
        success = False
        attempts = 0

        while not success and attempts <= max_retries:
            try:
                logging.info(f"Processing CDA: {cda} (Attempt {attempts + 1})")

                cda_input = wait.until(EC.visibility_of_element_located((By.NAME, "PA_NU_CDA")))
                cda_input.clear()
                cda_input.send_keys(cda)

                search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Pesquisar')]")))
                search_button.click()

                download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Imprimir')]")))
                driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
                time.sleep(0.2)
                driver.execute_script("arguments[0].click();", download_button)

                log_writer.writerow([f"'{cda}", "Success", datetime.now().isoformat(), f"Downloaded on attempt {attempts + 1}"])
                print(f"[ {index} / {total_cdAs} ] Processing CDA: {cda}... ✅")
                success = True

                time.sleep(1)
       
            except Exception as e:
                attempts += 1
                logging.warning(f"Attempt {attempts} failed for CDA {cda}: {e}")
                if attempts > max_retries:
                    log_writer.writerow([f"'{cda}", "Failed", datetime.now().isoformat(), str(e)])
                    print(f"[ {index} / {total_cdAs} ] Processing CDA: {cda}... ❌")
     
print("\n✅ Downloads concluded.\n")

# --- CLOSE BROWSER AFTER ALL CDAs ARE PROCESSED ---
driver.quit()

# Create a timestamped folder for this completed batch
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
archive_folder = os.path.join(download_dir, f"CDAs_{timestamp}")
os.makedirs(archive_folder, exist_ok=True)

# Move all PDF files from download_dir into archive_folder
for filename in os.listdir(download_dir):
    if filename.lower().endswith(".pdf"):
        source_path = os.path.join(download_dir, filename)
        destination_path = os.path.join(archive_folder, filename)
        shutil.move(source_path, destination_path)

logging.info(f"✅ All downloaded CDAs moved to: {archive_folder}")

# --- LOG COMPLETION ---
logging.info("Finished processing all CDAs.")
