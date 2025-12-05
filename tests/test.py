import pytest
from httpx import AsyncClient
from src.main import app
from src.config import settings
from unittest.mock import AsyncMock, patch


@pytest.fixture
def valid_headers():
    return {"Authorization": f"Bearer {settings.API_TOKEN}"}

@pytest.fixture
def mock_coin_list():
    return [{"id": "01coin", "symbol": "zoc", "name": "01coin"}, {"id": "bitcoin", "symbol": "btc", "name": "Bitcoin"}]

@pytest.fixture
def mock_market_response_inr():
    return [{"id": "bitcoin", "symbol": "btc", "name": "Bitcoin", "current_price": 5000000, "market_cap": 100000000}]

@pytest.fixture
def mock_market_response_cad():
    return [{"id": "bitcoin", "symbol": "btc", "name": "Bitcoin", "current_price": 80000, "market_cap": 1600000}]


@pytest.mark.asyncio
async def test_health_check_success():
    with patch("src.main.client._get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = {"gecko_says": "(V3) To the Moon!"}
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/health")
    
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_auth_missing():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/coins")
    assert response.status_code == 403 

@pytest.mark.asyncio
async def test_auth_invalid():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/coins", headers={"Authorization": "Bearer wrong"})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_list_coins_pagination(valid_headers, mock_coin_list):
    with patch("src.main.client.get_coin_list", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = mock_coin_list
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # Request 1 item per page
            response = await ac.get("/api/v1/coins?page=1&per_page=1", headers=valid_headers)
            
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 1
        assert data["data"][0]["id"] == "01coin"
        assert data["total_items"] == 2

@pytest.mark.asyncio
async def test_market_data_integration(valid_headers, mock_market_response_inr, mock_market_response_cad):
    
    expected_result = [{
        "id": "bitcoin", 
        "market_data": {
            "inr": {"current_price": 5000000},
            "cad": {"current_price": 80000}
        }
    }]

    with patch("src.main.client.get_market_data", new_callable=AsyncMock) as mock_service:
        mock_service.return_value = expected_result
        
        async with AsyncClient(app=app, base_url="http://test") as ac:
            response = await ac.get("/api/v1/coins/markets?ids=bitcoin", headers=valid_headers)
            
        assert response.status_code == 200
        assert response.json()["data"][0]["market_data"]["inr"]["current_price"] == 5000000