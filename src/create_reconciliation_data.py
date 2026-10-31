import pandas as pd
from pathlib import Path

Path("input").mkdir(exist_ok=True)

df = pd.read_csv(
    "input/customer_raw.csv",
    dtype=str,
    keep_default_na=False
)

# Select customers with unique names
df["full_name"] = (
    df["first_name"].str.strip() + " " +
    df["last_name"].str.strip()
)

base = df.drop_duplicates(subset=["full_name"]).head(25)

records = []

for i, (_, row) in enumerate(base.iterrows()):
    first = row["first_name"].strip()
    last = row["last_name"].strip()

    record = {
        "source_record_id": f"SRC{i+1:03d}",
        "first_name": first,
        "last_name": last,
        "email": row["email"],
        "phone": row["phone"]
    }

    # 10 exact matches
    if 10 <= i < 20:
        record["email"] = f"changed_{i}@example.com"

    # 5 records with spelling differences
    if 20 <= i < 25:
        record["first_name"] = first[:-1] + "x"
        record["email"] = f"unknown_{i}@example.com"
        record["phone"] = f"999999000{i}"

    records.append(record)

# Add 5 completely new customers
new_customers = [
    ("Zyron", "Qwext"),
    ("Qadira", "Vex"),
    ("Nimble", "Zorath"),
    ("Velora", "Quix"),
    ("Tavren", "Xol")
]

for i, (first, last) in enumerate(new_customers):
    records.append({
        "source_record_id": f"SRC{26+i:03d}",
        "first_name": first,
        "last_name": last,
        "email": f"new{i}@example.com",
        "phone": f"888888000{i}"
    })

result = pd.DataFrame(records)

result.to_csv(
    "input/reconciliation_source.csv",
    index=False
)

print("Reconciliation test dataset created!")
print("Total source records:", len(result))
print("File: input/reconciliation_source.csv")
