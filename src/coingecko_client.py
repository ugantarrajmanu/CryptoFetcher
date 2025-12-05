import asyncio
from typing import List, Dict, Optional, Any
from src.config import settings


class CoinGeckoClient:
    def __init__(self):
        self.base_url = settings.COINGECKO_BASE_URL

    # fetch list of coins
    async def get_coin_list(self) -> List[Dict]:
        return await self._get("/coins/list")

    # fetch list of coin categories
    async def get_categories(self) -> List[Dict]:
        return await self._get("/coins/categories/list")

    # fetch market data
    async def get_market_data(self, vs_currencies: List[str], ids: Optional[str], category: Optional[str], page: int, per_page: int) -> List[Dict]:
        # Make requests in parallel
        tasks = []
        for currency in vs_currencies:
            params = {
                "vs_currency": currency,
                "order": "market_cap_desc",
                "per_page": per_page,
                "page": page,
                "sparkline": "false",
                "locale": "en"
            }
            if ids:
                params["ids"] = ids
            if category:
                params["category"] = category
            
            tasks.append(self._get("/coins/markets", params))

        # Run requests in parallel
        results = await asyncio.gather(*tasks)
        
        # Merge results
        merged_data = {}
        
        # Process inr - res[0]
        for coin in results[0]:
            c_id = coin['id']
            merged_data[c_id] = {
                "id": c_id,
                "symbol": coin['symbol'],
                "name": coin['name'],
                "image": coin['image'],
                "market_data": {
                    "inr": {
                        "current_price": coin.get('current_price'),
                        "market_cap": coin.get('market_cap'),
                        "high_24h": coin.get('high_24h'),
                        "low_24h": coin.get('low_24h')
                    }
                }
            }

        # Process cad (results[1])
        for coin in results[1]:
            c_id = coin['id']
            if c_id in merged_data:
                merged_data[c_id]["market_data"]["cad"] = {
                    "current_price": coin.get('current_price'),
                    "market_cap": coin.get('market_cap'),
                    "high_24h": coin.get('high_24h'),
                    "low_24h": coin.get('low_24h')
                }

        return list(merged_data.values())