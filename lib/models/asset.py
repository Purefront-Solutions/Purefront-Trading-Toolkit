from typing import Self

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from lib.models.base import BaseModel, CommonMixin


class AssetModel(CommonMixin, BaseModel):
    __abstract__ = True

    asset_class: Mapped[str] = mapped_column(String)
    symbol: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(**data)
