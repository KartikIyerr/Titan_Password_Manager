import requests
import hashlib
import getpass
from titan.core.ascii_art import introBanner

# color codes
color_red = '\033[91m'
color_red_bold = '\033[1;91m'
color_green = '\033[92m'
color_green_bold = '\033[1;92m'
color_yellow = '\033[93m'
color_yellow_bold = '\033[1;93m'
color_blue = '\033[94m'
color_blue_bold = '\033[1;94m'
under = '\033[4m'
color_reset = '\033[0m'


def check_pwned(username):
    introBanner()
    print(f"Welcome to the Titan's password leak detection section.\n ")
    password = getpass.getpass(
        f"{color_green}[*]{color_reset} Enter the password to check pwning status: ")
    hash_pwd = hashlib.sha1(password.encode()).hexdigest().upper()

    suffix = hash_pwd[5:]
    prefix = hash_pwd[:5]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    # Added a User-Agent header to avoid 403 Forbidden response
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers)
    except requests.ConnectionError as ce:
        print(ce)

    if response.status_code == 200:
        # Account has been breached
        hashes = response.text.split('\n')
        # print(hashes)

        for hash in hashes:
            if hash.startswith(suffix):
                count = int(hash.split(':')[1])
                if count > 0 or count < 100:
                    print(
                        f"{color_red}[!]{color_reset} The password '{password}' has been breached {color_yellow}{count}{color_reset} times.")
                elif count > 100:
                    print(
                        f"{color_red}[!]{color_reset} The password '{password}' has been breached {color_red}{count}{color_reset} times.")
                else:
                    print(
                        f"{color_green}[!]{color_reset} The password '{password}' has not been breached yet.")
                return

    print(
        f"{color_green}[!]{color_reset} The password '{password}' has not been breached yet.")
