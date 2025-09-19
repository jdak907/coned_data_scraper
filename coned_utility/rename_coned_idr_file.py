import argparse
from pathlib import Path

def _parse_header(line: str) -> tuple[str, str]:
    digits = ''.join(ch for ch in line if ch.isdigit())
    letters = ''.join(ch for ch in line if not ch.isdigit()).strip()
    name = letters[21:].lstrip() if len(letters) > 21 else letters
    return digits, name

def rename_files(paths: list[Path]) -> list[tuple[Path, Path]]:
    results = []
    for fp in paths:
        header = fp.read_text(encoding="utf-8", errors="ignore").splitlines()[0].rstrip("\r\n")
        acct_num, acct_name = _parse_header(header)
        base = f"{acct_num} {acct_name}.txt".strip()
        target = fp.with_name(base)
        counter = 0
        while target.exists():
            counter += 1
            target = fp.with_name(f"{acct_num} {acct_name}-dup{counter}.txt")
        fp.rename(target)
        results.append((fp, target))
    return results

def main():
    parser = argparse.ArgumentParser(description="Rename ConEd IDR files based on first-line header.")
    parser.add_argument("files", nargs='+', help="List of files to rename")
    args = parser.parse_args()
    pairs = rename_files([Path(f) for f in args.files])
    for old, new in pairs:
        print(f"{old.name} -> {new.name}")

if __name__ == "__main__":
    main()
