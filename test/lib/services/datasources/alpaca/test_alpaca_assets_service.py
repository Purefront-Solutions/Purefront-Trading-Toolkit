from unittest.mock import MagicMock, patch

import pytest
import requests

from lib.models.alpaca.asset import AlpacaAssetModel
from lib.services.configuration.datasource import DatasourceConfiguration
from lib.services.configuration.type.query.assets import AssetsQueryType
from lib.services.datasources.alpaca.alpaca_assets_service import AlpacaAssetsService

_MOCK_SYS_CONFIG = MagicMock()
_MOCK_SYS_CONFIG.fetch_url = "http://localhost:8000/alpaca/v2/assets"
_MOCK_SYS_CONFIG.test_url = "http://localhost:8000/alpaca/v2/assets"


def _make_config(**overrides) -> DatasourceConfiguration:
    defaults = dict(
        name="test-ds", type="alpaca", api_key="key123", api_secret="secret456",
    )
    defaults.update(overrides)
    return DatasourceConfiguration(**defaults)


def _make_asset_data(**overrides) -> dict:
    defaults = dict(
        id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        **{"class": "us_equity"},
        cusip="987654321",
        exchange="NYSE",
        symbol="AAPL",
        name="Apple Inc.",
        status="active",
        tradable=True,
        marginable=True,
        shortable=True,
        borrow_status="easy_to_borrow",
        fractionable=True,
        margin_requirement_long="100%",
        margin_requirement_short="150%",
    )
    defaults.update(overrides)
    return defaults


# --- convert_to_model ---

def test_convert_to_model_returns_alpaca_asset_model():
    service = AlpacaAssetsService(_make_config())
    result = service.convert_to_model(_make_asset_data())
    assert isinstance(result, AlpacaAssetModel)


def test_convert_to_model_maps_class_to_asset_class():
    service = AlpacaAssetsService(_make_config())
    result = service.convert_to_model(_make_asset_data(**{"class": "crypto"}))
    assert result.asset_class == "crypto"


def test_convert_to_model_maps_symbol():
    service = AlpacaAssetsService(_make_config())
    result = service.convert_to_model(_make_asset_data(symbol="TSLA"))
    assert result.symbol == "TSLA"


def test_convert_to_model_maps_status():
    service = AlpacaAssetsService(_make_config())
    result = service.convert_to_model(_make_asset_data(status="inactive"))
    assert result.status == "inactive"


def test_convert_to_model_maps_boolean_fields():
    service = AlpacaAssetsService(_make_config())
    result = service.convert_to_model(_make_asset_data(tradable=False, marginable=False))
    assert result.tradable is False
    assert result.marginable is False


def test_convert_to_model_easy_to_borrow_true_when_borrow_status_is_easy_to_borrow():
    service = AlpacaAssetsService(_make_config())
    result = service.convert_to_model(_make_asset_data(borrow_status="easy_to_borrow"))
    assert result.easy_to_borrow is True


def test_convert_to_model_easy_to_borrow_false_when_borrow_status_is_not_easy_to_borrow():
    service = AlpacaAssetsService(_make_config())
    result = service.convert_to_model(_make_asset_data(borrow_status="hard_to_borrow"))
    assert result.easy_to_borrow is False


def test_convert_to_model_easy_to_borrow_false_when_borrow_status_absent():
    service = AlpacaAssetsService(_make_config())
    data = _make_asset_data()
    data.pop("borrow_status", None)
    result = service.convert_to_model(data)
    assert result.easy_to_borrow is False


def test_convert_to_model_maps_optional_cusip():
    service = AlpacaAssetsService(_make_config())
    result = service.convert_to_model(_make_asset_data(cusip="123456789"))
    assert result.cusip == "123456789"


def test_convert_to_model_sets_none_for_missing_optional_fields():
    service = AlpacaAssetsService(_make_config())
    data = _make_asset_data()
    data.pop("cusip", None)
    data.pop("exchange", None)
    result = service.convert_to_model(data)
    assert result.cusip is None
    assert result.exchange is None


def test_convert_to_model_sets_source_from_config_type():
    service = AlpacaAssetsService(_make_config(type="alpaca"))
    result = service.convert_to_model(_make_asset_data())
    assert result.source == "alpaca"


# --- fetch_assets ---

def test_fetch_assets_yields_single_batch():
    service = AlpacaAssetsService(_make_config())
    mock_response = MagicMock()
    mock_response.json.return_value = [_make_asset_data(), _make_asset_data(symbol="TSLA")]
    with patch("lib.services.datasources.alpaca.alpaca_assets_service.config", _MOCK_SYS_CONFIG):
        with patch("lib.services.datasources.alpaca.alpaca_assets_service.requests.get", return_value=mock_response):
            pages = list(service.fetch_assets(AssetsQueryType()))
    assert len(pages) == 1
    assert len(pages[0]) == 2
    assert all(isinstance(a, AlpacaAssetModel) for a in pages[0])


def test_fetch_assets_omits_params_when_not_set():
    service = AlpacaAssetsService(_make_config())
    mock_response = MagicMock()
    mock_response.json.return_value = []
    with patch("lib.services.datasources.alpaca.alpaca_assets_service.config", _MOCK_SYS_CONFIG):
        with patch("lib.services.datasources.alpaca.alpaca_assets_service.requests.get", return_value=mock_response) as mock_get:
            list(service.fetch_assets(AssetsQueryType()))
    params = mock_get.call_args[1]["params"]
    assert params == {}


def test_fetch_assets_passes_asset_class_param():
    service = AlpacaAssetsService(_make_config())
    mock_response = MagicMock()
    mock_response.json.return_value = []
    with patch("lib.services.datasources.alpaca.alpaca_assets_service.config", _MOCK_SYS_CONFIG):
        with patch("lib.services.datasources.alpaca.alpaca_assets_service.requests.get", return_value=mock_response) as mock_get:
            list(service.fetch_assets(AssetsQueryType(asset_class="us_equity")))
    params = mock_get.call_args[1]["params"]
    assert params["asset_class"] == "us_equity"


def test_fetch_assets_passes_status_param():
    service = AlpacaAssetsService(_make_config())
    mock_response = MagicMock()
    mock_response.json.return_value = []
    with patch("lib.services.datasources.alpaca.alpaca_assets_service.config", _MOCK_SYS_CONFIG):
        with patch("lib.services.datasources.alpaca.alpaca_assets_service.requests.get", return_value=mock_response) as mock_get:
            list(service.fetch_assets(AssetsQueryType(status="active")))
    params = mock_get.call_args[1]["params"]
    assert params["status"] == "active"


def test_fetch_assets_uses_api_key_and_secret_as_auth():
    service = AlpacaAssetsService(_make_config(api_key="mykey", api_secret="mysecret"))
    mock_response = MagicMock()
    mock_response.json.return_value = []
    with patch("lib.services.datasources.alpaca.alpaca_assets_service.config", _MOCK_SYS_CONFIG):
        with patch("lib.services.datasources.alpaca.alpaca_assets_service.requests.get", return_value=mock_response) as mock_get:
            list(service.fetch_assets(AssetsQueryType()))
    assert mock_get.call_args[1]["auth"] == ("mykey", "mysecret")


def test_fetch_assets_calls_raise_for_status():
    service = AlpacaAssetsService(_make_config())
    mock_response = MagicMock()
    mock_response.json.return_value = []
    with patch("lib.services.datasources.alpaca.alpaca_assets_service.config", _MOCK_SYS_CONFIG):
        with patch("lib.services.datasources.alpaca.alpaca_assets_service.requests.get", return_value=mock_response):
            list(service.fetch_assets(AssetsQueryType()))
    mock_response.raise_for_status.assert_called_once()


# --- test_connection ---

def test_test_connection_returns_true_on_success():
    service = AlpacaAssetsService(_make_config())
    with patch("lib.services.datasources.alpaca.alpaca_assets_service.config", _MOCK_SYS_CONFIG):
        with patch("lib.services.datasources.alpaca.alpaca_assets_service.requests.get", return_value=MagicMock()):
            result = service.test_connection()
    assert result is True


def test_test_connection_calls_raise_for_status():
    service = AlpacaAssetsService(_make_config())
    mock_response = MagicMock()
    with patch("lib.services.datasources.alpaca.alpaca_assets_service.config", _MOCK_SYS_CONFIG):
        with patch("lib.services.datasources.alpaca.alpaca_assets_service.requests.get", return_value=mock_response):
            service.test_connection()
    mock_response.raise_for_status.assert_called_once()


def test_test_connection_uses_correct_url():
    service = AlpacaAssetsService(_make_config())
    mock_sys_config = MagicMock()
    mock_sys_config.test_url = "https://paper-api.alpaca.markets/v2/assets"
    with patch("lib.services.datasources.alpaca.alpaca_assets_service.config", mock_sys_config):
        with patch("lib.services.datasources.alpaca.alpaca_assets_service.requests.get") as mock_get:
            mock_get.return_value = MagicMock()
            service.test_connection()
    assert mock_get.call_args[0][0] == "https://paper-api.alpaca.markets/v2/assets"


def test_test_connection_uses_api_key_and_secret_as_auth():
    service = AlpacaAssetsService(_make_config(api_key="mykey", api_secret="mysecret"))
    with patch("lib.services.datasources.alpaca.alpaca_assets_service.config", _MOCK_SYS_CONFIG):
        with patch("lib.services.datasources.alpaca.alpaca_assets_service.requests.get") as mock_get:
            mock_get.return_value = MagicMock()
            service.test_connection()
    assert mock_get.call_args[1]["auth"] == ("mykey", "mysecret")


def test_test_connection_propagates_http_error():
    service = AlpacaAssetsService(_make_config())
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("401 Unauthorized")
    with patch("lib.services.datasources.alpaca.alpaca_assets_service.config", _MOCK_SYS_CONFIG):
        with patch("lib.services.datasources.alpaca.alpaca_assets_service.requests.get", return_value=mock_response):
            with pytest.raises(Exception, match="401 Unauthorized"):
                service.test_connection()
