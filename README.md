# Soil Carbon API

[![CI](https://github.com/yourusername/soil-carbon-api/workflows/CI/badge.svg)](https://github.com/yourusername/soil-carbon-api/actions)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A FastAPI-based REST API for querying soil organic carbon data from the OSSL (Open Soil Spectral Library) dataset.

## Features

- **POST /soil_carbon**: Query soil carbon data by coordinates
- **GET /**: Welcome message and API information
- **GET /docs**: Interactive API documentation (Swagger UI)
- **GET /redoc**: Alternative API documentation (ReDoc)

## Setup

### 1. Create and activate virtual environment

```bash
# Navigate to the project directory
cd fastapi_soil_api

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Usage

### POST /soil_carbon

Query soil organic carbon data for given coordinates.

**Request Body:**
```json
{
  "latitude": 42.3601,
  "longitude": -71.0589,
  "max_distance_km": 10.0
}
```

**Parameters:**
- `latitude` (float, required): Latitude in decimal degrees (-90 to 90)
- `longitude` (float, required): Longitude in decimal degrees (-180 to 180)
- `max_distance_km` (float, optional): Maximum search distance in kilometers (default: 10.0, range: 0.1 to 1000)

**Response:**
```json
{
  "success": true,
  "message": "Soil carbon data found successfully",
  "data": {
    "carbon_pct": 2.5,
    "sample_id": "12345",
    "distance_meters": 1500.5,
    "latitude": 42.3650,
    "longitude": -71.0550
  }
}
```

## Testing the API

### Using curl

```bash
# Test the root endpoint
curl -X GET "http://localhost:8000/"

# Test the soil carbon endpoint
curl -X POST "http://localhost:8000/soil_carbon" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 42.3601,
    "longitude": -71.0589,
    "max_distance_km": 10.0
  }'
```

### Using HTTPie

```bash
# Install HTTPie if not already installed
pip install httpie

# Test the root endpoint
http GET localhost:8000/

# Test the soil carbon endpoint
http POST localhost:8000/soil_carbon \
  latitude=42.3601 \
  longitude=-71.0589 \
  max_distance_km=10.0
```

### Using Python requests

```python
import requests

# Test the root endpoint
response = requests.get("http://localhost:8000/")
print(response.json())

# Test the soil carbon endpoint
data = {
    "latitude": 42.3601,
    "longitude": -71.0589,
    "max_distance_km": 10.0
}
response = requests.post("http://localhost:8000/soil_carbon", json=data)
print(response.json())
```

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input parameters (e.g., latitude/longitude out of range)
- **500 Internal Server Error**: Unexpected server errors
- **Custom error messages**: Clear feedback for no data found scenarios

## Data Source

This API uses the OSSL (Open Soil Spectral Library) dataset through the `soilspecdata` Python package. The data includes soil organic carbon measurements from various sources and locations worldwide.

## Dependencies

- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications
- **GeoPandas**: Geospatial data processing
- **Shapely**: Geometric operations
- **NumPy**: Numerical computing (compatible with Python 3.11)
- **Pandas**: Data manipulation
- **Pydantic**: Data validation
- **soilspecdata**: OSSL dataset access (version 0.0.9)

## Python Compatibility

This project is compatible with Python 3.9+. The `requirements.txt` file has been updated to use compatible versions of all dependencies.

## Docker Support

### Using Docker Compose (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d --build

# Stop the service
docker-compose down
```

### Using Docker directly

```bash
# Build the image
docker build -t soil-carbon-api .

# Run the container
docker run -p 8000:8000 soil-carbon-api
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OSSL (Open Soil Spectral Library)](https://www.soilspectroscopy.org/) for providing the soil data
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [soilspecdata](https://pypi.org/project/soilspecdata/) for Python package access to OSSL data
