#!/bin/bash

# Crypto Market Volume Spike Detector Startup Script

echo "Starting Crypto Market Volume Spike Detector..."
echo "=============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt

# Start the application
echo "Starting Flask application..."
echo "The API will be available at: http://localhost:5000/api/get_signal"
echo "Press Ctrl+C to stop the application"
echo ""

python app.py