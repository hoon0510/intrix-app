"""
API Package
"""

from fastapi import FastAPI

app = FastAPI(
    title="Intrix API",
    description="Intrix Application API",
    version="0.1.0"
)
