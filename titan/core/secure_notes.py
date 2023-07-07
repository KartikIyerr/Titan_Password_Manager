import os
import subprocess
from cryptography.fernet import Fernet
import sys
import base64

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

# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

# Add the grandparent directory to sys.path
grandparent_dir = os.path.abspath(os.path.join(os.getcwd(), "../.."))
sys.path.append(grandparent_dir)

try:
    from titan.core.ascii_art import introBanner
    # from tpm2 import PasswordManager
except ImportError:
    print(f"{color_red}[!]{color_reset} Error importing the package.")


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
os.makedirs("Notes", exist_ok=True)


def gen_key():
    key = Fernet.generate_key()
    encoded_key = base64.urlsafe_b64encode(key).decode
    print(encoded_key)
    with open("Notes.key", 'wb') as w:
        w.write(encoded_key)
        w.close()


def encrypter(user_ip, save_choice, title):
    if not os.path.isfile("Notes.key"):
        gen_key()
    with open("Notes.key", 'rb') as r:
        encoded_key = r.read()
        print(encoded_key)
        key = base64.urlsafe_b64decode(encoded_key)
        print(key)
    cipher = Fernet(key)
    print(user_ip)


def sec_notes(username):
    introBanner()
    print(f"Welcome to the secure notes section of Titan Password Manager. Here you can store your valuable information and can fetch it whenever you want.\n")
    print(f"{color_green}[*]{color_reset} Select from the menu: \n")
    print(f"{color_blue}  1.{color_reset} View stored notes")
    print(f"{color_blue}  2.{color_reset} Write a new note\n")
    print(f"{color_blue} 99.{color_reset} Back to previous menu\n")
    while True:
        choice = int(input(
            f"{color_blue}{under}titan{color_reset}:{color_blue}{under}home{color_reset}:{color_blue}{under}secnotes{color_reset} > "))
        print()
        if choice == 2:
            title = input(
                f"{color_blue}[+]{color_reset} Enter the name of the title of your note: ")
            title = title.capitalize()
            print(
                f"{color_green}[*]{color_reset} Start writing whatever you want. Press {color_red}<enter>{color_reset} twice when finished.\n")
            try:
                lines = []
                while True:
                    line = input("")
                    if line == "":
                        break
                    lines.append(line)

                user_input = "\n".join(lines)
                save_choice = input(
                    f"{color_green}[-]{color_reset} Enter the filename to save with: ")

                # encrypted_txt = encrypter(user_input, save_choice, title)
                # writing contents to a file
                os.chdir("Notes")
                with open(save_choice, 'w') as w:
                    w.write(user_input)
                    w.close()
                print(f"{color_green}[!]{color_reset} Done.")
            except KeyboardInterrupt:
                pass

        elif choice == 1:
            files = os.listdir("Notes")
            for f, file in enumerate(files, start=1):
                print(f"  {color_blue}{f}.{color_reset} {file}")
            print(f"\n {color_blue}99.{color_reset} Back to previous menu.\n")

            while True:
                note_view = int(input(
                    f"{color_blue}{under}titan{color_reset}:{color_blue}{under}home{color_reset}:{color_blue}{under}secnotes{color_reset}:{color_blue}{under}viewnotes{color_reset} > "))

                if note_view > 0 and note_view <= len(files):
                    selected_file = files[note_view - 1]
                    file_path = os.path.join("Notes", selected_file)
                    subprocess.Popen(['notepad', file_path], shell=True)
                elif note_view == 99:
                    sec_notes(username)
                else:
                    print(
                        f"{color_red}[!] Provide a valid choice. {color_reset}")
        elif choice == 99:
            pass
