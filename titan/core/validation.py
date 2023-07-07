import re
import os


# color codes
color_red = '\033[91m'
color_red_bold = '\033[1;91m'
color_green = '\033[92m'
color_green_bold = '\033[1;92m'
color_yellow = '\033[93m'
color_yellow_bold = '\033[1;93m'
color_blue = '\033[94m'
color_blue_bold = '\033[1;94m'
color_reset = '\033[0m'


def validate_password(password):
    # Password rules:
    # - At least 8 characters long
    # - Contains at least one uppercase letter
    # - Contains at least one lowercase letter
    # - Contains at least one digit
    # - Contains at least one special character from !@#$%^&*

    # using regular expression to validate the conditions.
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*]).{8,}$"

    # Check if the password matches the pattern
    if re.match(pattern, password):
        return True
    else:
        print(
            f"{color_yellow}[!] The password you entered is not acceptable. Please try to create a complex one!{color_reset}")
        return False


def validate_username(username):
    pass
