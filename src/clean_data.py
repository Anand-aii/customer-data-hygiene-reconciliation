
import pandas as pd
import re
from pathlib import Path

INPUT = "input/customer_raw.csv"
OUTPUT = "output/customer_cleaned.xlsx"

Path("output").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)

# Load original data
df = pd.read_csv(INPUT, dtype=str, keep_default_na=False)

original_count = len(df)

# Preserve original data
df["original_email"] = df["email"]
df["original_phone"] = df["phone"]

# Clean text fields
for col in ["first_name", "last_name", "email", "segment", "status", "country"]:
    df[col] = df[col].astype(str).str.strip()

# Normalize email
df["email"] = df["email"].str.lower()

# Email validation
email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

df["email_status"] = df["email"].apply(
    lambda x: "Missing" if not x
    else "Valid format" if re.fullmatch(email_pattern, x)
    else "Invalid format"
)

# Normalize phone
def clean_phone(value):
    digits = re.sub(r"\D", "", str(value))
    return digits if digits else ""

df["phone"] = df["phone"].apply(clean_phone)

df["phone_status"] = df["phone"].apply(
    lambda x: "Missing" if not x
    else "Valid length" if 10 <= len(x) <= 15
    else "Check required"
)

# Detect exact duplicate records
duplicate_columns = [
    "first_name",
    "last_name",
    "email",
    "phone"
]

df["duplicate_status"] = df.duplicated(
    subset=duplicate_columns,
    keep="first"
).map({
    True: "Duplicate",
    False: "Unique"
})

# Add quality flags
df["quality_status"] = "Review"

df.loc[
    (df["email_status"] == "Valid format") &
    (df["phone_status"] == "Valid length") &
    (df["duplicate_status"] == "Unique"),
    "quality_status"
] = "Passed"

# Summary
summary = pd.DataFrame({
    "Metric": [
        "Original records",
        "Missing emails",
        "Invalid email formats",
        "Missing phones",
        "Duplicate records",
        "Passed records",
        "Records requiring review"
    ],
    "Count": [
        original_count,
        (df["email_status"] == "Missing").sum(),
        (df["email_status"] == "Invalid format").sum(),
        (df["phone_status"] == "Missing").sum(),
        (df["duplicate_status"] == "Duplicate").sum(),
        (df["quality_status"] == "Passed").sum(),
        (df["quality_status"] == "Review").sum()
    ]
})

# Export workbook
with pd.ExcelWriter(OUTPUT, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Master Audit", index=False)
    summary.to_excel(writer, sheet_name="Quality Summary", index=False)

print("\nDATA CLEANING COMPLETED")
print("-----------------------")
print("Original records:", original_count)
print("Duplicate records:", summary.loc[4, "Count"])
print("Passed records:", summary.loc[5, "Count"])
print("Review records:", summary.loc[6, "Count"])
print("Excel report:", OUTPUT)
