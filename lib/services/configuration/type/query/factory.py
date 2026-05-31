from lib.services.configuration.type.query.crypto_historical_bars import CryptoHistoricalBarsQueryType

_REGISTRY: dict[str, type] = {
    CryptoHistoricalBarsQueryType.name: CryptoHistoricalBarsQueryType,
}


def get_query_type_class(name: str) -> type:
    if name not in _REGISTRY:
        raise KeyError(f"Unknown query type: {name!r}")
    return _REGISTRY[name]
