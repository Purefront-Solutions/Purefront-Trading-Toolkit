import pytest

from lib.services.configuration.type.query.assets import AssetsQueryType
from lib.services.configuration.type.query.crypto_historical_bars import CryptoHistoricalBarsQueryType
from lib.services.configuration.type.query.factory import get_query_type_class
from lib.services.configuration.type.query.stock_historical_bars import StockHistoricalBarsQueryType


def test_known_type_returns_class():
    cls = get_query_type_class('crypto-historical-bars')
    assert cls is CryptoHistoricalBarsQueryType


def test_stock_historical_bars_type_returns_class():
    cls = get_query_type_class('stock-historical-bars')
    assert cls is StockHistoricalBarsQueryType


def test_assets_type_returns_class():
    cls = get_query_type_class('assets')
    assert cls is AssetsQueryType


def test_unknown_type_raises():
    with pytest.raises(KeyError):
        get_query_type_class('unknown-type')
