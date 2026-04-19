#!/usr/bin/env python3
"""
Check database contents directly
"""
import sqlite3

conn = sqlite3.connect('stock_data.db')
cursor = conn.cursor()

# Get table info
cursor.execute("PRAGMA table_info(forwardpedata)")
columns = cursor.fetchall()
print("Table structure:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

print("\nDatabase contents:")
cursor.execute('SELECT * FROM forwardpedata ORDER BY last_updated DESC')
rows = cursor.fetchall()

for row in rows:
    print(f"  {row[1]}: Price={row[2]}, Trailing EPS={row[3]}, Forward EPS={row[4]}, Forward PE={row[5]}, Updated={row[6]}")

conn.close()