import os
import sys

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


def introBanner():
    if sys.platform == 'win32':
        os.system("cls")
    elif sys.platform == 'linux' or sys.platform == 'Darwin':
        os.system("clear")
    else:
        raise Exception(
            f"{color_red}[!] Unsupported Platform.{color_reset}")

#     print(color_red_bold + f"""
#  _______ _______ _______ _______ _______
# |_     _|_     _|_     _|   _   |    |  | {color_red}[-] Welcome to the TITAN Password manager (v1.0)
#   |   |  _|   |_  |   | |       |       | {color_reset}[-] Author: Kartik Iyer{color_red_bold}
#   |___| |_______| |___| |___|___|__|____| {color_red}[-] TITAN is the product of TaskOne

# Trusted Information and Technology Access Navigator
# {color_blue}Note: Some modules are still under development, this is only a trial model\nthat is being released for beta-testing.
#                 """ + color_reset)

    print(color_red_bold + f"""
 ___________________________ _______  _
 \__   __/\__   __/\__   __/(  ___  )( (    /|
    ) (      ) (      ) (   | (   ) ||  \  ( |
    | |      | |      | |   | (___) ||   \ | |  {color_red}[-] Welcome to the TITAN Password manager (v1.0)
    | |      | |      | |   |  ___  || (\ \) |  {color_reset}[-] Author: Kartik Iyer{color_red_bold}
    | |      | |      | |   | (   ) || | \   |  {color_red}[-] TITAN is the product of TaskOne
    | |   ___) (___   | |   | )   ( || )  \  |
    )_(   \_______/   )_(   |/     \||/    )_)

Trusted Information and Technology Access Navigator

{color_blue}Note: Some modules of this tool are still under the development stages. This model is just released\nfor the beta-testing purposes.
                """ + color_reset)
