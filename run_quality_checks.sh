#!/usr/bin/env bash

set -e

echo "=========================================="
echo "RUNNING HEALTHCARE ETL PIPELINE"
echo "=========================================="

./.venv/Scripts/python.exe main.py

echo
echo "=========================================="
echo "RUNNING AUTOMATED TESTS"
echo "=========================================="

./.venv/Scripts/python.exe -m unittest discover -s tests -v

echo
echo "=========================================="
echo "ALL PIPELINE AND QUALITY CHECKS PASSED"
echo "=========================================="