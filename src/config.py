import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "CryptoFetcher"
    APP_VERSION: str = "1.0"

    COINGECKO_BASE_URL: str = "https://api.coingecko.com/api/v3/"

    class Config:
        env_file = ".env"


settings = Settings()