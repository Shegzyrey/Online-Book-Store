#!/usr/bin/env bash


SLEEP_INTERVAL=15

echo "Waiting for services... "


sleep $SLEEP_INTERVAL

# Run the Python application
echo "Starting Python application..."

python3 run.py
