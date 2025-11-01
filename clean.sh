#!/bin/bash

echo "🧹 Cleaning Spyder OSINT Repository..."
echo "===================================="

# Remove Python cache
echo "[+] Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null

# Remove temporary files
echo "[+] Removing temporary files..."
find . -name "*.tmp" -delete 2>/dev/null
find . -name "*.temp" -delete 2>/dev/null
find . -name "*.log" -delete 2>/dev/null

# Remove IDE files
echo "[+] Removing IDE files..."
rm -rf .vscode/ .idea/ 2>/dev/null

# Remove OS files
echo "[+] Removing OS generated files..."
find . -name ".DS_Store" -delete 2>/dev/null
find . -name "Thumbs.db" -delete 2>/dev/null

# Clean results directory but keep structure
echo "[+] Cleaning results directory..."
if [ -d "results" ]; then
    rm -f results/*.json 2>/dev/null
    echo "  Results directory cleaned (structure preserved)"
fi

# Remove old virtual environments
echo "[+] Checking for old virtual environments..."
if [ -d "venv" ]; then
    echo "  Virtual environment found - keeping it"
else
    echo "  No virtual environment found"
fi

echo ""
echo "✅ Repository cleaned successfully!"
echo ""
echo "Repository structure:"
tree -I '__pycache__|*.pyc|venv|.git' -L 3 2>/dev/null || ls -la
