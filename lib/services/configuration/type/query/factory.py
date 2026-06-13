from lib.services.configuration.type.query.assets import AssetsQueryType
from lib.services.configuration.type.query.crypto_historical_bars import CryptoHistoricalBarsQueryType
from lib.services.configuration.type.query.stock_historical_bars import StockHistoricalBarsQueryType

_REGISTRY: dict[str, type] = {
    CryptoHistoricalBarsQueryType.name: CryptoHistoricalBarsQueryType,
    StockHistoricalBarsQueryType.name: StockHistoricalBarsQueryType,
    AssetsQueryType.name: AssetsQueryType,
}


def get_query_type_class(name: str) -> type:
    if name not in _REGISTRY:
        raise KeyError(f"Unknown query type: {name!r}")
    return _REGISTRY[name]
