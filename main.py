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
    Throttles the account creation process by waiting for a random duration between min_delay and max_delay seconds.
    
    Args:
        min_delay (int, optional): Minimum number of seconds to wait. Defaults to 30.
        max_delay (int, optional): Maximum number of seconds to wait. Defaults to 60.
    """
    delay = random.randint(min_delay, max_delay)  # Generate a random delay within the specified range
    logging.info(f"Throttling for {delay} seconds to avoid detection.")  # Log the delay duration
    time.sleep(delay)  # Pause execution for the delay duration

def main():
    """
    Main function to orchestrate the creation and customization of Twitter accounts.
    """
    try:
        # Initialize ProxyManager with the path to proxies.txt
        proxy_manager = ProxyManager("proxies.txt")  # Create an instance of ProxyManager
        logging.info("ProxyManager initialized.")  # Log successful initialization

        api = authenticate_twitter_api()  # Authenticate with the Twitter API
        logging.info("Authenticated with Twitter API.")  # Log successful authentication

        # List of account details to be created
        accounts = [
            {"username": "user1", "email": "user1@mailinator.com", "password": "Passw0rd!"},
            {"username": "user2", "email": "user2@mailinator.com", "password": "Passw0rd!"},
            # Add more accounts as needed
        ]

        for account in accounts:
            try:
                proxy = proxy_manager.get_proxy()  # Retrieve a proxy from ProxyManager
                logging.info(f"Using proxy: {proxy}")  # Log the proxy being used

                # Create a new Twitter account using the provided details and proxy
                create_twitter_account(api, account['username'], account['email'], account['password'], proxy)
                logging.info(f"Account created for user: {account['username']}")  # Log successful account creation

                verification_code = verify_email(account['email'])  # Verify the email and retrieve the verification code
                logging.info(f"Email verified for: {account['email']}")  # Log successful email verification

                # Customize the profile with a profile image and bio
                customize_profile(api, account['username'], "path_to_profile_image.jpg", "Automated account")
                logging.info(f"Profile customized for user: {account['username']}")  # Log successful profile customization

                proxy_manager.rotate_proxy()  # Rotate to the next proxy for the subsequent account
                logging.info("Proxy rotated for next account.")  # Log proxy rotation

                throttle()  # Throttle the process to control the rate of account creation

            except Exception as e:
                logging.error(f"Failed to create account for {account['username']}: {e}")  # Log errors specific to account creation

    except Exception as e:
        logging.error(f"An error occurred: {e}")  # Log any unexpected errors in the main process

if __name__ == "__main__":
    main()  # Execute the main function when the script is run directly
