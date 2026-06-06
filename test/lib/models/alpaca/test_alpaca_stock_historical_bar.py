from lib.models.alpaca.alpaca_stock_historical_bar import AlpacaStockHistoricalBar


def test_alpaca_stock_historical_bar_tablename() -> None:
    assert AlpacaStockHistoricalBar.__tablename__ == "stock_historical_bars"


def test_alpaca_stock_historical_bar_has_all_columns() -> None:
    column_names = {c.key for c in AlpacaStockHistoricalBar.__table__.columns}
    expected = {
        "id", "created_at", "updated_at", "source",
        "symbol", "time", "open", "high", "low", "close",
        "volume", "trade_count", "volume_weighted_avg_price",
    }
    assert expected == column_names


def test_alpaca_stock_historical_bar_from_dict() -> None:
    data = {
        "symbol": "AAPL",
        "time": "2026-01-01T00:00:00Z",
        "open": 100,
        "high": 200,
        "low": 50,
        "close": 150,
        "volume": 1000,
        "trade_count": 4,
        "volume_weighted_avg_price": 125,
    }
    bar = AlpacaStockHistoricalBar.from_dict(data)
    assert bar.symbol == "AAPL"
    assert bar.open == 100
