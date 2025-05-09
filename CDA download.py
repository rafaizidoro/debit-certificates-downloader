from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to your ChromeDriver
chrome_driver_path = r"C:\Users\rafae\OneDrive\Documentos\Projetos TI\debit-certificates-downloader\chromedriver.exe"

# Setup Selenium
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Define wait (used throughout the script)
wait = WebDriverWait(driver, 10)

# Open website
driver.get("https://sitafeweb.sefin.ro.gov.br/projudi")

# --- LOG IN ---

# Wait for username input to appear and type it
username_input = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
username_input.send_keys("02092091271")

# Wait for password input and type it
password_input = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
password_input.send_keys("Sitafe321")

# Wait for the login button to be clickable and click it
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entrar')]")))
login_button.click()

# Wait for the "PROJUDI" button and click it
projudi_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'text-orange')]//h6[contains(text(), 'PROJUDI')]")))
projudi_button.click()

# --- ACCESS "Impressão de CDA" ---

# Wait for the "Impressão de CDA" menu link and click it
impressao_cda_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Impressão de CDA")))
impressao_cda_link.click()

# --- INPUT CDA NUMBER ---

# Wait for the CDA input field to be visible and type the number
cda_input = wait.until(EC.visibility_of_element_located((By.NAME, "PA_NU_CDA")))
cda_input.send_keys("20240200286010")

# --- SEARCH CDA ---

# Wait for the "Pesquisar" button and click it
search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Pesquisar')]")))
search_button.click()

# --- DOWNLOAD PDF ---

# Wait for the "Imprimir" (Download) button and click it
download_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Imprimir')]")))
download_button.click()

# Optional: Wait to make sure download starts before quitting
time.sleep(5)

# Close the browser
driver.quit()
