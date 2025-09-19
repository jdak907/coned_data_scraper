# ConEd / O&R Data Utility

A Python utility for automating Con Edison / Orange & Rockland workflows and preparing data for analysis. It includes a desktop UI for driving Selenium sessions (login, MFA, portal navigation) and CLI tools for transforming and exporting datasets.

Desktop UI (PySide6): initiate authenticated sessions and trigger HU/IDR requests.

Automation (Selenium): environment-driven, headless capable.

Data processing (Pandas): normalize raw exports to a consistent schema.

CLI tools: Excel→CSV conversion and safe batch renaming for IDR files.

Hygiene: PEP-8 style, docstrings, small tests, secrets via environment variables.

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
