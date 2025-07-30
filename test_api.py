#!/usr/bin/env python3
"""
Simple test script for the Crypto Market Volume Spike Detector API
"""

import requests
import json
import time

def test_api():
    """Test the API endpoint"""
    base_url = "http://localhost:5000"
    endpoint = "/api/get_signal"
    
    print("Testing Crypto Market Volume Spike Detector API")
    print("=" * 50)
    
    try:
        # Test the API endpoint
        response = requests.get(f"{base_url}{endpoint}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API is responding correctly")
            print(f"Response: {json.dumps(data, indent=2)}")
            
            if "status" in data:
                print("\n📊 Status: No volume spikes detected yet")
                print("The application is monitoring BTC/USDT trades...")
                print("Volume spikes will be detected when trade volume is 10x greater than the moving average")
            else:
                print("\n🚨 Volume Spike Detected!")
                print(f"Signal Type: {data.get('signal_type')}")
                print(f"Price: ${data.get('price'):,.2f}")
                print(f"Volume: {data.get('volume'):.2f} BTC")
                print(f"Timestamp: {data.get('timestamp')}")
                
        else:
            print(f"❌ API returned status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API")
        print("Make sure the Flask application is running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    test_api()