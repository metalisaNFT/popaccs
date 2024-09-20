import requests
import time
import logging

def solve_captcha(captcha_image_base64):
    try:
        # Example using 2Captcha API
        api_key = 'your_2captcha_api_key'
        url = 'http://2captcha.com/in.php'
        payload = {
            'method': 'base64',
            'key': api_key,
            'body': captcha_image_base64,
            'json': 1
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()
        result = response.json()
        if result['status'] == 1:
            request_id = result['request']
            fetch_url = 'http://2captcha.com/res.php'
            fetch_payload = {
                'key': api_key,
                'action': 'get',
                'id': request_id,
                'json': 1
            }
            while True:
                res = requests.get(fetch_url, params=fetch_payload)
                res.raise_for_status()
                res_json = res.json()
                if res_json['status'] == 1:
                    logging.info("Captcha solved.")
                    return res_json['request']
                elif res_json['request'] == 'CAPCHA_NOT_READY':
                    logging.info("Captcha not ready. Waiting 5 seconds.")
                    time.sleep(5)
                else:
                    raise Exception(f"Error solving captcha: {res_json['request']}")
        else:
            raise Exception(f"Error submitting captcha: {result['request']}")

    except requests.RequestException as e:
        logging.error(f"HTTP error during captcha solving: {e}")
        raise
    except Exception as e:
        logging.error(f"Error solving captcha: {e}")
        raise
