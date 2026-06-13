import pytest
from datetime import datetime, timezone

from lib.services.configuration.type.query.stock_historical_bars import StockHistoricalBarsQueryType


def test_name_is_class_constant():
    assert StockHistoricalBarsQueryType.name == 'stock-historical-bars'


def test_valid_construction():
    qt = StockHistoricalBarsQueryType(symbols=['AAPL'], frequency='1d')
    assert qt.symbols == ['AAPL']
    assert qt.frequency == '1d'
    assert qt.start is None
    assert qt.end is None


def test_symbols_required():
    with pytest.raises(TypeError):
        StockHistoricalBarsQueryType(frequency='1d')  # type: ignore[call-arg]


def test_frequency_required():
    with pytest.raises(TypeError):
        StockHistoricalBarsQueryType(symbols=['AAPL'])  # type: ignore[call-arg]


def test_invalid_frequency_raises():
    with pytest.raises(ValueError):
        StockHistoricalBarsQueryType(symbols=['AAPL'], frequency='5m')


def test_valid_frequencies():
    StockHistoricalBarsQueryType(symbols=['AAPL'], frequency='1d')
    StockHistoricalBarsQueryType(symbols=['AAPL'], frequency='1m')


def test_start_parsed_from_string():
    qt = StockHistoricalBarsQueryType(symbols=['AAPL'], frequency='1d', start='2024-01-01T00:00:00')
    assert isinstance(qt.start, datetime)
    assert qt.start.tzinfo == timezone.utc


def test_end_parsed_from_string():
    qt = StockHistoricalBarsQueryType(symbols=['AAPL'], frequency='1d', end='2024-06-01T00:00:00')
    assert isinstance(qt.end, datetime)
    assert qt.end.tzinfo == timezone.utc


def test_datetime_with_tz_preserved():
    qt = StockHistoricalBarsQueryType(symbols=['AAPL'], frequency='1d', start='2024-01-01T00:00:00+05:00')
    assert qt.start is not None
    assert qt.start.utcoffset() is not None


def test_to_dict_required_fields():
    qt = StockHistoricalBarsQueryType(symbols=['AAPL', 'MSFT'], frequency='1d')
    d = qt.to_dict()
    assert d['symbols'] == ['AAPL', 'MSFT']
    assert d['frequency'] == '1d'
    assert 'start' not in d
    assert 'end' not in d


def test_to_dict_with_optional_fields():
    qt = StockHistoricalBarsQueryType(
        symbols=['AAPL'],
        frequency='1m',
        start='2024-01-01T00:00:00',
        end='2024-06-01T00:00:00',
    )
    d = qt.to_dict()
    assert 'start' in d
    assert 'end' in d
    assert isinstance(d['start'], str)
    assert isinstance(d['end'], str)


def test_to_dict_excludes_name():
    qt = StockHistoricalBarsQueryType(symbols=['AAPL'], frequency='1d')
    assert 'name' not in qt.to_dict()
