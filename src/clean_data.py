import pandas as pd
import re
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

INPUT = "input/customer_raw.csv"
OUTPUT = "output/customer_cleaned.xlsx"

Path("output").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)

# Load original data as text
df = pd.read_csv(INPUT, dtype=str, keep_default_na=False)
original_count = len(df)

# Preserve original values
df["original_email"] = df["email"]
df["original_phone"] = df["phone"]

# Clean text fields
for col in ["first_name", "last_name", "email",
            "segment", "status", "country"]:
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

# Normalize phone and preserve as text
def clean_phone(value):
    digits = re.sub(r"\D", "", str(value))
    return str(digits) if digits else ""

df["phone"] = df["phone"].apply(clean_phone).astype("string")
df["original_phone"] = df["original_phone"].astype("string")

df["phone_status"] = df["phone"].apply(
    lambda x: "Missing" if not x
    else "Valid length" if 10 <= len(x) <= 15
    else "Check required"
)

# Detect exact duplicates
duplicate_columns = [
    "first_name", "last_name", "email", "phone"
]

df["duplicate_status"] = df.duplicated(
    subset=duplicate_columns,
    keep="first"
).map({
    True: "Duplicate",
    False: "Unique"
})

# Quality classification
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

# Export Excel workbook
with pd.ExcelWriter(OUTPUT, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Master Audit", index=False)
    summary.to_excel(writer, sheet_name="Quality Summary", index=False)

# Professional Excel formatting
wb = load_workbook(OUTPUT)

header_fill = PatternFill(
    "solid", fgColor="1F4E78"
)

header_font = Font(
    color="FFFFFF", bold=True
)

for ws in wb.worksheets:
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(
            horizontal="center"
        )

    for column_cells in ws.columns:
        letter = get_column_letter(column_cells[0].column)
        max_length = max(
            len(str(cell.value or ""))
            for cell in column_cells
        )
        ws.column_dimensions[letter].width = min(
            max(max_length + 3, 14), 35
        )

# Force phone columns to Excel text format
ws = wb["Master Audit"]

for column_name in ["phone", "original_phone"]:
    col_index = list(df.columns).index(column_name) + 1

    for row in range(2, ws.max_row + 1):
        cell = ws.cell(row=row, column=col_index)

        if cell.value is not None:
            cell.value = str(cell.value)
            cell.data_type = "s"
            cell.number_format = "@"

wb.save(OUTPUT)

print("\nDATA CLEANING COMPLETED")
print("-----------------------")
print("Original records:", original_count)
print("Duplicate records:", summary.loc[4, "Count"])
print("Passed records:", summary.loc[5, "Count"])
print("Review records:", summary.loc[6, "Count"])
print("Phone columns: Text format")
print("Excel formatting: Applied")
print("Excel report:", OUTPUT)
