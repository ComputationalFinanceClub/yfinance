from datetime import date, datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, Date, DateTime, select, distinct
)
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///stock_data.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


class ForwardPEData(Base):
    """Store historical forward PE data, appending new rows each day per ticker"""
    __tablename__ = "forward_pe_data"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), index=True, nullable=False)
    current_price = Column(Float, nullable=True)
    trailing_eps = Column(Float, nullable=True)
    forward_eps = Column(Float, nullable=True)
    forward_pe = Column(Float, nullable=True)
    dividend_rate = Column(Float, nullable=True)
    eps_current_year = Column(Float, nullable=True)
    fetch_date = Column(Date, nullable=False, default=date.today)
    fetched_at = Column(DateTime, nullable=False, default=datetime.now)


def create_tables() -> None:
    """Create tables if they don't exist."""
    Base.metadata.create_all(bind=engine)


create_tables()


def save_forward_pe_data(
    ticker: str,
    price: float | None = None,
    trailing_eps: float | None = None,
    forward_eps: float | None = None,
    forward_pe: float | None = None,
    dividend_rate: float | None = None,
    eps_current_year: float | None = None
) -> ForwardPEData:
    """Append a new row for today's data. No updates - append only."""
    today = date.today()
    with SessionLocal() as session:
        record = ForwardPEData(
            ticker=ticker.upper(),
            current_price=price,
            trailing_eps=trailing_eps,
            forward_eps=forward_eps,
            forward_pe=forward_pe,
            dividend_rate=dividend_rate,
            eps_current_year=eps_current_year,
            fetch_date=today,
            fetched_at=datetime.now()
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record


def get_stored_forward_pe_data(
    ticker: str | None = None,
    fetch_date: date | None = None
) -> list[ForwardPEData]:
    """Get stored forward PE data.

    Args:
        ticker: ticker symbol to filter by
        fetch_date: date to filter by (defaults to today)

    Returns:
        Single record if ticker specified, list of records otherwise
    """
    if fetch_date is None:
        fetch_date = date.today()

    with SessionLocal() as session:
        if ticker:
            stmt = select(ForwardPEData).where(
                ForwardPEData.ticker == ticker.upper(),
                ForwardPEData.fetch_date == fetch_date
            )
            result = session.execute(stmt).scalars().first()
            return [result] if result else []
        else:
            stmt = select(ForwardPEData).where(ForwardPEData.fetch_date == fetch_date).order_by(ForwardPEData.ticker)
            results: list[ForwardPEData] = list(session.execute(stmt).scalars().all())
            return results


def get_all_tickers() -> list[str]:
    """Get list of all unique tickers in database."""
    with SessionLocal() as session:
        stmt = select(distinct(ForwardPEData.ticker))
        rows = session.execute(stmt).scalars().all()
        return [r for r in rows]


def get_historical_data(ticker: str, limit: int = 30) -> list[ForwardPEData]:
    """Get historical data for a ticker (last N records)."""
    with SessionLocal() as session:
        stmt = (
            select(ForwardPEData)
            .where(ForwardPEData.ticker == ticker.upper())
            .order_by(ForwardPEData.fetch_date.desc())
            .limit(limit)
        )
        return list(session.execute(stmt).scalars().all())


def get_historical_data_multiple(tickers: list[str], limit: int = 30) -> dict[str, list[ForwardPEData]]:
    """Get historical data for multiple tickers."""
    result: dict[str, list[ForwardPEData]] = {}
    for ticker in tickers:
        result[ticker.upper()] = get_historical_data(ticker, limit)
    return result