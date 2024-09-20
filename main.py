from twitter_api import authenticate_twitter_api, create_twitter_account, customize_profile
from email_verification import verify_email
from captcha_solver import solve_captcha
from proxy_manager import ProxyManager
import logging
import time
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

def throttle(min_delay=30, max_delay=60):
    """
    Throttle account creation by waiting for a random period between min_delay and max_delay seconds.
    """
    delay = random.randint(min_delay, max_delay)
    logging.info(f"Throttling for {delay} seconds to avoid detection.")
    time.sleep(delay)

def main():
    try:
        # Initialize ProxyManager with the path to proxies.txt
        proxy_manager = ProxyManager("proxies.txt")
        logging.info("ProxyManager initialized.")

        api = authenticate_twitter_api()
        logging.info("Authenticated with Twitter API.")

        accounts = [
            {"username": "user1", "email": "user1@mailinator.com", "password": "Passw0rd!"},
            {"username": "user2", "email": "user2@mailinator.com", "password": "Passw0rd!"},
            # Add more accounts as needed
        ]

        for account in accounts:
            try:
                proxy = proxy_manager.get_proxy()
                logging.info(f"Using proxy: {proxy}")

                create_twitter_account(api, account['username'], account['email'], account['password'], proxy)
                logging.info(f"Account created for user: {account['username']}")

                verification_code = verify_email(account['email'])
                logging.info(f"Email verified for: {account['email']}")

                customize_profile(api, account['username'], "path_to_profile_image.jpg", "Automated account")
                logging.info(f"Profile customized for user: {account['username']}")

                proxy_manager.rotate_proxy()
                logging.info("Proxy rotated for next account.")

                throttle()  # Control the rate of account creation

            except Exception as e:
                logging.error(f"Failed to create account for {account['username']}: {e}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
