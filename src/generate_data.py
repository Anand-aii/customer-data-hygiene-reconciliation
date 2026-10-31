
import pandas as pd
import random
from pathlib import Path

random.seed(42)

Path("input").mkdir(exist_ok=True)

first_names = [
    "Aarav", "Rahul", "Priya", "Ananya", "Vikram",
    "Neha", "Arjun", "Sneha", "Karan", "Meera"
]

last_names = [
    "Sharma", "Patel", "Kumar", "Reddy", "Singh",
    "Gupta", "Iyer", "Nair", "Verma", "Das"
]

segments = [
    "Lapsed",
    "Proposal Abandoned",
    "Web Engagers",
    "Product Expiration"
]

records = []

for i in range(1, 501):
    first = random.choice(first_names)
    last = random.choice(last_names)

    email = f"{first.lower()}.{last.lower()}{i}@example.com"
    phone = f"+91-{random.randint(6000000000, 9999999999)}"

    record = {
        "customer_id": f"CUST{i:04d}",
        "first_name": first,
        "last_name": last,
        "email": email,
        "phone": phone,
        "segment": random.choice(segments),
        "status": random.choice(["Active", "Inactive", "Pending"]),
        "country": "India"
    }

    # Introduce intentional data-quality issues
    if i % 25 == 0:
        record["email"] = ""

    if i % 30 == 0:
        record["phone"] = None

    if i % 40 == 0:
        record["first_name"] = "  " + first + "  "

    records.append(record)

df = pd.DataFrame(records)

# Add duplicate records for testing
duplicates = df.iloc[:15].copy()
df = pd.concat([df, duplicates], ignore_index=True)

df.to_csv("input/customer_raw.csv", index=False)

print("Dataset created successfully!")
print("Total records:", len(df))
print("Columns:", list(df.columns))
print("Output: input/customer_raw.csv")
