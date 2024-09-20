import itertools
import logging

class ProxyManager:
    """
    A class to manage a list of proxy servers for routing traffic.
    """
    def __init__(self, proxy_file):
        """
        Initializes the ProxyManager by loading proxies from a file and setting up a cyclic iterator.
        
        Args:
            proxy_file (str): Path to the file containing proxy addresses.
        
        Raises:
            ValueError: If no proxies are found in the provided file.
        """
        self.proxies = self.load_proxies(proxy_file)  # Load proxies from the specified file
        if not self.proxies:
            raise ValueError("No proxies found in the proxy file.")  # Raise an error if the proxy list is empty
        self.proxy_cycle = itertools.cycle(self.proxies)  # Create a cyclic iterator to rotate proxies
        logging.info(f"Loaded {len(self.proxies)} proxies.")  # Log the number of proxies loaded

    def load_proxies(self, proxy_file):
        """
        Loads proxies from a given file, ignoring empty lines and comments.
        
        Args:
            proxy_file (str): Path to the file containing proxy addresses.
        
        Returns:
            list: A list of proxy addresses.
        
        Raises:
            FileNotFoundError: If the proxy file does not exist.
            Exception: For any other errors during file reading.
        """
        try:
            with open(proxy_file, 'r') as f:
                proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]  # Read and clean proxy lines
            logging.info(f"Loaded proxies from {proxy_file}.")  # Log successful proxy loading
            return proxies  # Return the list of proxies
        except FileNotFoundError:
            logging.error(f"Proxy file {proxy_file} not found.")  # Log missing proxy file
            raise  # Re-raise the exception
        except Exception as e:
            logging.error(f"Error loading proxies from {proxy_file}: {e}")  # Log other errors
            raise  # Re-raise the exception

    def get_proxy(self):
        """
        Retrieves the next proxy in the cycle.
        
        Returns:
            str: The next proxy address.
        
        Raises:
            Exception: If there is an error retrieving the proxy.
        """
        try:
            proxy = next(self.proxy_cycle)  # Get the next proxy from the cyclic iterator
            logging.info(f"Using proxy: {proxy}")  # Log the proxy being used
            return proxy  # Return the proxy address
        except Exception as e:
            logging.error(f"Error getting proxy: {e}")  # Log any errors encountered
            raise  # Re-raise the exception

    def rotate_proxy(self):
        """
        Rotates to the next proxy in the cycle.
        
        Returns:
            str: The new proxy address after rotation.
        
        Raises:
            Exception: If there is an error during proxy rotation.
        """
        try:
            proxy = next(self.proxy_cycle)  # Rotate to the next proxy
            logging.info(f"Rotated to new proxy: {proxy}")  # Log the rotation
            return proxy  # Return the new proxy address
        except Exception as e:
            logging.error(f"Error rotating proxy: {e}")  # Log any errors encountered
            raise  # Re-raise the exception
