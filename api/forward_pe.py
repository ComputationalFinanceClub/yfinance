from typing import Optional
import yfinance as yf
from api.database import save_forward_pe_data

def _get_optional_rounded(info: dict, key: str, ndigits: Optional[int] = None) -> Optional[float]:
    """
    Helper to safely extract a numeric field from info and optionally round it.
    Returns None on missing or invalid values.
    """
    raw = info.get(key)
    if raw is None:
        return None
    try:
        val = float(raw)
    except (TypeError, ValueError):
        return None
    return round(val, ndigits) if ndigits is not None else val

def get_forward_pe(ticker_symbol: str) -> tuple[Optional[float], Optional[float], Optional[float], Optional[float], Optional[float], Optional[float]]:
    stock = yf.Ticker(ticker_symbol.upper())
    info: dict = stock.info

    # forward PE (1 decimal), price (raw), forward EPS (2 decimals), trailing EPS (2), dividendRate (2), epsCurrentYear (2)
    fwd_pe = _get_optional_rounded(info, "forwardPE", 1)
    price = info.get("currentPrice")
    fwd_eps = _get_optional_rounded(info, "forwardEps", 2)
    trl_eps = _get_optional_rounded(info, "trailingEps", 2)
    div_rate = _get_optional_rounded(info, "dividendRate", 2)
    cy_eps = _get_optional_rounded(info, "epsCurrentYear", 2)

    # Save all fields to database
    save_forward_pe_data(ticker_symbol, price, trl_eps, fwd_eps, fwd_pe, div_rate, cy_eps)

    return fwd_pe, price, fwd_eps, trl_eps, div_rate, cy_eps

def get_multiple_fwd_pes(ticker_symbols: list[str]):
    fwd_pe_data = {}
    for ticker in ticker_symbols:
        fwd_pe, price, fwd_eps, trl_eps, div_rate, cy_eps = get_forward_pe(ticker)
        fwd_pe_data[ticker.upper()] = {
            "currentPrice": price,
            "trailingEPS": trl_eps,
            "forwardEPS": fwd_eps,
            "forwardPE": fwd_pe,
            "dividendRate": div_rate,
            "currentYearEPS": cy_eps
        }
    return fwd_pe_data

if __name__ == "__main__":
    ticker = input("Enter a stock ticker symbol: ")
    forward_pe, current_price, forward_eps, trailing_eps, dividend_rate, current_year_eps = get_forward_pe(ticker)
    if forward_pe is not None and forward_eps is not None and trailing_eps is not None:
        print(f"{ticker.upper()} Forward P/E Ratio: {forward_pe}")
        print(f"{ticker.upper()} Current Price: ${current_price}")
        print(f"{ticker.upper()} Forward EPS: ${forward_eps}")
        print(f"{ticker.upper()} Trailing EPS: ${trailing_eps}")
        print(f"{ticker.upper()} Dividend Rate: {dividend_rate}")
        print(f"{ticker.upper()} Current Year EPS: {current_year_eps}")
    else:
        print("Forward P/E data not available.")
    # list ["msft", "aapl", "googl"]
    # string "msft,aapl,googl"
    tickers_input = input("Enter multiple stock ticker symbols (comma-separated): ")
    ticker_list = [ticker.strip() for ticker in tickers_input.split(",")]