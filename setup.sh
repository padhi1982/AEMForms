#!/bin/bash
# AEM Forms Agent Workflow - Setup Script

echo "🔧 AEM Forms Agent Workflow Setup"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment (optional)
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q flask jinja2 beautifulsoup4 pdfplumber reportlab openai requests

echo "✅ Dependencies installed"
echo ""

# Setup OpenAI API key
python3 -c "
from config import setup_openai_key, validate_openai_key
import sys
setup_openai_key()
if not validate_openai_key():
    sys.exit(1)
"

if [ $? -ne 0 ]; then
    echo "❌ Failed to setup OpenAI API key"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application, run:"
echo "  python3 app.py"
echo ""
echo "Then open: http://localhost:5000"
