import os
import time
import datetime as _dt
from dataclasses import dataclass
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from tkinter.filedialog import askopenfilename
from tqdm import tqdm

@dataclass
class SessionState:
    ldc_accounts: pd.DataFrame = pd.DataFrame()
    login_status: int = 0
    coned_status: int = 0
    onr_status: int = 0
    mfa_status: int = 0
    current_date: _dt.date = _dt.date.today()
    now: _dt.datetime = _dt.datetime.now()

state = SessionState()
driver: Optional[webdriver.Chrome] = None
actions: Optional[ActionChains] = None

def _build_driver() -> webdriver.Chrome:
    """Create a Chrome WebDriver using environment-based configuration.
    Env vars:
      - CHROME_BINARY: path to Chrome/Chromium
      - CHROMEDRIVER_PATH: path to chromedriver
      - HEADLESS: '1' to run headless
    """
    chrome_binary = os.getenv("CHROME_BINARY")
    chromedriver_path = os.getenv("CHROMEDRIVER_PATH")
    headless = os.getenv("HEADLESS", "0") == "1"

    options = webdriver.ChromeOptions()
    if chrome_binary:
        options.binary_location = chrome_binary
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1400,1000")

    service = ChromeService(executable_path=chromedriver_path) if chromedriver_path else ChromeService()
    drv = webdriver.Chrome(service=service, options=options)
    return drv

def init_driver() -> None:
    """Initialize global WebDriver and action chains."""
    global driver, actions
    if driver is None:
        driver = _build_driver()
        actions = ActionChains(driver)

def load_accounts_list() -> None:
    """Prompt for an Excel file containing 'LDC Acct ID #' and load into state."""
    filename = askopenfilename(title="Select Excel with 'LDC Acct ID #' column")
    if not filename:
        raise RuntimeError("No file selected.")
    try:
        state.ldc_accounts = pd.read_excel(filename, dtype={'LDC Acct ID #': str})
    except Exception as exc:
        raise RuntimeError(f"Error loading accounts list: {exc}") from exc

def log_in() -> None:
    """Log into ConEd portal using env credentials."""
    init_driver()
    assert driver is not None
    username = os.getenv("CONED_USERNAME")
    password = os.getenv("CONED_PASSWORD")
    if not username or not password:
        raise RuntimeError("Missing CONED_USERNAME / CONED_PASSWORD environment variables.")
    try:
        driver.get("https://www.coned.com/en/login")
        driver.maximize_window()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "form-login-email"))).send_keys(username)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "form-login-password"))).send_keys(password + Keys.RETURN)
        state.login_status = 1
    except Exception as exc:
        raise RuntimeError(f"Login failed: {exc}") from exc

def log_in_mfa() -> None:
    """Handle MFA prompt by asking the user to type the current code."""
    assert driver is not None
    try:
        verify = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "form-login-mfa-code")))
        mfa_code = input("Enter 2FA code: ").strip()
        verify.send_keys(mfa_code + Keys.RETURN)
        state.mfa_status = 1
    except Exception as exc:
        raise RuntimeError(f"MFA failed: {exc}") from exc

def coned_portal() -> None:
    """Navigate to the ConEd accounts/billing portal."""
    assert driver is not None
    try:
        driver.get("https://www.coned.com/en/accounts-billing")
        state.coned_status = 1
    except Exception as exc:
        raise RuntimeError(f"ConEd portal navigation failed: {exc}") from exc

def onr_portal() -> None:
    """Navigate to the O&R accounts/billing portal."""
    assert driver is not None
    try:
        driver.get("https://www.oru.com/en/accounts-billing")
        state.onr_status = 1
    except Exception as exc:
        raise RuntimeError(f"O&R portal navigation failed: {exc}") from exc

def get_hu() -> None:
    """Request HU data for each account; placeholder navigation for demo."""
    assert driver is not None
    if state.ldc_accounts.empty:
        raise RuntimeError("No accounts loaded. Call load_accounts_list() first.")
    print("Requesting HU Data")
    for _acct in tqdm(state.ldc_accounts['LDC Acct ID #'], desc="HU Requests"):
        time.sleep(1)
        driver.get("https://apps.coned.com/HEF/HeritageInternet/heritage_login_hef/HeritageLogin.aspx?regiontype=HEF")
    print("HU requests complete.")

def get_idr() -> None:
    """Request IDR data; placeholder navigation for demo."""
    assert driver is not None
    if state.ldc_accounts.empty:
        raise RuntimeError("No accounts loaded. Call load_accounts_list() first.")
    print("Requesting IDR Data")
    for _acct in tqdm(state.ldc_accounts['LDC Acct ID #'], desc="IDR Requests"):
        time.sleep(1)
        driver.get("https://apps.coned.com/CEWEBService/Login.aspx?ReturnUrl=%2fCEWEBService%2f")
    print("IDR requests complete.")
