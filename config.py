import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET_KEY = os.getenv("TWITTER_API_SECRET_KEY")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# Proxy settings
PROXY_LIST = "proxies.txt"  # File containing list of proxies

# Validate configuration
if not all([TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET]):
    logging.error("One or more Twitter API credentials are missing in the .env file.")
    raise EnvironmentError("Missing Twitter API credentials.")

logging.info("Configuration loaded successfully.")
