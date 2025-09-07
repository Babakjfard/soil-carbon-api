from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
from soilspecdata.datasets.ossl import get_ossl

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

def find_soil_carbon_optimized(lat, lon, max_distance_km=10):
    """
    Optimized function to find soil carbon data near given coordinates.
    
    Args:
        lat (float): Latitude in decimal degrees
        lon (float): Longitude in decimal degrees
        max_distance_km (float): Maximum search distance in kilometers
        
    Returns:
        dict or str: Dictionary with carbon data or error message
    """
    try:
        # Load OSSL dataset
        ossl = get_ossl()
        
        # Get properties with coords and organic carbon
        props = ossl.get_properties([
            'latitude.point_wgs84_dd',
            'longitude.point_wgs84_dd',
            'oc_iso.10694_w.pct',
            'oc_usda.c1059_w.pct',
            'oc_usda.c729_w.pct'
        ], require_complete=False)
        
        props = props.dropna(subset=['latitude.point_wgs84_dd', 'longitude.point_wgs84_dd'])
        
        # Create GeoDataFrame
        gdf = gpd.GeoDataFrame(
            props,
            geometry=gpd.points_from_xy(props['longitude.point_wgs84_dd'], props['latitude.point_wgs84_dd']),
            crs='EPSG:4326'
        )
        
        # Create input point geometry
        input_point = Point(lon, lat)
        input_gdf = gpd.GeoDataFrame(geometry=[input_point], crs='EPSG:4326')
        
        # Use spatial index to find candidates within approximate bounding box around input_point
        # Convert max distance km to degrees roughly (1 deg latitude ~111 km)
        buffer_deg = max_distance_km / 111.0
        bbox = input_point.buffer(buffer_deg).bounds  # (minx, miny, maxx, maxy)
        
        # Spatial index query
        sindex = gdf.sindex
        possible_matches_index = list(sindex.intersection(bbox))
        possible_matches = gdf.iloc[possible_matches_index]
        
        if possible_matches.empty:
            return f"No Data in {max_distance_km} km radius"
        
        # Calculate exact distances in meters by projecting both to EPSG:3857
        possible_matches_proj = possible_matches.to_crs(epsg=3857)
        input_gdf_proj = input_gdf.to_crs(epsg=3857)
        
        possible_matches_proj['distance_m'] = possible_matches_proj.geometry.distance(input_gdf_proj.iloc[0].geometry)
        
        nearby = possible_matches_proj[possible_matches_proj['distance_m'] <= max_distance_km * 1000]
        
        if nearby.empty:
            return f"No Data in {max_distance_km} km radius"

        # Get nearest sample
        nearest = nearby.sort_values('distance_m').iloc[0]
        
        # Find first available carbon value
        for var in ['oc_iso.10694_w.pct', 'oc_usda.c1059_w.pct', 'oc_usda.c729_w.pct']:
            val = nearest.get(var)
            if pd.notnull(val):
                carbon_val = val
                break
        else:
            return f"No organic carbon data available within {max_distance_km} km"
        
        return {
            'carbon_pct': carbon_val,
            'sample_id': nearest.name,
            'distance_meters': nearest['distance_m'],
            'latitude': nearest['latitude.point_wgs84_dd'],
            'longitude': nearest['longitude.point_wgs84_dd'],
        }
        
    except Exception as e:
        raise Exception(f"Error processing soil carbon data: {str(e)}")

@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {
        "message": "Welcome to the Soil Carbon API",
        "description": "Query soil organic carbon data from OSSL dataset",
        "endpoints": {
            "GET /": "This welcome message",
            "POST /soil_carbon": "Query soil carbon data by coordinates",
            "GET /docs": "Interactive API documentation",
            "GET /redoc": "Alternative API documentation"
        }
    }

@app.post("/soil_carbon", response_model=SoilCarbonResponse)
async def get_soil_carbon(request: SoilCarbonRequest):
    """
    Query soil organic carbon data for given coordinates.
    
    Args:
        request (SoilCarbonRequest): Request containing latitude, longitude, and optional max_distance_km
        
    Returns:
        SoilCarbonResponse: Response containing carbon data or error message
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
        
        # Call the optimized function
        result = find_soil_carbon_optimized(
            lat=request.latitude,
            lon=request.longitude,
            max_distance_km=request.max_distance_km
        )
        
        # Check if result is an error message (string) or data (dict)
        if isinstance(result, str):
            return SoilCarbonResponse(
                success=False,
                message=result,
                data=None
            )
        else:
            return SoilCarbonResponse(
                success=True,
                message="Soil carbon data found successfully",
                data=result
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
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
