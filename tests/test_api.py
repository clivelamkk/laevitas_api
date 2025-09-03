import pytest
import pandas as pd
from laevitas_api import get_OptTrades, get_OptSnapshot, get_FutSnapshot, get_lav_implied_vol
from laevitas_api import utilities as ut
from os import environ

@pytest.fixture
def set_api_key():
    environ["api_lav"] = "test_api_key"
    yield
    environ.pop("api_lav", None)

def test_get_OptTrades(set_api_key, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": [{"id": 1, "data": "test"}]}
    mocker.patch("requests.get", return_value=mock_response)
    
    df = get_OptTrades("DERIBIT", "BTC", "2025-01-06")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["id"] == 1

def test_get_OptSnapshot(set_api_key, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": [{"id": 1, "data": "test"}]}
    mocker.patch("requests.get", return_value=mock_response)
    
    df = get_OptSnapshot("DERIBIT", "BTC", "2025-01-06", "2025-01-07", "1h")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["id"] == 1

def test_get_FutSnapshot(set_api_key, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": [{"id": 1, "data": "test"}]}
    mocker.patch("requests.get", return_value=mock_response)
    
    df = get_FutSnapshot("DERIBIT", "BTC", "2025-01-06", "2025-01-07", "1h")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["id"] == 1

def test_get_lav_implied_vol(set_api_key, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"items": [{"date": 1736244000000, "data": "test"}]}
    mocker.patch("requests.get", return_value=mock_response)
    
    result = get_lav_implied_vol("BTC-31DEC25-50000-C", "2025-01-07")
    assert isinstance(result, dict)
    assert result["data"] == "test"