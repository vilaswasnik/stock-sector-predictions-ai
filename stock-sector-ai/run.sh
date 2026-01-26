#!/bin/bash

echo "======================================"
echo "AI Stock Sector Prediction App"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "======================================"
echo "Starting Flask API Server..."
echo "======================================"
echo ""

# Start the API server
cd api
python app.py
