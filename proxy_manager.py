import itertools
import logging

class ProxyManager:
    def __init__(self, proxy_file):
        self.proxies = self.load_proxies(proxy_file)
        if not self.proxies:
            raise ValueError("No proxies found in the proxy file.")
        self.proxy_cycle = itertools.cycle(self.proxies)
        logging.info(f"Loaded {len(self.proxies)} proxies.")

    def load_proxies(self, proxy_file):
        try:
            with open(proxy_file, 'r') as f:
                proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            logging.info(f"Loaded proxies from {proxy_file}.")
            return proxies
        except FileNotFoundError:
            logging.error(f"Proxy file {proxy_file} not found.")
            raise
        except Exception as e:
            logging.error(f"Error loading proxies from {proxy_file}: {e}")
            raise

    def get_proxy(self):
        try:
            proxy = next(self.proxy_cycle)
            logging.info(f"Using proxy: {proxy}")
            return proxy
        except Exception as e:
            logging.error(f"Error getting proxy: {e}")
            raise

    def rotate_proxy(self):
        try:
            proxy = next(self.proxy_cycle)
            logging.info(f"Rotated to new proxy: {proxy}")
            return proxy
        except Exception as e:
            logging.error(f"Error rotating proxy: {e}")
            raise
