#!/bin/bash
# AEM Forms Agent Workflow - Gemini Setup Script

echo "🔧 AEM Forms Agent Workflow - Gemini Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    exit 1
fi

echo "✅ Python 3 found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q flask jinja2 beautifulsoup4 pdfplumber reportlab openai google-generativeai requests

echo "✅ Dependencies installed"
echo ""

# Setup API keys
echo "Setting up LLM API keys..."
python3 -c "
from config import setup_api_keys, ensure_api_key
import sys
setup_api_keys()
ensure_api_key()
print('')
"

if [ $? -ne 0 ]; then
    echo "❌ Failed to setup API keys"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application, run:"
echo "  python3 app.py"
echo ""
echo "Then open: http://localhost:5000"
echo ""
echo "💡 Tip: You can also set LLM provider:"
echo "  export LLM_PROVIDER=gemini    # Use Google Gemini (free)"
echo "  export LLM_PROVIDER=openai    # Use OpenAI (paid)"
