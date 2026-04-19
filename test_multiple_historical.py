#!/usr/bin/env python3
"""
Test getting historical data for multiple tickers
"""
from api.database import get_historical_data_multiple

print("=== Testing Multiple Tickers Historical Data ===\n")

tickers = ["AAPL", "MSFT", "GOOGL"]
print(f"Fetching historical data for: {tickers}\n")

data = get_historical_data_multiple(tickers, limit=2)

for ticker, records in data.items():
    print(f"{ticker}: {len(records)} records")
    for record in records:
        print(f"  {record.fetch_date}: Price=${record.current_price}, Forward PE={record.forward_pe}")
    print()

print("✓ Multiple tickers retrieval works!")
print("\nAPI Usage Examples:")
print("  GET /historical/multiple/?tickers=AAPL,MSFT&limit=10")
print("  GET /historical/multiple/?tickers=AAPL,MSFT,GOOGL,TSLA&limit=50")
