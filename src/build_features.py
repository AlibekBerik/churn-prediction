import sqlite3
import pandas as pd

conn = sqlite3.connect("data/retail.db")
with open("src/features.sql") as f:
    query = f.read()

rfm_df = pd.read_sql(query, conn)
rfm_df.to_csv("data/rfm_features.csv", index=False)

print(rfm_df["churned"].value_counts(normalize=True))