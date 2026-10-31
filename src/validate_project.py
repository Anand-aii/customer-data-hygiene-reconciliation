import pandas as pd
from pathlib import Path

MASTER_FILE = "output/customer_cleaned.xlsx"
SUPPRESSION_FILE = "input/suppression_list.csv"
SEGMENT_DIR = Path("output/segments")

segments = [
    "lapsed.csv",
    "proposal_abandoned.csv",
    "web_engagers.csv",
    "product_expiration.csv"
]

master = pd.read_excel(MASTER_FILE, sheet_name="Master Audit", dtype=str)

suppression = pd.read_csv(
    SUPPRESSION_FILE,
    dtype=str,
    keep_default_na=False
)

suppressed_emails = set(
    suppression["email"].str.strip().str.lower()
)

suppressed_emails.discard("")

all_exports = []

for filename in segments:
    path = SEGMENT_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing export: {filename}")

    data = pd.read_csv(path, dtype=str, keep_default_na=False)
    all_exports.append(data)

combined = pd.concat(all_exports, ignore_index=True)

export_emails = set(
    combined["email"].str.strip().str.lower()
)

export_emails.discard("")

leaked = export_emails.intersection(suppressed_emails)

unmatched = pd.read_csv(
    "reports/unmatched_segments.csv",
    dtype=str,
    keep_default_na=False
)

print("\nPROJECT VALIDATION REPORT")
print("-------------------------")

checks = {
    "Master record count is 515": len(master) == 515,
    "Four segment files exist": len(all_exports) == 4,
    "Exported records total 505": len(combined) == 505,
    "Suppressed records excluded": len(leaked) == 0,
    "Unmatched segment records are zero": len(unmatched) == 0
}

for check, passed in checks.items():
    print(("PASS" if passed else "FAIL") + " - " + check)

print("\nMaster records:", len(master))
print("Exported records:", len(combined))
print("Suppression matches:", len(suppressed_emails))
print("Suppressed emails found in exports:", len(leaked))

if all(checks.values()):
    print("\nALL VALIDATION CHECKS PASSED!")
else:
    print("\nSOME CHECKS FAILED. PLEASE REVIEW.")
