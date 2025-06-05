# DEBIT CERTIFICATES MANAGER SCRIPT
# THIS SCRIPT AUTOMATES THE PROCESS OF DOWNLOADING DEBIT CERTIFICATES (CDAS) FROM THE SITAFE SYSTEM.

# STANDARD LIBRARY IMPORTS
import os
import time
import csv
import shutil
import logging
import traceback  

# THIRD-PARTY LIBRARY IMPORTS
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# TEMPORARY CONDITIONAL IMPORT FOR STREAMLIT
if os.getenv("STREAMLIT_RUN") == "1":
    import streamlit as st
    def streamlit_print(*args, **kwargs):
        st.write(" ".join(str(a) for a in args))
else:
    def streamlit_print(*args, **kwargs):
        print(*args, **kwargs)

# SETUP LOGGING CONFIGURATION
def setup_logging():
    logging.basicConfig(
        filename="log.txt",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# SETUP DOWNLOAD DIRECTORY
def setup_download_directory(path: str) -> str:
    if os.path.exists(path):
        streamlit_print(f"📁 Pasta de download encontrada: {path}")
    else:
        streamlit_print(f"📁 Pasta de download não encontrada. A pasta foi criada em: {path}")
        os.makedirs(path, exist_ok=True)
    return os.path.abspath(path)

# SETUP CHROME DRIVER WITH OPTIONS
def setup_chrome_driver(download_dir: str, driver_path: str = None) -> webdriver.Chrome:
    streamlit_print("🔄 Iniciando serviços...")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })

    if not driver_path:
        driver_path = os.path.join(os.path.dirname(__file__), "bin", "chromedriver.exe")

    if not os.path.exists(driver_path):
        raise FileNotFoundError(f"Chromedriver not found at: {driver_path}")

    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

# LOGIN TO SITAFE SYSTEM
def login_to_sitafe(driver: webdriver.Chrome, wait: WebDriverWait, username: str, password: str):
    streamlit_print("🔐 Fazendo login no SitafeWeb...")
    driver.get("https://sitafeweb.sefin.ro.gov.br/projudi")

    username_input = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    username_input.send_keys(username)
    password_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    password_input.send_keys(password)
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entrar')]")))
    login_button.click()
    try:
        # WAIT FOR THE PAGE TO LOAD AFTER LOGIN
        wait.until(EC.presence_of_element_located((By.XPATH, "//h6[contains(text(), 'PROJUDI')]")))
    except:
        # IF LOGIN FAILS, DISPLAY ERROR MESSAGE
        try:
            error_message = driver.find_element(By.XPATH, "//div[contains(@class, 'alert')]").text
            raise Exception(f"❌ Falha no login: {error_message}")
        except:
            raise Exception("❌ Falha no login: CPF ou senha inválidos ou erro inesperado.")

# NAVIGATION TO THE CDA DOWNLOAD PAGE
def navigate_to_cda_page(driver: webdriver.Chrome, wait: WebDriverWait):
    projudi_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//div[contains(@class, 'text-orange')]//h6[contains(text(), 'PROJUDI')]"
    )))
    projudi_button.click()
    impressao_cda_link = wait.until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(., 'CDA')]"))
    )
    driver.execute_script("arguments[0].click();", impressao_cda_link)

# READ CDA LIST FROM CSV FILE
def read_cda_csv(file_path: str) -> list:
    try:
        with open(file_path, encoding='utf-8-sig', newline='') as file:
            reader = csv.DictReader(file)
            if 'cda' not in reader.fieldnames:
                raise ValueError("Column 'cda' not found in the CSV file.")
            return [row['cda'].strip() for row in reader if row['cda'].strip()]
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file '{file_path}' not found.")

# PROCESS CDA LIST AND DOWNLOAD CERTIFICATES
def process_cda_list(driver, wait, cda_list, download_dir, log_dir, max_retries=1, update_callback=None):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"log_{timestamp}.csv"
    log_path = os.path.join(log_dir, log_filename)

    os.makedirs(log_dir, exist_ok=True)

    total_cdAs = len(cda_list)
    success_count = 0
    streamlit_print(f"🗕 Iniciando o download de ({total_cdAs} CDAs)...")

    with open(log_path, mode="w", newline='', encoding='utf-8') as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow(["CDA", "Status", "Timestamp", "Message"])

        for index, cda in enumerate(cda_list, start=1):
            if update_callback:
                update_callback(index, total_cdAs, cda)
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
                    streamlit_print(f"[ {index} / {total_cdAs} ] Processando CDAs: {cda}... ✅")
                    success = True
                    success_count += 1
                    time.sleep(1)

                except Exception as e:
                    attempts += 1
                    full_trace = traceback.format_exc()
                    logging.warning(f"Attempt {attempts} failed for CDA {cda}:\n{full_trace}")
                    if attempts > max_retries:
                        log_writer.writerow([f"'{cda}", "Failed", datetime.now().isoformat(), full_trace])
                        streamlit_print(f"[ {index} / {total_cdAs} ] Processando CDAs: {cda}... ❌")
        # END OF CDA PROCESSING LOOP
        # UPDATE CALLBACK FOR FINAL STATUS
        if update_callback and total_cdAs > 0:
            update_callback(total_cdAs, total_cdAs, "✅ All CDAs processed successfully.")

    streamlit_print(f"\n✅ Downloads finalizados.\n")
    return total_cdAs, success_count, log_path

# ARCHIVE DOWNLOADED FILES
def archive_downloaded_files(download_dir, log_path=None):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_folder = os.path.join(download_dir, f"CDAs_{timestamp}")
    os.makedirs(archive_folder, exist_ok=True)

    for filename in os.listdir(download_dir):
        if filename.lower().endswith(".pdf"):
            shutil.move(os.path.join(download_dir, filename), os.path.join(archive_folder, filename))

    if log_path and os.path.exists(log_path):
        log_filename = os.path.basename(log_path)
        new_log_path = os.path.join(archive_folder, log_filename)
        shutil.move(log_path, new_log_path)
        log_path = new_log_path

    logging.info(f"✅ All downloaded CDAs moved to: {archive_folder}")
    return archive_folder, log_path

# RUN DOWNLOAD FROM FILE FUNCTION
def run_download_from_file(file_path, username, password, download_dir, driver_path=None, update_callback=None):
    setup_logging()
    cda_list = read_cda_csv(file_path)

    log_dir = "logs"
    download_dir = setup_download_directory(download_dir)
    driver = setup_chrome_driver(download_dir, driver_path)
    wait = WebDriverWait(driver, 15)

    login_to_sitafe(driver, wait, username, password)
    navigate_to_cda_page(driver, wait)
    total, success_count, log_path = process_cda_list(driver, wait, cda_list, download_dir, log_dir, uptade_callback=update_callback)
    archive_folder, log_path = archive_downloaded_files(download_dir, log_path)
    driver.quit()
    return total, success_count, log_path, archive_folder

# MAIN FUNCTION FOR STREAMLIT INTERFACE
if __name__ == "__main__":
    print("Please use the Streamlit interface to run this script.")
