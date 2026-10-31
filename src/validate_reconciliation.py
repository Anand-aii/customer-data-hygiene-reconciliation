import pandas as pd

FILE = "output/reconciliation_results.xlsx"

df = pd.read_excel(
    FILE,
    sheet_name="All Matches"
)

print("\nRECONCILIATION VALIDATION")
print("-------------------------")

checks = {
    "Total source records are 30": len(df) == 30,
    "All source IDs are unique": df["source_record_id"].is_unique,
    "No missing match classifications": df["match_type"].notna().all(),
    "All records classified": (
        df["match_type"].isin([
            "Exact Email",
            "Exact Phone",
            "Possible Fuzzy Match",
            "Unmatched"
        ]).all()
    ),
    "Five fuzzy matches found": (
        (df["match_type"] == "Possible Fuzzy Match").sum() == 5
    ),
    "Five unmatched records found": (
        (df["match_type"] == "Unmatched").sum() == 5
    )
}

for name, passed in checks.items():
    print(("PASS" if passed else "FAIL") + " - " + name)

print("\nTotal records:", len(df))
print("Unique source IDs:", df["source_record_id"].nunique())

if all(checks.values()):
    print("\nALL RECONCILIATION CHECKS PASSED!")
else:
    print("\nVALIDATION FAILED - PLEASE REVIEW")
