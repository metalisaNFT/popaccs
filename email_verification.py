import requests
import time
import logging

def verify_email(email):
    try:
        # Example using Mailinator API
        api_token = 'your_mailinator_api_token'
        inbox = email.split('@')[0]
        domain = email.split('@')[1]

        # Poll for the verification email
        for attempt in range(30):  # Retry up to 30 times (e.g., 5 minutes)
            url = f"https://api.mailinator.com/v2/domains/{domain}/inboxes/{inbox}/messages"
            headers = {
                'Authorization': f'Bearer {api_token}'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            messages = response.json().get('messages', [])
            for message in messages:
                if 'verification code' in message['subject'].lower():  # Adjust condition as needed
                    message_id = message['id']
                    # Fetch the message content
                    msg_url = f"https://api.mailinator.com/v2/domains/{domain}/inboxes/{inbox}/messages/{message_id}"
                    msg_response = requests.get(msg_url, headers=headers)
                    msg_response.raise_for_status()
                    msg_content = msg_response.json().get('data', {}).get('parts', [])
                    for part in msg_content:
                        if part['mime_type'] == 'text/plain':
                            body = part['body']
                            # Extract verification code from the body
                            verification_code = extract_verification_code(body)
                            logging.info(f"Verification code extracted: {verification_code}")
                            return verification_code
            logging.info("Verification email not received yet. Retrying in 10 seconds.")
            time.sleep(10)  # Wait before retrying

        raise Exception("Verification email not received in time.")

    except requests.RequestException as e:
        logging.error(f"HTTP error during email verification for {email}: {e}")
        raise
    except Exception as e:
        logging.error(f"Error during email verification for {email}: {e}")
        raise

def extract_verification_code(email_body):
    import re
    match = re.search(r'(\d{6})', email_body)  # Example: 6-digit code
    if match:
        return match.group(1)
    else:
        raise Exception("Verification code not found in the email.")
