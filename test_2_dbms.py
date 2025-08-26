import sqlite3
import requests
import pytest
from config import API_KEY

BASE_URL = "https://www.alphavantage.co/query"

#Test 1: Valid API call
def test_valid_stock_overview():
    """Tests if a valid stock symbol returns a successful response."""
    params ={
        "function": "OVERVIEW",
        "symbol": "IBM",
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)

    assert response.status_code == 200 #aka its OK

    data = response.json()
    assert "Symbol" in data
    assert data["Symbol"] == "IBM"

#Test 2: Invalid API call
def test_invalid_stock_symbol():
    """Tests if an invalid stock symbol returns an error message."""
    params ={
        "function": "OVERVIEW",
        "symbol": "INVALID_SYMBOLAAAAAAAAAAAAAA",
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)

    assert response.status_code == 200 #API still returns 200 but with error message

    data = response.json()
    assert data == {}  # Invalid symbol returns empty dictionary    
    #assert "Error Message" in data or "Note" in data

#Test 3: Test data types
def test_data_types_for_valid_stock():
    """Tests the data types of the response fields."""
    params ={
        "function": "OVERVIEW",
        "symbol": "AAPL",
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)

    assert response.status_code == 200

    data = response.json()
    assert data["MarketCapitalization"].isdigit()
    assert float(data["PERatio"])
    # assert isinstance(data["Symbol"], str)
    # assert isinstance(data["Open"], str)
    # assert isinstance(data["High"], str)
    # assert isinstance(data["Low"], str)
    # assert isinstance(data["Price"], str)

def setup_database():
    conn = sqlite3.connect("stock_data.db")
    cursor= conn.cursor()
    #time to create a table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_overview (
        symbol TEXT PRIMARY KEY,
        name TEXT,
        market_cap INTEGER
    )
    """)
    conn.commit()
    conn.close()

#Test 4: Testing saving to and retrieving from the database
def test_database_integration():
    """Fetching data, saving it to SQLite, and verifying it was aved correctly."""
    setup_database()

    #1. Fetch data from API
    params ={
        "function": "OVERVIEW",
        "symbol": "MSFT",
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 200
    data = response.json()
    symbol = data["Symbol"]
    name = data["Name"]
    market_cap = int(data["MarketCapitalization"])

    #2. Save to database
    conn = sqlite3.connect("stock_data.db")
    cursor = conn.cursor()
    cursor.execute("REPLACE INTO stock_overview (symbol, name, market_cap) VALUES (?, ?, ?)",
                   (symbol, name, market_cap))
    conn.commit()

    #3. Retrieve from database to verify
    cursor.execute("SELECT name, market_cap FROM stock_overview WHERE symbol = ?", (symbol,))
    db_result = cursor.fetchone()
    conn.close()

    assert db_result is not None
    db_name, db_market_cap = db_result

    #4. Assert that data in DB matches API data
    assert db_name == name
    assert db_market_cap == market_cap