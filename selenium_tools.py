import time
from bs4 import BeautifulSoup
from selenium import webdriver # type: ignore
from selenium.webdriver.chrome.service import Service as ChromeService # type: ignore
from selenium.webdriver.common.by import By # type: ignore
from selenium.webdriver.support.ui import WebDriverWait # type: ignore
from selenium.webdriver.support import expected_conditions as EC # type: ignore
from selenium.webdriver.chrome.options import Options # type: ignore
from webdriver_manager.chrome import ChromeDriverManager

from utility import string_parse_for_url # type: ignore

driver: any = None

def close_driver(*args):
    global driver
    # Verifica si el driver ya ha sido cerrado previamente
    if driver and getattr(driver, "closed", False) is False:
        driver.quit()
        print("Navegador cerrado.")
        # Marcamos el driver como cerrado
        driver.closed = True
    else:
        print("Navegador ya estaba cerrado.")

def initialize_selenium():
    global driver
    chrome_opt = Options()
    chrome_opt.add_argument("--disable-gpu")
    chrome_opt.add_argument("--disable-software-rasterizer")
    chrome_opt.add_argument("--no-first-run")
    chrome_opt.add_argument("--no-default-browser-check")
    chrome_opt.add_argument("--disable-popup-blocking")
    chrome_opt.add_argument("--disable-infobars")

    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_opt)
    driver.set_window_position(-10000, 0)

def open_page_wait(url, class_method):
    global driver
    driver.get(url)

    time.sleep(5)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_method))
    )
    
    return BeautifulSoup(driver.page_source, 'html.parser')