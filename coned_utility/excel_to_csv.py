import argparse
from pathlib import Path
import pandas as pd

def excel_to_csv(xlsx_path: Path, csv_path: Path | None = None) -> Path:
    """Convert a single Excel file to CSV."""
    df = pd.read_excel(xlsx_path)
    out = csv_path or xlsx_path.with_suffix('.csv')
    df.to_csv(out, index=False)
    return out

def main():
    parser = argparse.ArgumentParser(description="Convert Excel (.xlsx) to CSV.")
    parser.add_argument("xlsx", help="Path to Excel file or a directory")
    parser.add_argument("--glob", default="*.xlsx", help="Glob pattern when a directory is given")
    args = parser.parse_args()
    p = Path(args.xlsx)
    if p.is_dir():
        for fp in p.glob(args.glob):
            out = excel_to_csv(fp)
            print(f"Converted: {fp} -> {out}")
    else:
        out = excel_to_csv(p)
        print(f"Converted: {p} -> {out}")

if __name__ == "__main__":
    main()
