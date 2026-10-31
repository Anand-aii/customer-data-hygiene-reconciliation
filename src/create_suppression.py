import pandas as pd
from pathlib import Path

Path("input").mkdir(exist_ok=True)

df = pd.read_csv("input/customer_raw.csv", dtype=str, keep_default_na=False)

# Create 10 fictional opt-out records from our test dataset
eligible = df.iloc[20:500]
eligible = eligible[eligible["email"].str.strip() != ""]

suppression = eligible[["email"]].head(10).copy()
suppression["reason"] = "Demo opt-out record"

suppression.to_csv("input/suppression_list.csv", index=False)

print("Demo suppression list created")
print("Suppression records:", len(suppression))
print("File: input/suppression_list.csv")
