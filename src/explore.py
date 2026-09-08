import sqlite3
import pandas as pd

conn = sqlite3.connect("data/retail.db")

print(pd.read_sql("SELECT * FROM orders LIMIT 5", conn))
print(pd.read_sql("SELECT COUNT(DISTINCT customer_id) as num_customers FROM orders", conn))
print(pd.read_sql("SELECT MIN(order_date) as earliest, MAX(order_date) as latest FROM orders", conn))