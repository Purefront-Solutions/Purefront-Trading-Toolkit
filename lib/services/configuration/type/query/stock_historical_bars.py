from dataclasses import dataclass
from typing import ClassVar

from lib.services.configuration.type.query.historical_bars import HistoricalBarsQueryType


@dataclass
class StockHistoricalBarsQueryType(HistoricalBarsQueryType):
    name: ClassVar[str] = 'stock-historical-bars'
