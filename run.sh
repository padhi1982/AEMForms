#!/bin/bash

# AEM Forms Agent Workflow - Startup Script
# This script sets up and runs the web interface locally

echo "🚀 AEM Forms Agent Workflow - Startup"
echo "======================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "\n📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Create necessary directories
mkdir -p uploads outputs

echo "\n✅ Setup complete!"
echo ""
echo "🌐 Starting web server..."
echo "📱 Open your browser and navigate to: http://localhost:5000"
echo ""
echo "To stop the server, press Ctrl+C"
echo ""

# Run the Flask app
python3 app.py
