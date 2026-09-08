import pandas as pd
import sqlite3

# Load both sheets of the Excel file and combine them
df1 = pd.read_excel("data/online_retail_II.xlsx", sheet_name="Year 2009-2010")
df2 = pd.read_excel("data/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = pd.concat([df1, df2], ignore_index=True)

# Drop rows with no Customer ID — we can't track churn for unknown customers
df = df.dropna(subset=["Customer ID"])

# Drop cancelled orders (Invoice numbers starting with 'C')
df = df[~df["Invoice"].astype(str).str.startswith("C")]

# Drop bad data: zero or negative quantity/price
df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]

# Rename columns to be SQL-friendly (no spaces)
df = df.rename(columns={
    "Customer ID": "customer_id",
    "Invoice": "order_id",
    "InvoiceDate": "order_date",
    "StockCode": "product_id",
    "Description": "description",
    "Quantity": "quantity",
    "Price": "price",
    "Country": "country"
})

conn = sqlite3.connect("data/retail.db")
df.to_sql("orders", conn, if_exists="replace", index=False)
conn.close()

print(f"Loaded {len(df)} clean order rows into SQLite.")