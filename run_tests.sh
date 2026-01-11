#!/bin/bash
# Run all tests using the project's virtual environment
# Passes any additional arguments to pytest (e.g., -v, -k "test_name")
./venv/bin/python3 -m pytest flashcards/tests/ "$@"
