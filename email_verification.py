import requests
import time
import logging

def verify_email(email):
    """
    Verifies the email address by polling the Mailinator API for a verification email and extracting the code.
    
    Args:
        email (str): The email address to verify.
    
    Returns:
        str: The extracted verification code from the email.
    
    Raises:
        Exception: If the verification email is not received in time or other errors occur.
    """
    try:
        # Example using Mailinator API
        api_token = 'your_mailinator_api_token'  # Replace with your actual Mailinator API token
        inbox = email.split('@')[0]  # Extract the inbox name from the email address
        domain = email.split('@')[1]  # Extract the domain from the email address

        # Poll for the verification email with a maximum of 30 attempts (e.g., 5 minutes)
        for attempt in range(30):
            url = f"https://api.mailinator.com/v2/domains/{domain}/inboxes/{inbox}/messages"  # Mailinator API endpoint for inbox messages
            headers = {
                'Authorization': f'Bearer {api_token}'  # Authorization header with Bearer token
            }
            response = requests.get(url, headers=headers)  # Make GET request to fetch messages
            response.raise_for_status()  # Raise an error for bad status codes
            messages = response.json().get('messages', [])  # Parse JSON response to get messages
            for message in messages:
                if 'verification code' in message['subject'].lower():  # Check if the message subject contains 'verification code'
                    message_id = message['id']  # Get the ID of the relevant message
                    # Fetch the message content using the message ID
                    msg_url = f"https://api.mailinator.com/v2/domains/{domain}/inboxes/{inbox}/messages/{message_id}"
                    msg_response = requests.get(msg_url, headers=headers)  # Make GET request to fetch message content
                    msg_response.raise_for_status()  # Raise an error for bad status codes
                    msg_content = msg_response.json().get('data', {}).get('parts', [])  # Extract message parts
                    for part in msg_content:
                        if part['mime_type'] == 'text/plain':  # Look for the plain text part of the email
                            body = part['body']  # Get the body of the email
                            # Extract verification code from the body using a helper function
                            verification_code = extract_verification_code(body)
                            logging.info(f"Verification code extracted: {verification_code}")  # Log the extracted code
                            return verification_code  # Return the verification code
            logging.info("Verification email not received yet. Retrying in 10 seconds.")  # Log that the email hasn't been received yet
            time.sleep(10)  # Wait for 10 seconds before retrying

        raise Exception("Verification email not received in time.")  # Raise an exception if the email isn't received in time

    except requests.RequestException as e:
        logging.error(f"HTTP error during email verification for {email}: {e}")  # Log HTTP-related errors
        raise  # Re-raise the exception for upstream handling
    except Exception as e:
        logging.error(f"Error during email verification for {email}: {e}")  # Log any other errors
        raise  # Re-raise the exception

def extract_verification_code(email_body):
    """
    Extracts a 6-digit verification code from the email body using regular expressions.
    
    Args:
        email_body (str): The body content of the verification email.
    
    Returns:
        str: The extracted 6-digit verification code.
    
    Raises:
        Exception: If no verification code is found in the email body.
    """
    import re  # Regular expressions module
    match = re.search(r'(\d{6})', email_body)  # Search for a sequence of 6 digits
    if match:
        return match.group(1)  # Return the matched verification code
    else:
        raise Exception("Verification code not found in the email.")  # Raise an exception if no code is found
