#!/bin/bash
# Script to execute the School Enrollment Management System Framework
# This starts the Streamlit application

# Set colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Sistema de Matrícula Escolar 2026${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Change to the script directory
cd "$(dirname "$0")"

echo -e "${GREEN}Starting Streamlit application...${NC}"
echo ""

# Check if dependencies are installed
if ! command -v streamlit &> /dev/null; then
    echo "Streamlit is not installed. Installing dependencies..."
    
    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        echo "Error: requirements.txt not found in current directory."
        exit 1
    fi
    
    # Attempt to install dependencies
    if ! pip install -r requirements.txt; then
        echo "Error: Failed to install dependencies. Please check:"
        echo "  1. Ensure pip is properly installed"
        echo "  2. Check your internet connection"
        echo "  3. Verify requirements.txt is not corrupted"
        exit 1
    fi
fi

echo ""
echo -e "${GREEN}Starting application...${NC}"
echo -e "Access the application at: ${BLUE}http://localhost:8501${NC}"
echo ""

# Run the application (runs in foreground)
streamlit run app.py --server.port 8501
