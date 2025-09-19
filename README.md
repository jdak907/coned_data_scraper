# ConEd / O&R Data Utility — PySide6 + MIT

A small, security-hardened toolkit that automates the conEdison portal for batch data requests:

- **Desktop UI (PySide6)** to drive Selenium flows for ConEd/O&R (login, MFA, portal navigation).
- **CLI utilities** for data cleanup and batch ops (Excel→CSV, IDR file renaming).
- **Data wrangling (Pandas)** to normalize raw utility exports into an analytics-friendly schema.
- **Good hygiene**: PEP-8, type hints, docstrings, tests, and **no hardcoded secrets** (env-vars + `.env`).

**License:** MIT (permissive).

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# env (or use a .env file with python-dotenv)
export CONED_USERNAME="you@example.com"
export CONED_PASSWORD="******"
export CHROME_BINARY="/path/to/chrome"
export CHROMEDRIVER_PATH="/path/to/chromedriver"
export HEADLESS=1

# Run the desktop UI
python -m coned_utility.main

# Or use a CLI tool
python -m coned_utility.dataframe --input raw.csv --output normalized.csv
```

## Structure
```
coned_utility/
  main.py                 # PySide6 app
  datafunctions.py        # Selenium flows (login/MFA/portal + requests)
  dataframe.py            # CSV normalization CLI
  excel_to_csv.py         # Excel→CSV CLI
  rename_coned_idr_file.py# Safe batch renamer
examples/selenium_test.py
tests/test_basic.py
LICENSE
```

## Notes
- DOMs change over time; selectors here are illustrative patterns.
- Do not commit secrets; `.env` is ignored.
