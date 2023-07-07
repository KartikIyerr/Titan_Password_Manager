import os
import sys
import shutil
from docs.notice import display_terms

color_red = '\033[91m'
color_reset = '\033[0m'

# User's home
titan_code_dir = os.getcwd()
home_dir = os.path.expanduser("~")
titan_home = "TitanPwdManager"
config_folder = "TitanConfig"
comp_dir = os.path.join(home_dir, titan_home)
os.chdir(home_dir)
os.makedirs(comp_dir, exist_ok=True)
os.chdir(comp_dir)
os.makedirs(config_folder, exist_ok=True)


def checkUser():
    if os.path.isdir(comp_dir):
        os.chdir(comp_dir)
        os.makedirs(config_folder, exist_ok=True)
        os.chdir(config_folder)
        if os.path.isfile("user_acceptance_status.txt"):
            status_read = open("user_acceptance_status.txt", "r")
            status = status_read.read()
            if status == "User accepted":
                pass
        else:
            try:
                shutil.copy(
                    "D:/Python/Titan Password Manager/docs/notice.py", "./")
                if os.path.isfile("notice.py"):
                    display_terms()
                    terms_accept = input(
                        "Do you agree to the terms and conditions (y/n): ")
                    if terms_accept.lower() == "y":
                        acceptance_status = open(
                            "user_acceptance_status.txt", "w")
                        acceptance_status.write("User accepted")
                        acceptance_status.close()
                    else:
                        print(
                            f"{color_red}[!] You must agree to the terms and conditions before using the Titan Password manager. Exiting.{color_reset}")
                        sys.exit()
                else:
                    raise FileNotFoundError(
                        f"{color_red}[!] File not found.{color_reset}")
                    sys.exit()
            except Exception as e:
                print(e)
    else:
        print(f"{color_red}[!] No directory found.{color_reset}")
        sys.exit()
