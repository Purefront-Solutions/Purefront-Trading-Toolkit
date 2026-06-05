from lib.models.alpaca.asset import AlpacaAssetModel


def _make_asset(**overrides) -> AlpacaAssetModel:
    defaults = dict(
        asset_class='us_equity',
        symbol='AAPL',
        status='active',
        tradable=True,
        marginable=True,
        shortable=True,
        easy_to_borrow=True,
        fractionable=True,
    )
    defaults.update(overrides)
    return AlpacaAssetModel.from_dict(defaults)


def test_tablename():
    assert AlpacaAssetModel.__tablename__ == 'alpaca_assets'


def test_from_dict_sets_symbol():
    obj = _make_asset(symbol='TSLA')
    assert obj.symbol == 'TSLA'


def test_from_dict_sets_asset_class():
    obj = _make_asset(asset_class='crypto')
    assert obj.asset_class == 'crypto'


def test_from_dict_sets_status():
    obj = _make_asset(status='inactive')
    assert obj.status == 'inactive'


def test_from_dict_sets_tradable():
    obj = _make_asset(tradable=False)
    assert obj.tradable is False


def test_from_dict_sets_optional_cusip():
    obj = _make_asset(cusip='123456789')
    assert obj.cusip == '123456789'


def test_from_dict_optional_cusip_defaults_none():
    obj = _make_asset()
    assert obj.cusip is None


def test_from_dict_sets_exchange():
    obj = _make_asset(exchange='NYSE')
    assert obj.exchange == 'NYSE'


def test_from_dict_sets_margin_requirement_long():
    obj = _make_asset(margin_requirement_long='100%')
    assert obj.margin_requirement_long == '100%'
