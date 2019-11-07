import sqlite3
import pandas as pd

conn = sqlite3.connect('aggregated_data.db')

df = pd.read_csv("aggregated_data.csv")
df.to_sql("Properties", conn, if_exists='append', index=False)