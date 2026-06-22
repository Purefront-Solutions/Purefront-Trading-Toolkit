import time
from abc import ABC, abstractmethod
from collections.abc import Generator

import requests

from lib.models.historical_bars import HistoricalBars
from lib.services.configuration.collection import CollectionFrequency
from lib.services.configuration.datasource import DatasourceConfiguration
from lib.services.configuration.type.query.historical_bars import HistoricalBarsQueryType

_TIMEFRAME_MAP: dict[CollectionFrequency, str] = {
    CollectionFrequency.ONE_DAY: '1D',
    CollectionFrequency.ONE_MINUTE: '1M',
}

_MAX_RETRIES: int = 3
_RETRY_BASE_DELAY: float = 1.0


class AlpacaHistoricalBarsService(ABC):
    def __init__(self, datasource_config: DatasourceConfiguration) -> None:
        self._datasource_config = datasource_config

    @property
    @abstractmethod
    def _system_config(self) -> object: ...

    @property
    @abstractmethod
    def _test_symbol(self) -> str: ...

    @abstractmethod
    def convert_to_model(self, data: dict) -> HistoricalBars: ...

    def _fetch_with_retries(self, url: str, params: dict) -> dict:
        last_exc: Exception | None = None
        for attempt in range(_MAX_RETRIES + 1):
            if attempt > 0:
                time.sleep(_RETRY_BASE_DELAY * (2 ** (attempt - 1)))
            try:
                response = requests.get(
                    url,
                    auth=(self._datasource_config.api_key, self._datasource_config.api_secret),
                    headers={"accept": "application/json"},
                    params=params,
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                if e.response is not None and e.response.status_code < 500:
                    raise
                last_exc = e
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
                last_exc = e

        assert last_exc is not None
        raise last_exc

    def fetch_historical_bars(self, query_config: HistoricalBarsQueryType) -> Generator[list[HistoricalBars], None, None]:
        params: dict = {
            "timeframe": _TIMEFRAME_MAP[CollectionFrequency(query_config.frequency)],
            "start": query_config.start.isoformat(),
            "symbols": ",".join(query_config.symbols),
            "limit": self._system_config.page_limit,
        }
        if query_config.end is not None:
            params["end"] = query_config.end.isoformat()

        while True:
            response_data = self._fetch_with_retries(self._system_config.fetch_url, params)
            bars: list[HistoricalBars] = []
            for symbol, bars_data in response_data['bars'].items():
                bars.extend([self.convert_to_model({**bar_data, 'symbol': symbol}) for bar_data in bars_data])
            yield bars
            next_page_token: str | None = response_data.get('next_page_token')
            if not next_page_token:
                break
            params = {**params, 'page_token': next_page_token}

    def test_connection(self) -> bool:
        url = self._system_config.test_url
        print(f"Testing connection to {url} with API key {self._datasource_config.api_key}")
        response = requests.get(
            url,
            auth=(self._datasource_config.api_key, self._datasource_config.api_secret),
            headers={"accept": "application/json"},
            params={"symbols": self._test_symbol, "timeframe": "1D"},
        )
        response.raise_for_status()
        return True
