from lib.models.alpaca.alpaca_crypto_historical_bar import AlpacaCryptoHistoricalBar
from lib.services.configuration.system import SystemConfigurationService
from lib.services.datasources.alpaca.alpaca_historical_bars_service import AlpacaHistoricalBarsService


class _LazySystemConfig:
    _instance: object | None = None

    def __getattr__(self, name: str) -> object:
        if type(self)._instance is None:
            type(self)._instance = SystemConfigurationService('datasource_services').get_one('alpaca_crypto')
        return getattr(type(self)._instance, name)


config: _LazySystemConfig = _LazySystemConfig()


class AlpacaCryptoService(AlpacaHistoricalBarsService):
    @property
    def _system_config(self) -> object:
        return config

    @property
    def _test_symbol(self) -> str:
        return 'BTC/USD'

    def convert_to_model(self, data: dict) -> AlpacaCryptoHistoricalBar:
        bar_dict = {
            'symbol': data['symbol'],
            'time': data['t'],
            'open': data['o'],
            'high': data['h'],
            'low': data['l'],
            'close': data['c'],
            'volume': data['v'],
            'trade_count': data['n'],
            'volume_weighted_avg_price': data['vw'],
            'source': self._datasource_config.type
        }
        return AlpacaCryptoHistoricalBar.from_dict(bar_dict)
