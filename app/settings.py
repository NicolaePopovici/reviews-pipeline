import os
import sys
import logging
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_logger():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    return root


logger = get_logger()

# Database settings
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_URL = os.getenv("POSTGRES_URL")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_DB_SCHEMA = os.getenv("POSTGRES_DB_SCHEMA")
API_V1_STR = os.getenv("API_V1_STR", "/api/v1")

BUCKET_NAME = os.getenv("BUCKET_NAME")
KEY = os.getenv("KEY")
