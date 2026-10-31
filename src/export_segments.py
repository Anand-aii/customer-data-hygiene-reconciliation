import pandas as pd
from pathlib import Path

INPUT = "output/customer_cleaned.xlsx"
SUPPRESSION_FILE = "input/suppression_list.csv"

SEGMENTS = {
    "Lapsed": "lapsed.csv",
    "Proposal Abandoned": "proposal_abandoned.csv",
    "Web Engagers": "web_engagers.csv",
    "Product Expiration": "product_expiration.csv"
}

Path("output/segments").mkdir(parents=True, exist_ok=True)
Path("reports").mkdir(exist_ok=True)

df = pd.read_excel(INPUT, sheet_name="Master Audit", dtype=str)
suppression = pd.read_csv(
    SUPPRESSION_FILE,
    dtype=str,
    keep_default_na=False
)

# Normalize email addresses for matching
df["email_key"] = df["email"].fillna("").str.strip().str.lower()

suppression_emails = set(
    suppression["email"].str.strip().str.lower()
)

suppression_emails.discard("")

# Preserve all records and flag suppression matches
df["suppression_status"] = df["email_key"].apply(
    lambda email: "Suppressed"
    if email in suppression_emails
    else "Not Suppressed"
)

suppressed = df[df["suppression_status"] == "Suppressed"].copy()

# Keep suppressed records out of marketing exports
exportable = df[df["suppression_status"] == "Not Suppressed"].copy()

summary = []

for segment, filename in SEGMENTS.items():
    segment_df = exportable[exportable["segment"] == segment].copy()

    segment_df.drop(columns=["email_key"], errors="ignore").to_csv(
        f"output/segments/{filename}",
        index=False
    )

    summary.append({
        "Segment": segment,
        "Total Records": len(df[df["segment"] == segment]),
        "Suppressed": len(suppressed[suppressed["segment"] == segment]),
        "Exported": len(segment_df),
        "Output File": filename
    })

    print(
        f"{segment}: {len(segment_df)} exported, "
        f"{len(suppressed[suppressed['segment'] == segment])} suppressed"
    )

# Save suppression audit separately
suppressed.drop(columns=["email_key"], errors="ignore").to_csv(
    "reports/suppression_matches.csv",
    index=False
)

# Save unmatched segments
unmatched = df[
    df["segment"].isna() |
    ~df["segment"].isin(SEGMENTS.keys())
].copy()

unmatched.drop(columns=["email_key"], errors="ignore").to_csv(
    "reports/unmatched_segments.csv",
    index=False
)

# Save quality review records
review = df[df["quality_status"] == "Review"].copy()
review.drop(columns=["email_key"], errors="ignore").to_csv(
    "reports/records_for_review.csv",
    index=False
)

pd.DataFrame(summary).to_csv(
    "reports/segment_summary.csv",
    index=False
)

print("\nEXPORT COMPLETED")
print("Total records:", len(df))
print("Suppressed records:", len(suppressed))
print("Unmatched segment records:", len(unmatched))
print("Records requiring review:", len(review))
print("Suppression audit: reports/suppression_matches.csv")
