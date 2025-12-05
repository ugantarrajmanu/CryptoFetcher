# Crypto Market Fetcher API
A robust HTTP REST API built with FastAPI to fetch cryptocurrency market updates. This application integrates with the CoinGecko API to provide coin listings, categories, and specific market data aggregated in INR (Indian Rupee) and CAD (Canadian Dollar).

# Features
- List Coins: Fetch a paginated list of all supported coins (ID, symbol, name).

- Categories: Retrieve all coin categories.

- Market Data: Get detailed market data for specific coins, automatically aggregated for both INR and CAD currencies in a single response.

- Authentication: Secure endpoints using a Bearer API Token / JWT-based mechanism.

- Documentation: Automatic interactive API docs (Swagger UI & ReDoc).

- Dockerized: Fully containerized for easy deployment.

- Quality Assurance: Includes unit tests (pytest), coverage reporting, and linting (Ruff).

# Project Structure
```
.
├── Dockerfile           # Docker configuration
├── README.md            # Project documentation
├── pyproject.toml       # Linting (Ruff) and Test configuration
├── requirements.txt     # Python dependencies
├── src
│   ├── __init__.py
│   ├── auth.py          # Authentication logic (Bearer Token)
│   ├── coingecko_client.py # Service for CoinGecko API interaction
│   ├── config.py        # Environment configuration (Pydantic)
│   └── main.py          # App entry point and route definitions
└── tests
    ├── __init__.py
    └── test_app.py      # Unit tests with mocking
```

# Getting Started

## Prerequisites

- Python 3.9+
- Docker

## Local Installation
1. Clone the repository:
```Bash
git clone https://github.com/ugantarrajmanu/CryptoFetcher
cd crypto-fetcher
```

2. Create and activate a virtual environment:
```Bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```Bash
pip install -r requirements.txt
```

4. Run the application:
```Bash
# The default API_TOKEN is "secret-token". 
# You can override this via environment variables.
uvicorn src.main:app --reload
```

# Authentication

All ```/api/v1/``` endpoints are protected. You must provide the ```Authorization``` header in your requests.

## Header Format:
```
Authorization: Bearer secret-token
```

_(Replace secret-token with the value defined in src/config.py or your .env file)_

# Docker Deployment
1. **Build the Docker image:**
```Bash
docker build -t crypto-fetcher .
```

2. **Run the container:**
```Bash
docker run -d -p 8000:8000 --name crypto-app -e API_TOKEN=my-prod-secret crypto-fetcher
```

3. **Verify Health**: Visit ```http://localhost:8000/health```


# API Endpoints

**Public**

- GET /health: Checks application status and upstream connectivity.

**Protected (Requires Token)**
- ```GET /api/v1/coins```: List all coins.
    - Query Params: ```page``` (default 1), ```per_page``` (default 10).

- ```GET /api/v1/categories```: List all coin categories.

- ```GET /api/v1/coins/markets```: Get market data in INR and CAD.

- Query Params: ```ids``` (comma-separated, e.g., ```bitcoin```,```ethereum```), ```category```, ```page```, ```per_page```.


# Running Tests

This project uses pytest with pytest-cov for test coverage.

```Bash
pytest --cov=src tests/
```

# Configuration

Configuration is managed via ```src/config.py``` using Pydantic. You can override settings using environment variables or a ```.env``` file.

| Variable | Default | Description |
| :--- | :--- | :--- |
| `API_TOKEN` | `secret-token` | The secret token required for Bearer auth. |
| `EXTERNAL_TIMEOUT` | `10` | Timeout in seconds for CoinGecko API calls. |
| `APP_NAME` | `Crypto Market Fetcher` | Name of the application. |
