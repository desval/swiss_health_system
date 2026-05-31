"""
Build source manifest for data/statistik-ra workbooks.
Stdlib-only — no external dependencies required.

Usage:
    python code/build_manifest.py

Output:
    output/data/source_manifest.csv
"""

import os
import re
import csv
from zipfile import ZipFile
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(ROOT, "data", "statistik-ra")
OUTPUT_DIR = os.path.join(ROOT, "output", "data")
MANIFEST_PATH = os.path.join(OUTPUT_DIR, "source_manifest.csv")

NS_M = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"

FILENAME_RE = re.compile(r"Statistik-RA-(\d{4})(?:-(\d+))?\.xlsx$", re.IGNORECASE)


# ── helpers ───────────────────────────────────────────────────────────────────

def _era(year: int) -> str:
    """Map calendar year to schema era label aligned to Swiss RA reform phases."""
    if year <= 2011:
        return "phase1_legacy"     # age + sex only
    if year <= 2019:
        return "phase2_transition"  # + prior hospitalisation
    return "phase3_modern"          # + 22 PCG groups


def _read_zip_text(zf: ZipFile, entry: str) -> str | None:
    """Return text content of a zip entry, or None if not found."""
    try:
        with zf.open(entry) as fh:
            return fh.read().decode("utf-8", errors="replace")
    except KeyError:
        return None


def _sheet_names(path: str) -> list[str]:
    """Extract ordered worksheet names from an XLSX file without openpyxl."""
    try:
        with ZipFile(path) as zf:
            wb_text = _read_zip_text(zf, "xl/workbook.xml")
            if not wb_text:
                return []
            root = ET.fromstring(wb_text)
            return [
                s.get("name", "")
                for s in root.findall(f"{{{NS_M}}}sheets/{{{NS_M}}}sheet")
            ]
    except Exception as exc:
        print(f"  WARNING: could not read sheets from {path}: {exc}")
        return []


# ── main ──────────────────────────────────────────────────────────────────────

def build_manifest() -> list[dict]:
    """Scan SOURCE_DIR and return a list of manifest records."""
    records = []
    for fname in sorted(os.listdir(SOURCE_DIR)):
        m = FILENAME_RE.match(fname)
        if not m:
            continue
        year = int(m.group(1))
        revision = int(m.group(2)) if m.group(2) else 0
        path = os.path.join(SOURCE_DIR, fname)
        sheets = _sheet_names(path)
        records.append(
            {
                "filename": fname,
                "year": year,
                "revision": revision,
                "era": _era(year),
                "n_sheets": len(sheets),
                "sheets": " | ".join(sheets),
                "is_canonical": False,  # filled in next pass
            }
        )

    # ── canonical selection rule: highest revision per year ───────────────────
    # For each year, mark the record with the highest revision as canonical.
    # If a year has only one record (no suffix), it is canonical by default.
    by_year: dict[int, list[dict]] = {}
    for r in records:
        by_year.setdefault(r["year"], []).append(r)

    for year_records in by_year.values():
        best = max(year_records, key=lambda r: r["revision"])
        best["is_canonical"] = True

    return records


def write_manifest(records: list[dict]) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    fields = ["filename", "year", "revision", "is_canonical", "era", "n_sheets", "sheets"]
    with open(MANIFEST_PATH, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(sorted(records, key=lambda r: (r["year"], r["revision"])))
    print(f"Manifest written: {MANIFEST_PATH}  ({len(records)} rows)")


def print_summary(records: list[dict]) -> None:
    canonical = [r for r in records if r["is_canonical"]]
    by_era = {}
    for r in canonical:
        by_era.setdefault(r["era"], []).append(r["year"])

    print(f"\n{'─' * 60}")
    print(f"  Total workbooks :  {len(records)}")
    print(f"  Canonical files :  {len(canonical)}")
    print(f"  Years covered   :  {min(r['year'] for r in records)}–{max(r['year'] for r in records)}")
    print()
    print("  Canonical by era:")
    for era, years in sorted(by_era.items()):
        print(f"    {era:28s}  {len(years):2d} years  ({min(years)}–{max(years)})")

    superseded = [r for r in records if not r["is_canonical"]]
    if superseded:
        print()
        print("  Superseded (lower revision kept but not canonical):")
        for r in superseded:
            canonical_rev = max(
                (x["revision"] for x in records if x["year"] == r["year"]),
            )
            print(f"    {r['filename']:45s}  →  superseded by revision {canonical_rev}")
    print(f"{'─' * 60}\n")


if __name__ == "__main__":
    print("Building Statistik-RA source manifest …")
    records = build_manifest()
    print_summary(records)
    write_manifest(records)
