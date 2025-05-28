# Debit Certificates Manager Script
# This script automates the process of downloading debit certificates (CDAs) from the Sitafe system.

# Standard library imports
import os
import time
import csv
import shutil
import logging
import traceback  

# Third-party library imports
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
load_dotenv()

# Temporary Conditional import for Streamlit
if os.getenv("STREAMLIT_RUN") == "1":
    import streamlit as st
    def streamlit_print(*args, **kwargs):
        st.write(" ".join(str(a) for a in args))
else:
    def streamlit_print(*args, **kwargs):
        print(*args, **kwargs)

# Setup logging configuration
def setup_logging():
    logging.basicConfig(
        filename="log.txt",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# Setup download directory
def setup_download_directory(path: str) -> str:
    if os.path.exists(path):
        streamlit_print(f"📁 Download folder found: {path}")
    else:
        streamlit_print(f"📁 Download folder not found. It will be created: {path}")
        os.makedirs(path, exist_ok=True)
    return os.path.abspath(path)

# Setup Chrome driver with options
def setup_chrome_driver(download_dir: str, driver_path: str) -> webdriver.Chrome:
    streamlit_print("🔄 Starting services...")
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") # Use headless mode for background operation
    chrome_options.add_argument("--disable-gpu") # Disable GPU acceleration
    chrome_options.add_argument("--start-maximized") # Start maximized
    chrome_options.add_argument("--disable-infobars") # Disable infobars
    chrome_options.add_argument("--disable-extensions") # Disable extensions
    chrome_options.add_argument("--log-level=3") # Suppress logs
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

# Login to Sitafe system
def login_to_sitafe(driver: webdriver.Chrome, wait: WebDriverWait, username: str, password: str):
    streamlit_print("🔐 Logging into Sitafe...")
    driver.get("https://sitafeweb.sefin.ro.gov.br/projudi")
    username_input = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    username_input.send_keys(username)
    password_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    password_input.send_keys(password)
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entrar')]")))
    login_button.click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//h6[contains(text(), 'PROJUDI')]")))

# Navigation to the CDA Download page
def navigate_to_cda_page(driver: webdriver.Chrome, wait: WebDriverWait):
    projudi_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//div[contains(@class, 'text-orange')]//h6[contains(text(), 'PROJUDI')]"
    )))
    projudi_button.click()
    impressao_cda_link = wait.until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(., 'CDA')]"))
    )
    driver.execute_script("arguments[0].click();", impressao_cda_link)

# Read CDA list from CSV file
def read_cda_csv(file_path: str) -> list:
    try:
        with open(file_path, encoding='utf-8-sig', newline='') as file:
            reader = csv.DictReader(file)
            if 'cda' not in reader.fieldnames:
                raise ValueError("Column 'cda' not found in the CSV file.")
            return [row['cda'].strip() for row in reader if row['cda'].strip()]
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file '{file_path}' not found.")

def process_cda_list(driver, wait, cda_list, download_dir, log_dir, max_retries=1):
    # Prepare log file
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"log_{timestamp}.csv"
    log_path = os.path.join(log_dir, log_filename)

    os.makedirs(log_dir, exist_ok=True)  # Ensure log folder exists

    total_cdAs = len(cda_list)
    success_count = 0
    streamlit_print(f"📥 Starting downloads ({total_cdAs} CDAs)...")

    with open(log_path, mode="w", newline='', encoding='utf-8') as log_file:
        log_writer = csv.writer(log_file)
        log_writer.writerow(["CDA", "Status", "Timestamp", "Message"])

        for index, cda in enumerate(cda_list, start=1):
            success = False
            attempts = 0

            while not success and attempts <= max_retries:
                try:
                    logging.info(f"Processing CDA: {cda} (Attempt {attempts + 1})")

                    # Fill CDA input
                    cda_input = wait.until(EC.visibility_of_element_located((By.NAME, "PA_NU_CDA")))
                    cda_input.clear()
                    cda_input.send_keys(cda)

                    # Click "Pesquisar"
                    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Pesquisar')]")))
                    search_button.click()

                    # Wait for and click "Imprimir"
                    download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Imprimir')]")))
                    driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
                    time.sleep(0.2)
                    driver.execute_script("arguments[0].click();", download_button)

                    # Log success
                    log_writer.writerow([f"'{cda}", "Success", datetime.now().isoformat(), f"Downloaded on attempt {attempts + 1}"])
                    streamlit_print(f"[ {index} / {total_cdAs} ] Processing CDA: {cda}... ✅")
                    success = True
                    success_count += 1
                    time.sleep(1)

                except Exception as e:
                    attempts += 1
                    full_trace = traceback.format_exc()
                    logging.warning(f"Attempt {attempts} failed for CDA {cda}:\n{full_trace}")
                    if attempts > max_retries:
                        log_writer.writerow([f"'{cda}", "Failed", datetime.now().isoformat(), full_trace])
                        streamlit_print(f"[ {index} / {total_cdAs} ] Processing CDA: {cda}... ❌")


    streamlit_print(f"\n✅ Finished downloading. Log saved to: {log_path}\n")
    return total_cdAs, success_count, log_path

# ARCHIVE DOWNLOADED FILES INTO A TIMESTAMPED FOLDER

def archive_downloaded_files(download_dir, log_path=None):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_folder = os.path.join(download_dir, f"CDAs_{timestamp}")
    os.makedirs(archive_folder, exist_ok=True)

    # Move downloaded PDF files to the archive folder
    for filename in os.listdir(download_dir):
        if filename.lower().endswith(".pdf"):
            shutil.move(os.path.join(download_dir, filename), os.path.join(archive_folder, filename))
    
    # Move log file if provided, and update its path
    if log_path and os.path.exists(log_path):
        log_filename = os.path.basename(log_path)
        new_log_path = os.path.join(archive_folder, log_filename)
        shutil.move(log_path, new_log_path)
        log_path = new_log_path  # Update variable to point to new location

    logging.info(f"✅ All downloaded CDAs moved to: {archive_folder}")
    return archive_folder, log_path

# RUN AND DOWNLOAD FROM A FILE (Streamlit)

def run_download_from_file(file_path):    

    setup_logging()
    
    # Read CDA list properly (auto-handles CSV)
    cda_list = read_cda_csv(file_path)

    # Load environment variables
       
    username = os.getenv("SITAFE_USERNAME")
    password = os.getenv("SITAFE_PASSWORD")
    driver_path = os.getenv("CHROMEDRIVER_PATH")
    download_dir = os.getenv("DOWNLOAD_DIR") or "downloads"
    log_dir = "logs"

    # Start Chrome driver
    driver = setup_chrome_driver(download_dir, driver_path)
    wait = WebDriverWait(driver, 15)

    # 🧭 Login and navigate
    login_to_sitafe(driver, wait, username, password)
    navigate_to_cda_page(driver, wait)

    # Process CDAs
    total, success_count, log_path = process_cda_list(driver, wait, cda_list, download_dir, log_dir)

    # Archive and Cleanup
    archive_folder, log_path = archive_downloaded_files(download_dir, log_path)
    driver.quit()
    return total, success_count, log_path, archive_folder


# Main function to run the script
def main():
    streamlit_print("Starting Script...")
    setup_logging()

    # Load env vars
    username = os.getenv("SITAFE_USERNAME")
    password = os.getenv("SITAFE_PASSWORD")
    driver_path = os.getenv("CHROMEDRIVER_PATH")
    download_dir = os.getenv("DOWNLOAD_DIR") or "downloads"
    log_dir = "logs"

    # Setup driver
    driver = setup_chrome_driver(download_dir, driver_path)
    wait = WebDriverWait(driver, 10)

    # Load CDA list from CSV
    cda_list = read_cda_csv("cdas.csv")

    # Run
    login_to_sitafe(driver, wait, username, password)
    navigate_to_cda_page(driver, wait)
    process_cda_list(driver, wait, cda_list, download_dir, log_dir)
    
    # Archive downloaded files and quit
    archive_downloaded_files(download_dir)
    driver.quit()

    logging.info("Finished processing all CDAs.")
    input("\nScript finalizado. Pressione Enter para fechar.")

# Ensure the script runs only when executed directly
if __name__ == "__main__":
    main()