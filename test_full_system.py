#!/usr/bin/env python3
"""
Test script to verify database functionality and API endpoints
"""
import requests
import json
from api.database import get_stored_forward_pe_data, get_all_tickers
from api.forward_pe import get_forward_pe

def test_database_directly():
    """Test database functions directly"""
    print("=== Testing Database Directly ===")

    # Check stored data
    all_data = get_stored_forward_pe_data()
    print(f"Total records in database: {len(all_data)}")

    if all_data:
        print("Sample records:")
        for i, data in enumerate(all_data[:3]):  # Show first 3 records
            print(f"  {data.ticker}: Price={data.current_price}, Forward PE={data.forward_pe}")

    # Get all tickers
    tickers = get_all_tickers()
    print(f"Stored tickers: {tickers}")

def test_forward_pe_integration():
    """Test that forward_pe function saves to database"""
    print("\n=== Testing Forward PE Integration ===")

    # Fetch data for a new ticker
    test_ticker = "NVDA"  # NVIDIA
    print(f"Fetching data for {test_ticker}...")

    try:
        fwd_pe, price, fwd_eps, trl_eps = get_forward_pe(test_ticker)
        print(f"Live data - {test_ticker}: Price={price}, Forward PE={fwd_pe}")

        # Check if it was saved
        stored_data = get_stored_forward_pe_data(test_ticker)
        if stored_data:
            print(f"✓ Data saved to database: Price={stored_data.current_price}, Forward PE={stored_data.forward_pe}")
        else:
            print("✗ Data not found in database")

    except Exception as e:
        print(f"Error fetching {test_ticker}: {e}")

def test_api_endpoints():
    """Test API endpoints if server is running"""
    print("\n=== Testing API Endpoints ===")

    base_url = "http://localhost:8000"

    try:
        # Test stored data endpoint
        response = requests.get(f"{base_url}/stored-data/")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ API working - {len(data.get('data', []))} records retrieved")
        else:
            print(f"✗ API not responding (status: {response.status_code})")

        # Test tickers endpoint
        response = requests.get(f"{base_url}/tickers/")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Tickers endpoint working - {len(data.get('tickers', []))} tickers")
        else:
            print(f"✗ Tickers endpoint not working (status: {response.status_code})")

    except requests.exceptions.ConnectionError:
        print("⚠ API server not running - start with: uvicorn api.main:app --reload")

def check_database_file():
    """Check if database file exists"""
    print("\n=== Database File Check ===")

    import os
    db_path = "stock_data.db"
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"✓ Database file exists: {db_path} ({size} bytes)")
    else:
        print(f"✗ Database file not found: {db_path}")

if __name__ == "__main__":
    test_database_directly()
    test_forward_pe_integration()
    test_api_endpoints()
    check_database_file()

    print("\n=== Summary ===")
    print("To test API endpoints, run: uvicorn api.main:app --reload")
    print("Then visit: http://localhost:8000/docs for interactive API docs")