from lib.models.asset import AssetModel


class ConcreteAsset(AssetModel):
    __tablename__ = "test_assets"


def test_from_dict_sets_asset_class():
    obj = ConcreteAsset.from_dict({'asset_class': 'us_equity', 'symbol': 'AAPL', 'status': 'active'})
    assert obj.asset_class == 'us_equity'


def test_from_dict_sets_symbol():
    obj = ConcreteAsset.from_dict({'asset_class': 'crypto', 'symbol': 'BTC/USD', 'status': 'active'})
    assert obj.symbol == 'BTC/USD'


def test_from_dict_sets_status():
    obj = ConcreteAsset.from_dict({'asset_class': 'us_equity', 'symbol': 'AAPL', 'status': 'inactive'})
    assert obj.status == 'inactive'
