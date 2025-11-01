
#!/bin/bash
# Spyder OSINT Setup Script

echo "Setting up Spyder OSINT environment..."

# Deactivate any existing virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    deactivate 2>/dev/null || true
fi

# Remove corrupted virtual environment
if [ -d "venv" ]; then
    echo "Removing corrupted virtual environment..."
    rm -rf venv
fi

# Create new virtual environment
echo "Creating new virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo "Setup complete! Virtual environment is ready."
echo "To activate in the future, run: source venv/bin/activate"
