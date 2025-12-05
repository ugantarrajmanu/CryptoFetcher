import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "CryptoFetcher"
    APP_VERSION: str = "1.0"
    API_TOKEN: str = "secret-token"
    EXTERNAL_TIMEOUT: int = 10

    COINGECKO_BASE_URL: str = "https://api.coingecko.com/api/v3/"

    class Config:
        env_file = ".env"


settings = Settings()