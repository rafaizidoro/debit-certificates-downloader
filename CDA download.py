# --- SETUP LOGGING ---
import logging

logging.basicConfig(
    filename="log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- SETUP CHROME DRIVER PATH ---
chrome_driver_path = r"C:\Users\rafae\OneDrive\Documentos\Projetos TI\Automação Dívida Ativa\chromedriver.exe"
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# --- DEFINE WEBDRIVER WAIT OBJECT (REUSABLE) ---
wait = WebDriverWait(driver, 10)

# --- LOAD CDA LIST FROM .TXT FILE ---
with open("cdas.txt", "r") as file:
    cda_list = [line.strip() for line in file if line.strip()]

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

# --- PROCESS EACH CDA IN THE LIST AND LOGS EACH TRY ---
for cda in cda_list:
    try:
    logging.info(f"Processing CDA: {cda}")

    # Find and fill the CDA input
    cda_input = wait.until(EC.visibility_of_element_located((By.NAME, "PA_NU_CDA")))
    cda_input.clear()
    cda_input.send_keys(cda)

    # Click "Pesquisar"
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Pesquisar')]")))
    search_button.click()

    # Click "Imprimir"
    download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Imprimir')]")))
    download_button.click()

    # Optional: wait briefly to ensure the download starts
    time.sleep(1)

    # Log error message
    except Exception as e:
        logging.error(f"Error processing CDA {cda}: {e}")
    
# --- CLOSE BROWSER AFTER ALL CDAs ARE PROCESSED ---
driver.quit()

# --- LOG COMPLETION ---
logging.info("Finished processing all CDAs.")
