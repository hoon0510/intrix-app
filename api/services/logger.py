import logging
from datetime import datetime
import os
from pathlib import Path

def setup_logger():
    """Configure and setup the application logger"""
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"),
            logging.StreamHandler()
        ]
    )
    
    # Create logger instance
    logger = logging.getLogger("intrix")
    
    # Set log level based on environment
    if os.getenv("ENV") == "production":
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)
    
    return logger

# Initialize logger
logger = setup_logger() 