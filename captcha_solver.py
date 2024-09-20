import requests  # HTTP library for making requests
import time  # Time module for sleep delays
import logging  # Logging module for tracking events

def solve_captcha(captcha_image_base64):
    """
    Solves a CAPTCHA by sending the base64-encoded image to the 2Captcha API and retrieving the solved text.
    
    Args:
        captcha_image_base64 (str): The base64-encoded CAPTCHA image.
    
    Returns:
        str: The solved CAPTCHA text.
    
    Raises:
        Exception: If there are issues with the CAPTCHA solving process.
    """
    try:
        # Example using 2Captcha API
        api_key = 'your_2captcha_api_key'  # Replace with your actual 2Captcha API key
        url = 'http://2captcha.com/in.php'  # Endpoint to submit CAPTCHA for solving
        payload = {
            'method': 'base64',  # Specify that the CAPTCHA image is sent as a base64 string
            'key': api_key,  # API key for authentication
            'body': captcha_image_base64,  # The base64-encoded CAPTCHA image
            'json': 1  # Request JSON response
        }
        response = requests.post(url, data=payload)  # Submit the CAPTCHA solving request
        response.raise_for_status()  # Raise an error for bad status codes
        result = response.json()  # Parse JSON response
        if result['status'] == 1:
            request_id = result['request']  # Get the request ID for polling
            fetch_url = 'http://2captcha.com/res.php'  # Endpoint to fetch the solved CAPTCHA
            fetch_payload = {
                'key': api_key,  # API key for authentication
                'action': 'get',  # Specify action to get the result
                'id': request_id,  # The request ID obtained earlier
                'json': 1  # Request JSON response
            }
            while True:
                res = requests.get(fetch_url, params=fetch_payload)  # Poll for the solved CAPTCHA
                res.raise_for_status()  # Raise an error for bad status codes
                res_json = res.json()  # Parse JSON response
                if res_json['status'] == 1:
                    logging.info("Captcha solved.")  # Log successful CAPTCHA solving
                    return res_json['request']  # Return the solved CAPTCHA text
                elif res_json['request'] == 'CAPCHA_NOT_READY':
                    logging.info("Captcha not ready. Waiting 5 seconds.")  # Log that CAPTCHA is not ready yet
                    time.sleep(5)  # Wait before retrying
                else:
                    raise Exception(f"Error solving captcha: {res_json['request']}")  # Raise exception for other errors
        else:
            raise Exception(f"Error submitting captcha: {result['request']}")  # Raise exception if submission failed

    except requests.RequestException as e:
        logging.error(f"HTTP error during captcha solving: {e}")  # Log HTTP-related errors
        raise  # Re-raise the exception
    except Exception as e:
        logging.error(f"Error solving captcha: {e}")  # Log any other errors
        raise  # Re-raise the exception
