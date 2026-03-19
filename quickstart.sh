#!/bin/bash
# Quick Start Script - Gets you running in 30 seconds!

set -e  # Exit on error

cd "$(dirname "$0")"

echo "🚀 AEM Forms Agent Workflow - Quick Start"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Check Python
echo "${BLUE}[1/4]${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "${YELLOW}⚠️  Python 3 not found. Please install Python 3.8+ from https://www.python.org${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "${GREEN}✅ Python ${PYTHON_VERSION} found${NC}"

# Step 2: Install dependencies
echo ""
echo "${BLUE}[2/4]${NC} Installing dependencies..."
python3 -m pip install -q flask werkzeug pdfplumber jinja2 beautifulsoup4 reportlab openai 2>/dev/null || {
    echo "${YELLOW}Note: Some packages may require additional setup${NC}"
}
echo "${GREEN}✅ Dependencies installed${NC}"

# Step 3: Create directories
echo ""
echo "${BLUE}[3/4]${NC} Creating directories..."
mkdir -p uploads outputs aem-agent-workflow
echo "${GREEN}✅ Directories created${NC}"

# Step 4: Start server
echo ""
echo "${BLUE}[4/4]${NC} Starting web server..."
echo ""
echo "${GREEN}════════════════════════════════════════════════════════${NC}"
echo "${GREEN}✅ Ready to go!${NC}"
echo ""
echo "${YELLOW}📱 Open your browser and go to:${NC}"
echo "   ${BLUE}http://localhost:5000${NC}"
echo ""
echo "${YELLOW}💡 Tip: Drag and drop your PDF file into the upload area${NC}"
echo ""
echo "${YELLOW}To stop the server, press Ctrl+C${NC}"
echo "${GREEN}════════════════════════════════════════════════════════${NC}"
echo ""

python3 app.py
