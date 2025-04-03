import os
from dotenv import load_dotenv
import logging

logging.basicConfig(
    filename="logs/api-gateway.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s", 
)
logger = logging.getLogger(__name__)

ENVIRONMENT = os.getenv("ENV", "development")
if ENVIRONMENT == "development":
    load_dotenv(".env.dev")
else:
    load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///dev.db")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
DEBUG_MODE = os.getenv("DEBUG", True)