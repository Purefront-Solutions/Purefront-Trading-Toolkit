from collections.abc import Generator

import requests

from lib.models.alpaca.asset import AlpacaAssetModel
from lib.services.configuration.datasource import DatasourceConfiguration
from lib.services.configuration.system import SystemConfigurationService
from lib.services.configuration.type.query.assets import AssetsQueryType


class _LazySystemConfig:
    _instance: object | None = None

    def __getattr__(self, name: str) -> object:
        if type(self)._instance is None:
            type(self)._instance = SystemConfigurationService('datasource_services').get_one('alpaca_assets')
        return getattr(type(self)._instance, name)


config: _LazySystemConfig = _LazySystemConfig()


class AlpacaAssetsService:
    def __init__(self, datasource_config: DatasourceConfiguration) -> None:
        self._datasource_config = datasource_config

    def convert_to_model(self, data: dict) -> AlpacaAssetModel:
        asset_dict = {
            'alpaca_id': data['id'],
            'asset_class': data['class'],
            'symbol': data['symbol'],
            'status': data['status'],
            'cusip': data.get('cusip'),
            'exchange': data.get('exchange'),
            'name': data.get('name'),
            'tradable': data['tradable'],
            'marginable': data['marginable'],
            'shortable': data['shortable'],
            'easy_to_borrow': data.get('borrow_status') == 'easy_to_borrow',
            'fractionable': data['fractionable'],
            'margin_requirement_long': data.get('margin_requirement_long'),
            'margin_requirement_short': data.get('margin_requirement_short'),
            'source': self._datasource_config.type,
        }
        return AlpacaAssetModel.from_dict(asset_dict)

    def fetch_assets(self, query_config: AssetsQueryType) -> Generator[list[AlpacaAssetModel], None, None]:
        params: dict = {}
        if query_config.asset_class is not None:
            params['asset_class'] = query_config.asset_class
        if query_config.symbol is not None:
            params['symbol'] = query_config.symbol
        if query_config.status is not None:
            params['status'] = query_config.status

        response = requests.get(
            config.fetch_url,
            auth=(self._datasource_config.api_key, self._datasource_config.api_secret),
            headers={"accept": "application/json"},
            params=params,
        )
        response.raise_for_status()
        assets = [self.convert_to_model(item) for item in response.json()]
        yield assets

    def test_connection(self) -> bool:
        url = config.test_url
        response = requests.get(
            url,
            auth=(self._datasource_config.api_key, self._datasource_config.api_secret),
            headers={"accept": "application/json"},
        )
        response.raise_for_status()
        return True
