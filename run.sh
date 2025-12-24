#!/bin/bash
set -e

# Setup venv if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Installing dependencies..."
    ./venv/bin/pip install -r requirements.txt
fi

# Run the app
./venv/bin/python ascii_app.py
