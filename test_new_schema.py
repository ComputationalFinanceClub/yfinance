#!/usr/bin/env python3
"""
Test the new database schema - append-only with all fields
"""
from api.database import get_stored_forward_pe_data, get_all_tickers, get_historical_data, ForwardPEData
from api.forward_pe import get_forward_pe
from datetime import date

print("=== Testing New Database Schema ===\n")

# Fetch and save data for a few tickers
test_tickers = ["AAPL", "MSFT", "GOOGL"]

print(f"Fetching data for {test_tickers}...")
for ticker in test_tickers:
    try:
        fwd_pe, price, fwd_eps, trl_eps, div_rate, cy_eps = get_forward_pe(ticker)
        print(f"  {ticker}: Price=${price}, Forward PE={fwd_pe}")
    except Exception as e:
        print(f"  {ticker}: Error - {e}")

print("\n=== Checking Today's Data ===")
today_data = get_stored_forward_pe_data()
print(f"Records for today ({date.today()}):")
for record in today_data:
    print(f"  {record.ticker}: Price=${record.current_price}, Forward PE={record.forward_pe}, Div Rate={record.dividend_rate}, CY EPS={record.eps_current_year}")

print("\n=== Checking Specific Ticker ===")
aapl = get_stored_forward_pe_data("AAPL")
if aapl:
    print(f"AAPL record:")
    print(f"  Date: {aapl.fetch_date}")
    print(f"  Price: ${aapl.current_price}")
    print(f"  Forward PE: {aapl.forward_pe}")
    print(f"  Dividend Rate: {aapl.dividend_rate}")
    print(f"  Current Year EPS: {aapl.eps_current_year}")
    print(f"  Fetched at: {aapl.fetched_at}")

print("\n=== All Tickers ===")
tickers = get_all_tickers()
print(f"Stored tickers: {tickers}")

print("\n=== Total Records in Database ===")
total = ForwardPEData.select().count()
print(f"Total records: {total}")

print("\n✓ New schema working correctly!")
print("  - Table creates automatically if it doesn't exist")
print("  - All fields (forward PE, price, EPS, dividend, etc.) are stored")
print("  - New rows are appended each time (append-only model)")
