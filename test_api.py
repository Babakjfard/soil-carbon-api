#!/usr/bin/env python3
"""
Test script for the Soil Carbon API
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        response.raise_for_status()
        print("✅ Root endpoint working")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")

def test_soil_carbon_endpoint():
    """Test the soil carbon endpoint with sample data"""
    print("\nTesting soil carbon endpoint...")
    
    # Test cases
    test_cases = [
        {
            "name": "Boston, MA",
            "data": {
                "latitude": 42.3601,
                "longitude": -71.0589,
                "max_distance_km": 10.0
            }
        },
        {
            "name": "San Francisco, CA",
            "data": {
                "latitude": 37.7749,
                "longitude": -122.4194,
                "max_distance_km": 5.0
            }
        },
        {
            "name": "Invalid coordinates (should fail)",
            "data": {
                "latitude": 200.0,  # Invalid latitude
                "longitude": -71.0589,
                "max_distance_km": 10.0
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n--- Testing: {test_case['name']} ---")
        try:
            response = requests.post(
                f"{BASE_URL}/soil_carbon",
                json=test_case['data'],
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Request successful")
                print(f"Success: {result['success']}")
                print(f"Message: {result['message']}")
                if result['data']:
                    print(f"Carbon %: {result['data'].get('carbon_pct', 'N/A')}")
                    print(f"Distance: {result['data'].get('distance_meters', 'N/A')} meters")
            else:
                print(f"❌ Request failed with status {response.status_code}")
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed with exception: {e}")

def main():
    """Main test function"""
    print("Soil Carbon API Test Script")
    print("=" * 40)
    
    # Wait a moment for the server to be ready
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    # Test endpoints
    test_root_endpoint()
    test_soil_carbon_endpoint()
    
    print("\n" + "=" * 40)
    print("Test completed!")

if __name__ == "__main__":
    main()
