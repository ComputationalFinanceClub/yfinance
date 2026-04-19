from datetime import date
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.forward_pe import get_forward_pe, get_multiple_fwd_pes
from api.momentum import analyze_momentum, analyze_multiple_momentum
from api.database import get_stored_forward_pe_data, get_all_tickers, get_historical_data, get_historical_data_multiple

# Import database module to ensure tables are created on startup
import api.database

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/fwd-pe/{ticker}")
def forward_pe(ticker: str):
    fwd_pe, price, fwd_eps, trl_eps, div_rate, cy_eps = get_forward_pe(ticker)
    return {
        "date": date.today().isoformat(),
        "ticker": ticker.upper(),
        "price": price,
        "forwardPE": fwd_pe,
        "forwardEPS": fwd_eps,
        "trailingEPS": trl_eps,
        "dividendRate": div_rate,
        "currentYearEPS": cy_eps
    }

@app.get("/fwd-pe/multiple/")
def forward_pe_multiple(tickers: str):
    ticker_list = tickers.split(",")
    data = get_multiple_fwd_pes(ticker_list)
    return {"tickers": data}

@app.get("/momentum/multiple/")
def momentum_multiple(tickers: str):
    ticker_list = [t.strip() for t in tickers.split(",") if t.strip()]
    if not ticker_list:
        return {"error": "No valid tickers provided", "tickers": {}}
    results = analyze_multiple_momentum(ticker_list)
    return {"tickers": results}

@app.get("/momentum/{ticker}")
def momentum(ticker: str):
    return analyze_momentum(ticker)

@app.get("/stored-data/{ticker}")
def get_stored_data(ticker: str):
    """Get today's stored data for a specific ticker"""
    data = get_stored_forward_pe_data(ticker)
    if data:
        return {
            "date": data.fetch_date.isoformat(),
            "ticker": data.ticker,
            "currentPrice": data.current_price,
            "trailingEPS": data.trailing_eps,
            "forwardEPS": data.forward_eps,
            "forwardPE": data.forward_pe,
            "dividendRate": data.dividend_rate,
            "currentYearEPS": data.eps_current_year,
            "fetchedAt": data.fetched_at.isoformat()
        }
    return {"error": "No data found for ticker"}

@app.get("/stored-data/")
def get_all_stored_data():
    """Get all today's stored data"""
    data = get_stored_forward_pe_data()
    return {
        "data": [
            {
                "date": item.fetch_date.isoformat(),
                "ticker": item.ticker,
                "currentPrice": item.current_price,
                "trailingEPS": item.trailing_eps,
                "forwardEPS": item.forward_eps,
                "forwardPE": item.forward_pe,
                "dividendRate": item.dividend_rate,
                "currentYearEPS": item.eps_current_year,
                "fetchedAt": item.fetched_at.isoformat()
            } for item in data
        ]
    }

@app.get("/tickers/")
def get_tickers():
    """Get list of all tickers in the database"""
    return {"tickers": get_all_tickers()}

@app.get("/historical/{ticker}")
def get_ticker_history(ticker: str, limit: int = 30):
    """Get historical data for a ticker"""
    data = get_historical_data(ticker, limit)
    if not data:
        return {"error": f"No historical data found for ticker {ticker.upper()}"}
    
    return {
        "ticker": ticker.upper(),
        "records": [
            {
                "date": item.fetch_date.isoformat(),
                "currentPrice": item.current_price,
                "trailingEPS": item.trailing_eps,
                "forwardEPS": item.forward_eps,
                "forwardPE": item.forward_pe,
                "dividendRate": item.dividend_rate,
                "currentYearEPS": item.eps_current_year,
                "fetchedAt": item.fetched_at.isoformat()
            } for item in data
        ]
    }

@app.get("/historical/multiple/")
def get_multiple_ticker_history(tickers: str, limit: int = 30):
    """Get historical data for multiple tickers simultaneously
    
    Args:
        tickers: Comma-separated ticker symbols (e.g., 'AAPL,MSFT,GOOGL')
        limit: Number of records per ticker (default 30)
    
    Example: /historical/multiple/?tickers=AAPL,MSFT,GOOGL&limit=100
    """
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    if not ticker_list:
        return {"error": "No valid tickers provided"}
    
    data = get_historical_data_multiple(ticker_list, limit)
    
    return {
        "tickers": {
            ticker: {
                "records": [
                    {
                        "date": item.fetch_date.isoformat(),
                        "currentPrice": item.current_price,
                        "trailingEPS": item.trailing_eps,
                        "forwardEPS": item.forward_eps,
                        "forwardPE": item.forward_pe,
                        "dividendRate": item.dividend_rate,
                        "currentYearEPS": item.eps_current_year,
                        "fetchedAt": item.fetched_at.isoformat()
                    } for item in records
                ]
            }
            for ticker, records in data.items()
        }
    }
