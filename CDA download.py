# cda_download_modular.py

import os
import time
import csv
import shutil
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_logging():
    logging.basicConfig(
        filename="log.txt",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def setup_download_directory(path: str) -> str:
    if os.path.exists(path):
        print(f"📁 Download folder found: {path}")
    else:
        print(f"📁 Download folder not found. It will be created: {path}")
        os.makedirs(path, exist_ok=True)
    return os.path.abspath(path)

def setup_chrome_driver(download_dir: str, driver_path: str) -> webdriver.Chrome:
    print("🔄 Starting services...")
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--headless=new")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def login_to_sitafe(driver: webdriver.Chrome, wait: WebDriverWait, username: str, password: str):
    print("🔐 Logging into Sitafe...")
    driver.get("https://sitafeweb.sefin.ro.gov.br/projudi")
    username_input = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    username_input.send_keys(username)
    password_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    password_input.send_keys(password)
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entrar')]")))
    login_button.click()
    wait.until(EC.presence_of_element_located((By.XPATH, "//h6[contains(text(), 'PROJUDI')]")))

def navigate_to_cda_page(driver: webdriver.Chrome, wait: WebDriverWait):
    projudi_button = wait.until(EC.element_to_be_clickable((
        By.XPATH, "//div[contains(@class, 'text-orange')]//h6[contains(text(), 'PROJUDI')]"
    )))
    projudi_button.click()
    impressao_cda_link = wait.until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(., 'CDA')]"))
    )
    driver.execute_script("arguments[0].click();", impressao_cda_link)

def read_cda_csv(file_path: str) -> list:
    with open(file_path, encoding='utf-8-sig', newline='') as file:
        reader = csv.DictReader(file)
        return [row['cda'].strip() for row in reader if row['cda'].strip()]

def read_previous_log(log_path: str) -> set:
    processed = set()
    try:
        with open(log_path, mode="r", newline='', encoding="utf-8") as existing_log:
            reader = csv.DictReader(existing_log)
            for row in reader:
                if row["Status"] == "Success":
                    processed.add(row["CDA"].replace("'", "").strip())
    except FileNotFoundError:
        pass
    return processed

def process_cda_list(driver, wait, cda_list, download_dir, log_path, max_retries=2):
    processed_successfully = read_previous_log(log_path)
    cda_list_to_process = []
    for cda in cda_list:
        if cda in processed_successfully:
            print(f"[SKIPPED] CDA {cda} already marked as Success in log.")
        else:
            cda_list_to_process.append(cda)

    total_cdAs = len(cda_list_to_process)
    print(f"📥 Starting downloads ({total_cdAs} CDAs)...")

    with open(log_path, mode="a", newline='', encoding='utf-8') as log_file:
        log_writer = csv.writer(log_file)
        if os.stat(log_path).st_size == 0:
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

def archive_downloaded_files(download_dir):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_folder = os.path.join(download_dir, f"CDAs_{timestamp}")
    os.makedirs(archive_folder, exist_ok=True)
    for filename in os.listdir(download_dir):
        if filename.lower().endswith(".pdf"):
            source_path = os.path.join(download_dir, filename)
            destination_path = os.path.join(archive_folder, filename)
            shutil.move(source_path, destination_path)
    logging.info(f"✅ All downloaded CDAs moved to: {archive_folder}")

def main():
    print("Starting Script...")
    setup_logging()
    download_dir = setup_download_directory(r"C:\Users\rafae\Downloads\CDAs")
    driver_path = r"C:\Users\rafae\OneDrive\Documentos\Projetos TI\debit-certificates-downloader\chromedriver.exe"
    driver = setup_chrome_driver(download_dir, driver_path)
    wait = WebDriverWait(driver, 10)

    cda_list = read_cda_csv("cdas.csv")

    login_to_sitafe(driver, wait, "02092091271", "Sitafe321")
    navigate_to_cda_page(driver, wait)

    process_cda_list(driver, wait, cda_list, download_dir, "output_log.csv")
    driver.quit()

    archive_downloaded_files(download_dir)
    logging.info("Finished processing all CDAs.")
    input("\nScript finalizado. Pressione Enter para fechar.")

if __name__ == "__main__":
    main()
