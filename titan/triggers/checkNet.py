import requests


def check_internet_connection():
    try:
        # Make a HEAD request to a reliable website
        response = requests.head("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False
