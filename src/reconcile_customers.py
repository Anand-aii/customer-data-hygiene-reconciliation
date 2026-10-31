import pandas as pd
import re
from pathlib import Path
from rapidfuzz import process, fuzz

MASTER_FILE = "output/customer_cleaned.xlsx"
SOURCE_FILE = "input/reconciliation_source.csv"

Path("output").mkdir(exist_ok=True)
Path("reports").mkdir(exist_ok=True)


def normalize_email(value):
    return str(value).strip().lower()


def normalize_phone(value):
    return re.sub(r"\D", "", str(value))


def normalize_name(first, last):
    return (
        str(first).strip().lower() + " " +
        str(last).strip().lower()
    )


# Load datasets
master = pd.read_excel(
    MASTER_FILE,
    sheet_name="Master Audit",
    dtype=str
).fillna("")

source = pd.read_csv(
    SOURCE_FILE,
    dtype=str,
    keep_default_na=False
)

# Avoid duplicate copies of the same customer in master
master = master.drop_duplicates(
    subset=["customer_id"],
    keep="first"
).copy()

# Normalize master fields
master["email_key"] = master["email"].apply(normalize_email)
master["phone_key"] = master["phone"].apply(normalize_phone)

master["name_key"] = master.apply(
    lambda row: normalize_name(
        row["first_name"],
        row["last_name"]
    ),
    axis=1
)

# Create lookup dictionaries
email_lookup = {
    email: index
    for index, email in master["email_key"].items()
    if email
}

phone_lookup = {
    phone: index
    for index, phone in master["phone_key"].items()
    if phone
}

name_choices = {
    index: name
    for index, name in master["name_key"].items()
    if name.strip()
}

results = []

for _, row in source.iterrows():

    email = normalize_email(row["email"])
    phone = normalize_phone(row["phone"])

    name = normalize_name(
        row["first_name"],
        row["last_name"]
    )

    matched_index = None
    match_type = "Unmatched"
    match_score = 0

    # 1. Exact email match
    if email and email in email_lookup:
        matched_index = email_lookup[email]
        match_type = "Exact Email"
        match_score = 100

    # 2. Exact phone match
    elif phone and phone in phone_lookup:
        matched_index = phone_lookup[phone]
        match_type = "Exact Phone"
        match_score = 100

    # 3. Fuzzy name matching
    else:
        candidate = process.extractOne(
            name,
            name_choices,
            scorer=fuzz.ratio,
            score_cutoff=75
        )

        if candidate:
            matched_name, score, matched_index = candidate
            match_type = "Possible Fuzzy Match"
            match_score = round(score, 2)

    if matched_index is not None:
        matched_customer = master.loc[matched_index]

        matched_customer_id = matched_customer["customer_id"]
        matched_name = matched_customer["name_key"]
    else:
        matched_customer_id = ""
        matched_name = ""

    results.append({
        "source_record_id": row["source_record_id"],
        "source_name": name,
        "source_email": email,
        "source_phone": phone,
        "matched_customer_id": matched_customer_id,
        "matched_name": matched_name,
        "match_type": match_type,
        "match_score": match_score,
        "review_required": (
            "Yes" if match_type in [
                "Possible Fuzzy Match",
                "Unmatched"
            ] else "No"
        )
    })


# Create results dataframe
result_df = pd.DataFrame(results)

# Separate reports
fuzzy_matches = result_df[
    result_df["match_type"] == "Possible Fuzzy Match"
]

unmatched = result_df[
    result_df["match_type"] == "Unmatched"
]

summary = (
    result_df["match_type"]
    .value_counts()
    .rename_axis("Match Type")
    .reset_index(name="Records")
)

# Save complete reconciliation workbook
with pd.ExcelWriter(
    "output/reconciliation_results.xlsx",
    engine="openpyxl"
) as writer:

    result_df.to_excel(
        writer,
        sheet_name="All Matches",
        index=False
    )

    summary.to_excel(
        writer,
        sheet_name="Summary",
        index=False
    )

# Save separate CSV reports
fuzzy_matches.to_csv(
    "reports/fuzzy_matches_review.csv",
    index=False
)

unmatched.to_csv(
    "reports/unmatched_customers.csv",
    index=False
)

print("\nCUSTOMER RECONCILIATION COMPLETED")
print("---------------------------------")
print("Source records:", len(source))
print("Exact email matches:", (result_df["match_type"] == "Exact Email").sum())
print("Exact phone matches:", (result_df["match_type"] == "Exact Phone").sum())
print("Possible fuzzy matches:", len(fuzzy_matches))
print("Unmatched records:", len(unmatched))
print("Manual review required:", (result_df["review_required"] == "Yes").sum())

print("\nExcel report: output/reconciliation_results.xlsx")
print("Fuzzy review: reports/fuzzy_matches_review.csv")
print("Unmatched report: reports/unmatched_customers.csv")
