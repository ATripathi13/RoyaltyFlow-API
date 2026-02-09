#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Run seed data script to initialize the SQLite database
python -m app.seed_data
