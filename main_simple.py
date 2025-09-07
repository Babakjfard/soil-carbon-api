from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import os

# Initialize FastAPI app
app = FastAPI(
    title="Soil Carbon API",
    description="API for querying soil organic carbon data from OSSL dataset",
    version="1.0.0"
)

# Pydantic models for request/response
class SoilCarbonRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")
    max_distance_km: Optional[float] = Field(10.0, ge=0.1, le=1000, description="Maximum search distance in kilometers")

class SoilCarbonResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {
        "message": "Welcome to the Soil Carbon API",
        "description": "Query soil organic carbon data from OSSL dataset",
        "status": "running",
        "endpoints": {
            "GET /": "This welcome message",
            "POST /soil_carbon": "Query soil carbon data by coordinates",
            "GET /docs": "Interactive API documentation",
            "GET /redoc": "Alternative API documentation",
            "GET /health": "Health check endpoint"
        }
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for deployment platforms.
    """
    return {
        "status": "healthy",
        "message": "API is running",
        "service": "soil-carbon-api"
    }

@app.post("/soil_carbon", response_model=SoilCarbonResponse)
async def get_soil_carbon(request: SoilCarbonRequest):
    """
    Query soil organic carbon data for given coordinates.
    This is a simplified version that returns mock data for testing.
    """
    try:
        # Validate coordinates
        if not (-90 <= request.latitude <= 90):
            raise HTTPException(
                status_code=400, 
                detail="Latitude must be between -90 and 90 degrees"
            )
        
        if not (-180 <= request.longitude <= 180):
            raise HTTPException(
                status_code=400, 
                detail="Longitude must be between -180 and 180 degrees"
            )
        
        # For now, return mock data to test the API structure
        # We'll add the real soil carbon functionality after deployment works
        mock_data = {
            "carbon_pct": 2.5,
            "sample_id": "mock_12345",
            "distance_meters": 1500.0,
            "latitude": request.latitude + 0.01,  # Slightly offset
            "longitude": request.longitude + 0.01,
            "note": "This is mock data. Real soil carbon functionality will be added after deployment."
        }
        
        return SoilCarbonResponse(
            success=True,
            message="Mock soil carbon data returned successfully",
            data=mock_data
        )
            
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
