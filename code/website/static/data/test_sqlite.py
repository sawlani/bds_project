import sqlite3
import pandas as pd

conn = sqlite3.connect('aggregated_data.db')

c = conn.cursor()
c.execute("SELECT * FROM Properties LIMIT 1;")
print(c.fetchall())