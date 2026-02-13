#!/bin/bash

# Initialize database
python models.py

# Run database migrations
alembic upgrade head

# Start FastAPI server
python main.py
