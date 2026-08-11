import os

from dotenv import load_dotenv
from neo4j import GraphDatabase


# Load environment variables
load_dotenv()


COGNODB_URI = os.getenv("COGNODB_URI")
COGNODB_USERNAME = os.getenv("COGNODB_USERNAME")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD")


if not COGNODB_URI:
    raise ValueError("COGNODB_URI is missing")

if not COGNODB_USERNAME:
    raise ValueError("COGNODB_USERNAME is missing")

if not COGNODB_PASSWORD:
    raise ValueError("COGNODB_PASSWORD is missing")


# Create one database driver
driver = GraphDatabase.driver(
    COGNODB_URI,
    auth=(
        COGNODB_USERNAME,
        COGNODB_PASSWORD
    )
)


def get_driver():
    """
    Return the CognoDB driver.
    """
    return driver


def close_driver():
    """
    Close the database connection.
    """
    driver.close()