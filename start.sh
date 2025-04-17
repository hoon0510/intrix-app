#!/bin/bash
cd backend
pip install -r ../requirements.txt
PYTHONPATH=. uvicorn main:app --host 0.0.0.0 --port 8000 