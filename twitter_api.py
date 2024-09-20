import tweepy  # Twitter API library for Python
from tweepy.errors import TweepyException  # Exception class for Tweepy-related errors
from config import TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET  # Importing Twitter API credentials from config
from selenium import webdriver  # Selenium library for browser automation
from selenium.webdriver.chrome.service import Service  # Service class to manage ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager  # Automatically manages ChromeDriver binaries
from selenium.webdriver.chrome.options import Options  # Class to set Chrome browser options
import time  # Time module for sleep delays
from captcha_solver import solve_captcha  # Custom module to solve CAPTCHAs
from email_verification import verify_email  # Custom module to verify email addresses
import logging  # Logging module for tracking events
import base64  # Base64 encoding/decoding
import requests  # HTTP library for making requests

def authenticate_twitter_api():
    """
    Authenticates with the Twitter API using Tweepy and returns the API object.
    
    Raises:
        TweepyException: If authentication fails.
    """
    try:
        auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)  # Initialize OAuth handler with API keys
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)  # Set access tokens
        api = tweepy.API(auth)  # Create Tweepy API object
        api.verify_credentials()  # Verify the credentials
        logging.info("Twitter API authentication successful.")  # Log successful authentication
        return api  # Return the authenticated API object
    except TweepyException as e:
        logging.error(f"Twitter API authentication failed: {e}")  # Log the error
        raise  # Re-raise the exception for upstream handling

def create_twitter_account(api, username, email, password, proxy=None):
    """
    Creates a new Twitter account using Selenium for browser automation.
    
    Args:
        api: Authenticated Tweepy API object.
        username (str): Desired username for the Twitter account.
        email (str): Email address for account registration.
        password (str): Password for the account.
        proxy (str, optional): Proxy server to route the browser traffic through.
    
    Raises:
        TweepyException: If there are issues with Tweepy API calls.
        Exception: For any unexpected errors during account creation.
    """
    # Configure Chrome options for Selenium
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation flags
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)

    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')  # Set proxy if provided

    # Initialize Selenium WebDriver with ChromeDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get("https://twitter.com/i/flow/signup")  # Navigate to Twitter signup page
        time.sleep(5)  # Wait for the page to load

        # Step 1: Enter Name
        name_field = driver.find_element("name", "name")  # Locate the name input field
        name_field.send_keys(username)  # Input the desired username
        logging.info("Entered username.")
        time.sleep(2)  # Pause for 2 seconds

        # Step 2: Enter Email
        email_field = driver.find_element("name", "email")  # Locate the email input field
        email_field.send_keys(email)  # Input the email address
        logging.info("Entered email.")
        time.sleep(2)  # Pause for 2 seconds

        # Step 3: Enter Password
        password_field = driver.find_element("name", "password")  # Locate the password input field
        password_field.send_keys(password)  # Input the password
        logging.info("Entered password.")
        time.sleep(2)  # Pause for 2 seconds

        # Handle Captcha if Present
        try:
            captcha_image = driver.find_element("id", "captcha_image_id")  # Locate the CAPTCHA image (update selector as needed)
            captcha_src = captcha_image.get_attribute('src')  # Get the source URL of the CAPTCHA image
            # Download and convert CAPTCHA image to base64
            captcha_response = requests.get(captcha_src)  # Fetch the CAPTCHA image
            captcha_base64 = base64.b64encode(captcha_response.content).decode('utf-8')  # Encode image in base64
            captcha_text = solve_captcha(captcha_base64)  # Solve CAPTCHA using the captcha_solver module
            
            captcha_field = driver.find_element("name", "captcha_field_name")  # Locate the CAPTCHA input field (update selector as needed)
            captcha_field.send_keys(captcha_text)  # Input the solved CAPTCHA text
            logging.info("Solved and entered captcha.")
            time.sleep(2)  # Pause for 2 seconds
        except Exception as e:
            logging.info("No captcha found or an error occurred:", exc_info=True)  # Log if CAPTCHA handling fails

        # Submit the signup form
        submit_button = driver.find_element("xpath", "//button[@type='submit']")  # Locate the submit button
        submit_button.click()  # Click the submit button to submit the form
        logging.info("Submitted signup form.")
        time.sleep(5)  # Wait for the verification step

        # Verify Email
        verification_code = verify_email(email)  # Retrieve the verification code via email_verification module
        verification_field = driver.find_element("name", "verification_code")  # Locate the verification code input field (update selector as needed)
        verification_field.send_keys(verification_code)  # Input the verification code
        logging.info("Entered verification code.")
        time.sleep(2)  # Pause for 2 seconds

        # Finalize Account Creation
        finalize_button = driver.find_element("xpath", "//button[@type='submit']")  # Locate the finalize button
        finalize_button.click()  # Click the finalize button to complete account creation
        logging.info("Finalized account creation.")
        time.sleep(5)  # Wait for account creation to complete

        logging.info(f"Successfully created Twitter account for user: {username}")  # Log successful account creation

    except TweepyException as e:
        logging.error(f"An error occurred during account creation for {username}: {e}", exc_info=True)  # Log Tweepy-related errors
        raise  # Re-raise the exception
    except Exception as e:
        logging.error(f"An unexpected error occurred during account creation for {username}: {e}", exc_info=True)  # Log unexpected errors
        raise  # Re-raise the exception
    finally:
        driver.quit()  # Ensure the browser is closed regardless of success or failure

def customize_profile(api, username, profile_picture, bio):
    """
    Customizes the Twitter profile by updating the profile picture and bio.
    
    Args:
        api: Authenticated Tweepy API object.
        username (str): Twitter username whose profile is to be customized.
        profile_picture (str): Path to the profile image file.
        bio (str): Bio text to be set for the profile.
    
    Raises:
        TweepyException: If there are issues with Tweepy API calls.
    """
    try:
        user = api.get_user(screen_name=username)  # Retrieve the user object for the given username
        api.update_profile_image(profile_picture)  # Update the profile image with the provided picture
        api.update_profile(description=bio)  # Update the profile bio with the provided text
        logging.info(f"Profile customized for user: {username}")  # Log successful profile customization
    except TweepyException as e:
        logging.error(f"Failed to customize profile for {username}: {e}")  # Log any errors encountered
        raise  # Re-raise the exception for upstream handling
