#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p static/uploads/company_logos
mkdir -p static/uploads/cv_files
mkdir -p static/uploads/profile_pictures
mkdir -p static/uploads/documents

# Initialize database
python initialize_database.py

echo "Build completed successfully!"
