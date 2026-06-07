import pytest

from lib.services.configuration.type.query.assets import AssetsQueryType


def test_name_is_assets():
    assert AssetsQueryType.name == 'assets'


def test_all_fields_default_to_none():
    q = AssetsQueryType()
    assert q.asset_class is None
    assert q.status is None


def test_to_dict_omits_none_fields():
    q = AssetsQueryType()
    assert q.to_dict() == {}


def test_to_dict_includes_asset_class_when_set():
    q = AssetsQueryType(asset_class='us_equity')
    assert q.to_dict() == {'asset_class': 'us_equity'}


def test_to_dict_includes_status_when_set():
    q = AssetsQueryType(status='active')
    assert q.to_dict() == {'status': 'active'}


def test_to_dict_includes_all_set_fields():
    q = AssetsQueryType(asset_class='crypto', status='active')
    assert q.to_dict() == {'asset_class': 'crypto', 'status': 'active'}
