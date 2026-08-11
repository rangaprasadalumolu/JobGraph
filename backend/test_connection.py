import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


# Load variables from .env
load_dotenv()

COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")


if not COGNODB_URI:
    raise ValueError("COGNODB_URI is missing from .env")

if not COGNODB_USERNAME:
    raise ValueError("COGNODB_USERNAME is missing from .env")

if not COGNODB_PASSWORD:
    raise ValueError("COGNODB_PASSWORD is missing from .env")


driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(COGNODB_USERNAME, COGNODB_PASSWORD)
)


try:
    driver.verify_connectivity()
    print("=================================")
    print("CognoDB connection successful!")
    print("=================================")

finally:
    driver.close()