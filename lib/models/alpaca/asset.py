from typing import Optional

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from lib.models.asset import AssetModel


class AlpacaAssetModel(AssetModel):
    __tablename__ = "alpaca_assets"

    alpaca_id: Mapped[str] = mapped_column(String)
    exchange: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tradable: Mapped[bool] = mapped_column(Boolean)
    marginable: Mapped[bool] = mapped_column(Boolean)
    shortable: Mapped[bool] = mapped_column(Boolean)
    easy_to_borrow: Mapped[bool] = mapped_column(Boolean)
    fractionable: Mapped[bool] = mapped_column(Boolean)
    margin_requirement_long: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    margin_requirement_short: Mapped[Optional[str]] = mapped_column(String, nullable=True)
