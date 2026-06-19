from collections.abc import Generator

from lib.adapters.interfaces.datasource_adapter_interface import DatasourceAdapterInterface
from lib.models.alpaca.asset import AlpacaAssetModel
from lib.models.alpaca.alpaca_crypto_historical_bar import AlpacaCryptoHistoricalBar
from lib.models.alpaca.alpaca_stock_historical_bar import AlpacaStockHistoricalBar
from lib.models.base import BaseModel
from lib.services.configuration.datasource import DatasourceConfiguration
from lib.services.configuration.query import QueryConfiguration
from lib.services.configuration.type.query.assets import AssetsQueryType
from lib.services.configuration.type.query.crypto_historical_bars import CryptoHistoricalBarsQueryType
from lib.services.configuration.type.query.stock_historical_bars import StockHistoricalBarsQueryType
from lib.services.datasources.alpaca.alpaca_assets_service import AlpacaAssetsService
from lib.services.datasources.alpaca.alpaca_crypto_service import AlpacaCryptoService
from lib.services.datasources.alpaca.alpaca_stock_service import AlpacaStockService


class AlpacaDatasourceAdapter(DatasourceAdapterInterface):
    def __init__(self, config: DatasourceConfiguration) -> None:
        self._config = config
        self._service = AlpacaCryptoService(config)
        self._stock_service = AlpacaStockService(config)
        self._assets_service = AlpacaAssetsService(config)

    def get_model(self, query_config: QueryConfiguration) -> type[BaseModel]:
        if query_config.type == 'crypto-historical-bars':
            return AlpacaCryptoHistoricalBar
        if query_config.type == 'stock-historical-bars':
            return AlpacaStockHistoricalBar
        if query_config.type == 'assets':
            return AlpacaAssetModel
        raise ValueError(f"Unsupported query type: {query_config.type}")

    def run_query(self, query_config: QueryConfiguration) -> Generator[list[BaseModel], None, None]:
        if query_config.type == 'crypto-historical-bars':
            fields = {k: v for k, v in query_config.to_dict().items() if k not in ('name', 'type')}
            return self._service.fetch_historical_bars(CryptoHistoricalBarsQueryType(**fields))
        if query_config.type == 'stock-historical-bars':
            fields = {k: v for k, v in query_config.to_dict().items() if k not in ('name', 'type')}
            return self._stock_service.fetch_historical_bars(StockHistoricalBarsQueryType(**fields))
        if query_config.type == 'assets':
            fields = {k: v for k, v in query_config.to_dict().items() if k not in ('name', 'type')}
            return self._assets_service.fetch_assets(AssetsQueryType(**fields))
        raise ValueError(f"Unsupported query type: {query_config.type}")

    def test_connection(self) -> bool:
        return self._service.test_connection()
