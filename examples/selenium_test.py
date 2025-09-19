from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import os

options = webdriver.ChromeOptions()
if os.getenv("CHROME_BINARY"):
    options.binary_location = os.getenv("CHROME_BINARY")
if os.getenv("HEADLESS", "1") == "1":
    options.add_argument("--headless=new")
service = ChromeService(executable_path=os.getenv("CHROMEDRIVER_PATH"))
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://example.com")
print(driver.title)
driver.quit()
