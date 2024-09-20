import tweepy
from tweepy.errors import TweepyException  # Updated import
from config import TWITTER_API_KEY, TWITTER_API_SECRET_KEY, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from captcha_solver import solve_captcha
from email_verification import verify_email
import logging
import base64
import requests

def authenticate_twitter_api():
    try:
        auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        api.verify_credentials()
        logging.info("Twitter API authentication successful.")
        return api
    except TweepyException as e:  # Updated exception
        logging.error(f"Twitter API authentication failed: {e}")
        raise

def create_twitter_account(api, username, email, password, proxy=None):
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless")  # Run in headless mode

    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get("https://twitter.com/i/flow/signup")
        time.sleep(5)  # Wait for the page to load

        # Step 1: Enter Name
        name_field = driver.find_element("name", "name")
        name_field.send_keys(username)
        logging.info("Entered username.")
        time.sleep(2)

        # Step 2: Enter Email
        email_field = driver.find_element("name", "email")
        email_field.send_keys(email)
        logging.info("Entered email.")
        time.sleep(2)

        # Step 3: Enter Password
        password_field = driver.find_element("name", "password")
        password_field.send_keys(password)
        logging.info("Entered password.")
        time.sleep(2)

        # Handle Captcha if Present
        try:
            captcha_image = driver.find_element("id", "captcha_image_id")  # Update selector as needed
            captcha_src = captcha_image.get_attribute('src')
            # Download and convert captcha image to base64
            captcha_response = requests.get(captcha_src)
            captcha_base64 = base64.b64encode(captcha_response.content).decode('utf-8')
            captcha_text = solve_captcha(captcha_base64)
            
            captcha_field = driver.find_element("name", "captcha_field_name")  # Update selector as needed
            captcha_field.send_keys(captcha_text)
            logging.info("Solved and entered captcha.")
            time.sleep(2)
        except Exception as e:
            logging.info("No captcha found or an error occurred:", exc_info=True)

        # Submit the signup form
        submit_button = driver.find_element("xpath", "//button[@type='submit']")
        submit_button.click()
        logging.info("Submitted signup form.")
        time.sleep(5)  # Wait for the verification step

        # Verify Email
        verification_code = verify_email(email)
        verification_field = driver.find_element("name", "verification_code")  # Update selector as needed
        verification_field.send_keys(verification_code)
        logging.info("Entered verification code.")
        time.sleep(2)

        # Finalize Account Creation
        finalize_button = driver.find_element("xpath", "//button[@type='submit']")
        finalize_button.click()
        logging.info("Finalized account creation.")
        time.sleep(5)  # Wait for account creation to complete

        logging.info(f"Successfully created Twitter account for user: {username}")

    except TweepyException as e:  # If Tweepy exceptions are raised here
        logging.error(f"An error occurred during account creation for {username}: {e}", exc_info=True)
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred during account creation for {username}: {e}", exc_info=True)
        raise
    finally:
        driver.quit()

def customize_profile(api, username, profile_picture, bio):
    try:
        user = api.get_user(screen_name=username)
        api.update_profile_image(profile_picture)
        api.update_profile(description=bio)
        logging.info(f"Profile customized for user: {username}")
    except TweepyException as e:  # Updated exception
        logging.error(f"Failed to customize profile for {username}: {e}")
        raise
