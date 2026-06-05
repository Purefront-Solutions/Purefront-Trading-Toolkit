from dataclasses import dataclass
from typing import ClassVar

from lib.services.configuration.interface.query_interface import QueryInterface


@dataclass
class AssetsQueryType(QueryInterface):
    name: ClassVar[str] = 'assets'
    asset_class: str | None = None
    symbol: str | None = None
    status: str | None = None

    def to_dict(self) -> dict:
        d: dict = {}
        if self.asset_class is not None:
            d['asset_class'] = self.asset_class
        if self.symbol is not None:
            d['symbol'] = self.symbol
        if self.status is not None:
            d['status'] = self.status
        return d
