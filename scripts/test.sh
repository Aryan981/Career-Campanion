#!/bin/bash
set -e

echo "Running Backend Tests..."
export PYTHONPATH=$PYTHONPATH:$(pwd)
export OPENROUTER_API_KEY=sk-dummy-key-for-tests
python3 -m pytest backend/tests/test_main.py -v
