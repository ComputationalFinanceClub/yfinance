#!/usr/bin/env python3
"""
Test append-only behavior - fetch the same ticker twice and verify new row is created
"""
from api.forward_pe import get_forward_pe
from api.database import ForwardPEData
import sqlite3

print("=== Testing Append-Only Behavior ===\n")

# Get current count for AAPL
conn = sqlite3.connect('stock_data.db')
cursor = conn.cursor()
cursor.execute('SELECT count(*) FROM forwardpedata WHERE ticker = "AAPL"')
initial_count = cursor.fetchone()[0]
conn.close()
print(f"Initial AAPL records: {initial_count}")

# Fetch AAPL again
print("Fetching AAPL again...")
get_forward_pe('AAPL')

# Check count again
conn = sqlite3.connect('stock_data.db')
cursor = conn.cursor()
cursor.execute('SELECT count(*) FROM forwardpedata WHERE ticker = "AAPL"')
final_count = cursor.fetchone()[0]
conn.close()
print(f"Final AAPL records: {final_count}")

if final_count == initial_count + 1:
    print("\n✓ Append-only working! New row was created.")
else:
    print(f"\n✗ Issue: Expected {initial_count + 1} records but got {final_count}")

# Show all AAPL records
print("\nAll AAPL records:")
for record in ForwardPEData.select().where(ForwardPEData.ticker == 'AAPL'):
    print(f"  {record.fetch_date} @ {record.fetched_at}: Price=${record.current_price}, Forward PE={record.forward_pe}")
