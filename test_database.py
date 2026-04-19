#!/usr/bin/env python3
"""
Test script to demonstrate the database functionality
"""
from api.database import create_tables, save_forward_pe_data, get_stored_forward_pe_data, get_all_tickers
from api.forward_pe import get_forward_pe

def test_database():
    # Create tables
    print("Creating database tables...")
    create_tables()

    # Test saving data manually
    print("Saving test data...")
    save_forward_pe_data("AAPL", 150.25, 6.15, 7.25, 20.8)
    save_forward_pe_data("MSFT", 305.50, 11.85, 13.45, 22.7)

    # Test fetching data
    print("Fetching stored data...")
    aapl_data = get_stored_forward_pe_data("AAPL")
    if aapl_data:
        print(f"AAPL data: Price={aapl_data.current_price}, Forward PE={aapl_data.forward_pe}")

    # Test fetching all data
    all_data = get_stored_forward_pe_data()
    print(f"Total records: {len(all_data)}")

    # Test getting tickers
    tickers = get_all_tickers()
    print(f"Stored tickers: {tickers}")

    # Test integration with forward_pe function
    print("Testing integration with forward_pe function...")
    try:
        fwd_pe, price, fwd_eps, trl_eps = get_forward_pe("TSLA")
        print(f"TSLA: Forward PE={fwd_pe}, Price={price}")

        # Check if it was saved
        tsla_data = get_stored_forward_pe_data("TSLA")
        if tsla_data:
            print("TSLA data saved to database successfully!")
    except Exception as e:
        print(f"Error fetching TSLA data: {e}")

if __name__ == "__main__":
    test_database()