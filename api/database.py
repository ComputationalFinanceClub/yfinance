from peewee import SqliteDatabase, Model, CharField, FloatField, DateTimeField, DateField, fn
import datetime
from datetime import date

# Create a SQLite database
db = SqliteDatabase('stock_data.db')

class ForwardPEData(Model):
    """Store historical forward PE data, appending new rows each day per ticker"""
    ticker = CharField(max_length=10)  # No unique constraint - allow multiple rows per ticker
    current_price = FloatField(null=True)
    trailing_eps = FloatField(null=True)
    forward_eps = FloatField(null=True)
    forward_pe = FloatField(null=True)
    dividend_rate = FloatField(null=True)
    eps_current_year = FloatField(null=True)
    fetch_date = DateField(default=date.today)  # Date the data was fetched
    fetched_at = DateTimeField(default=datetime.datetime.now)  # Timestamp of fetch

    class Meta:
        database = db
        indexes = (
            (('ticker', 'fetch_date'), False),  # Speed up lookups by ticker and date
        )

def create_tables():
    """Create tables if they don't exist. Uses safe=True to skip if already exists."""
    try:
        db.create_tables([ForwardPEData], safe=True)
    except Exception as e:
        print(f"Warning: Could not create tables: {e}")

# Initialize tables when module is imported
create_tables()

def save_forward_pe_data(ticker: str, price: float = None, trailing_eps: float = None,
                        forward_eps: float = None, forward_pe: float = None,
                        dividend_rate: float = None, eps_current_year: float = None):
    """Append a new row for today's data. No updates - append only."""
    today = date.today()
    
    # Always create a new record for today's data
    data = ForwardPEData.create(
        ticker=ticker.upper(),
        current_price=price,
        trailing_eps=trailing_eps,
        forward_eps=forward_eps,
        forward_pe=forward_pe,
        dividend_rate=dividend_rate,
        eps_current_year=eps_current_year,
        fetch_date=today,
        fetched_at=datetime.datetime.now()
    )
    return data

def get_stored_forward_pe_data(ticker: str = None, fetch_date: date = None):
    """Get stored forward PE data.
    
    Args:
        ticker: Optional ticker symbol to filter by
        fetch_date: Optional date to filter by (defaults to today)
    
    Returns:
        Single record if ticker specified, list of records otherwise
    """
    if fetch_date is None:
        fetch_date = date.today()
    
    query = ForwardPEData.select().where(ForwardPEData.fetch_date == fetch_date)
    
    if ticker:
        try:
            return query.where(ForwardPEData.ticker == ticker.upper()).get()
        except ForwardPEData.DoesNotExist:
            return None
    else:
        return list(query.order_by(ForwardPEData.ticker))

def get_all_tickers():
    """Get list of all unique tickers in database."""
    query = ForwardPEData.select(ForwardPEData.ticker.distinct())
    return [data.ticker for data in query]

def get_historical_data(ticker: str, limit: int = 30):
    """Get historical data for a ticker (last N records).
    
    Args:
        ticker: Ticker symbol
        limit: Number of records to return (default 30 days)
    
    Returns:
        List of records ordered by date descending
    """
    return list(
        ForwardPEData.select()
        .where(ForwardPEData.ticker == ticker.upper())
        .order_by(ForwardPEData.fetch_date.desc())
        .limit(limit)
    )

def get_historical_data_multiple(tickers: list[str], limit: int = 30):
    """Get historical data for multiple tickers.
    
    Args:
        tickers: List of ticker symbols
        limit: Number of records per ticker (default 30)
    
    Returns:
        Dictionary with ticker symbols as keys and lists of records as values
    """
    result = {}
    for ticker in tickers:
        result[ticker.upper()] = get_historical_data(ticker, limit)
    return result