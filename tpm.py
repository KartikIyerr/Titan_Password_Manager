#!/usr/bin/env python

#########################################################################################
#                                                                                       #
#   Titan Password Manager - Secure and Easy-to-Use Password Management Solution        #
#                                                                                       #
#   COPYRIGHT (c) 2023 - All Rights Reserved                                            #
#                                                                                       #
#   Author: Kartik Iyer                                                                 #        #
#   License: This product is licensed under the terms of the GNU Public License.        #
#                                                                                       #
#   WARNING: DO NOT MODIFY THIS CODE UNLESS YOU FULLY UNDERSTAND ITS FUNCTIONALITY.     #
#            MAKING CHANGES WITHOUT PROPER KNOWLEDGE CAN COMPROMISE THE SECURITY        #
#            AND FUNCTIONALITY OF THE PASSWORD MANAGER.                                 #
#                                                                                       #
#########################################################################################


import sys
import os
import getpass
import sqlite3
import time
import base64
import argparse
import random
import string
import logging
import pyperclip

sys.dont_write_bytecode = True

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


# importing core modules
try:
    from titan.core.ascii_art import introBanner
    from titan.core.validation import validate_password
    from titan.core.EncryptionDecryption import EncryptionDecryption
    from titan.core.ConnectionClass import DBConnectionProcedures
    from titan.core.pwne_check import check_pwned
    from titan.core.secure_notes import sec_notes
    from titan.triggers.checkUser import checkUser
    from titan.triggers.Manual import Manual
    from titan.triggers.checkNet import check_internet_connection
    from titan.triggers.dailyTips import tips

except ImportError as i:
    print(f"{color_red}[!]{color_reset} Error importing the packages. {i}")
    sys.exit(1)

try:
    from cryptography.fernet import Fernet
except ImportError:
    os.system("pip3 install cryptography")

# Python2/3 compatibility
try:
    input = raw_input
except NameError:
    pass


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

# # checking the acceptance of user agreement
# checkUser()


# main code
try:
    class PasswordManager(EncryptionDecryption, DBConnectionProcedures):
        def __init__(self):
            self.cipher = None
            logging.basicConfig(filename="titan.log",
                                level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        def platform_check(self):
            # checking the platform
            if (sys.platform == 'win32'):
                tip = tips()
                print(f"{color_yellow}Tip: {tip}{color_reset}\n")
                print(
                    f"{color_red_bold}[-]{color_reset} Operating system detected: Windows \n")
                logging.info("Operating System detected: Windows.")
            elif (sys.platform == 'linux'):
                print(
                    f"{color_red_bold}[-]{color_reset} Operating system detected: Linux ")

                # checking for root
                if os.geteuid() != 0:
                    print(
                        f"\n  TITAN Password Manager - By Kartik Iyer")
                    print(
                        f"  Not running as {color_red}root{color_reset}. Exiting the TITAN Password Manager.\n")
                    sys.exit()
            else:
                print(
                    f"  {color_red_bold}[!]{color_reset} This tool does not support your device.")

        def checkMasterCredentials(self, username, password):
            os.chdir(home_dir)
            try:
                if os.path.isdir("TitanPwdManager"):
                    os.chdir("TitanPwdManager")
                    conn = sqlite3.connect("TitanDatabase")
                    if conn:
                        cursor = conn.cursor()
                        cursor.execute(
                            f"SELECT DB_PWD from StoredMasterPwd where NAME = '{username}'")

                        pwd_frm_db = cursor.fetchone()
                        # print(pwd_frm_db)

                        if pwd_frm_db:
                            encryptedPwd = base64.b64decode(pwd_frm_db[0])
                            decryptedPwd = self.decPwd(encryptedPwd)
                            decryptedPwd = decryptedPwd.decode('utf-8')
                            cursor.connection.commit()
                            conn.close()
                            return decryptedPwd

                        else:
                            print(
                                f"{color_yellow}  [!] Are you a new user? Maybe you should register with us!{color_reset}")
                            while True:
                                user_choice = input(
                                    f"{color_blue_bold}  [-]{color_reset} Can I take you to the Registration process? (y/n): ")
                                if user_choice == "y" or user_choice == "Y":

                                    self.registrationMenu()
                                elif user_choice == "n" or user_choice == "N":
                                    introBanner()
                                    self.MainMenu()
                                else:
                                    raise ValueError(
                                        f"{color_red}[!]{color_reset} Enter a proper value")
                    else:
                        print(
                            f"{color_red}[!] Problem connecting with the database.")
                else:
                    print(
                        f"{color_red}  [!]{color_reset} No database initialized. Maybe you have not yet registered with us...")
                    sys.exit(0)
            except Exception as e:
                print(
                    f"{color_yellow}  [!] Are you a new user? Maybe you should register with us!{color_reset}")
                time.sleep(1)
                self.MainMenu()

        def registrationMenu(self):
            try:
                introBanner()
                logging.info("User selected registration menu.")
                print(f"Welcome to the Registration section of Titan Password manager. Create your new vault\nby providing us the required information and be sure to keep the master password SAFE.\n")
                print(
                    f"{color_red}Warning:{color_reset} Master password is non-recoverable. Please keep it in a safe place.\n")
                print(
                    f"{color_green_bold}[+] Create Master Credentials{color_reset}")

                while True:
                    new_username = input(
                        f"{color_green_bold}[-]{color_reset} Enter a unique username: ")
                    logging.info(f"User entered username as: {new_username}.")
                    status = self.checkMasterUser(new_username)

                    if not status:
                        new_password = getpass.getpass(
                            f"{color_green_bold}[-]{color_reset} Enter a new master password: ")
                        logging.info(f"User entered the password.")
                        confirm_password = getpass.getpass(
                            f"{color_green_bold}[-]{color_reset} Confirm master password: ")

                        if new_password != confirm_password:
                            print(
                                f"{color_red}[!] Passwords do not match. Please try again.{color_reset}")
                        else:
                            validationStatusOfPwd = validate_password(
                                new_password)

                            if (validationStatusOfPwd):
                                encryptedPassword = self.encPwd(new_password)
                                self.sqlConnectionMaster(
                                    new_username, encryptedPassword)
                                print(
                                    f"{color_green}[*]{color_reset} Your account is created!")
                                print(
                                    f"{color_blue}[*]{color_reset} Performing the necessary configurations!")
                                time.sleep(1.5)
                                print(
                                    f"{color_blue}[*]{color_reset} Done..\n")

                                while True:
                                    after_reg_input = input(
                                        f"{color_blue}[-]{color_reset} Do you want to login into your TITAN Account? [y/n]: ")

                                    if (after_reg_input == "y" or after_reg_input == "Y"):
                                        self.loginMenu()
                                    elif (after_reg_input == "n" or after_reg_input == "N"):
                                        self.MainMenu()
                                    else:
                                        print(
                                            f"{color_red_bold}[!]{color_reset} Please enter a proper value")
                    else:
                        print(
                            f"{color_yellow}[!] This username already exists. Try to be more creative.{color_reset}")
            except KeyboardInterrupt:
                self.MainMenu()

        def countdown(self, seconds):
            while seconds >= 0:
                minutes, sec = divmod(seconds, 60)
                timer = "\033[94m  Countdown: {:02d}:{:02d}\033[0m".format(
                    minutes, sec)
                sys.stdout.write("\r{}".format(timer))
                sys.stdout.flush()
                time.sleep(1)
                seconds -= 1

        def storePwdMenu(self, login_username):
            try:
                introBanner()
                print(
                    f"Welcome to the Password Storage Menu. This menu allows you to store your valuable passwords in a secure \ndatabase to be fetched later.\n")
                print(
                    f"{color_blue}[*] Store your passwords with us.{color_reset}\n")
                website = input(
                    f"  {color_blue}[-]{color_reset} Enter the name of the website (just the name): ")
                pwdToStore = getpass.getpass(
                    f"  {color_blue}[-]{color_reset} Enter the password to store: ")
                encryptedPwd = self.encPwdForPwdStorage(pwdToStore)
                status = self.sqlConnectionToStorePwd(
                    login_username, website, encryptedPwd)

                if status:
                    print(
                        f"  {color_green_bold}[*]{color_reset} Your password is successfully stored.")
                    time.sleep(1)
                    self.afterLoginVerificationMenu(login_username)

            except KeyboardInterrupt:
                self.afterLoginVerificationMenu(login_username)

        def retrievePwdMenu(self, username):
            try:
                introBanner()
                print(
                    f"Welcome to the Password Retrieval Menu. Here is a list of all the website of whose passwords you have\nstored with us.\n")

                storedWebSites = self.retrieveWebsiteFromDB(username)
                if storedWebSites is not None:
                    for i, item in enumerate(storedWebSites, start=1):
                        print(f"  {color_blue}{i}.{color_reset} {item[0]}  ")
                    print()
                    print(f" {color_blue}99.{color_reset} Go back a menu.\n")
                    while True:
                        web_choice = int(input(
                            f"{color_blue}[-]{color_reset} Enter your choice: "))

                        if web_choice == 99:
                            self.afterLoginVerificationMenu(self.username)

                        elif web_choice >= 1 and web_choice <= len(storedWebSites):
                            selected_website = storedWebSites[web_choice - 1][0]
                            password = self.retrievePwdFromDBPwd(
                                self.username, selected_website)
                            if password is not None:
                                print(
                                    f"{color_green}=>{color_reset} Password:{color_green} {password}{color_reset}")
                        else:
                            print(
                                f"{color_red}[!] Invalid input. Select a valid one.{color_reset}")
                else:
                    print(
                        f"{color_yellow}  No passwords were found. Start by storing a new password from the \"Store Password Menu\"{color_reset}\n")

            except KeyboardInterrupt:
                self.afterLoginVerificationMenu(username)

        def deletePwdMenu(self, username):
            try:
                self.username = username
                introBanner()
                print(
                    f"Welcome to the Password Deletion Menu. This menu will allow you to remove an inserted password\nfrom our database.\n")
                storedWebSites = self.retrieveWebsiteFromDB(self.username)
                if storedWebSites is None:
                    print(
                        f"{color_yellow}  No passwords were found. Start by storing a new password from the \"Store Password Menu\"{color_reset}\n")
                else:
                    for i, item in enumerate(storedWebSites, start=1):
                        print(f"  {color_blue}{i}.{color_reset} {item[0]}  ")
                    print()
                    print(f" {color_blue}99.{color_reset} Go back a menu.\n")
                    while True:
                        web_choice = int(input(
                            f"{color_blue}[-]{color_reset} Enter your choice: "))

                        if web_choice == 99:
                            self.afterLoginVerificationMenu(self.username)

                        elif web_choice >= 1 and web_choice <= len(storedWebSites):
                            selected_website = storedWebSites[web_choice - 1][0]
                            status_of_deletion = self.deletePwd(
                                self.username, selected_website)
                            if status_of_deletion:
                                print(
                                    f"{color_green}[*]{color_reset} Password deleted successfully.")
                        else:
                            print(
                                f"{color_red}[!] Invalid input. Select a valid one.{color_reset}")
            except KeyboardInterrupt:
                self.afterLoginVerificationMenu(username)

        def updatePwdMenu(self, username):
            try:
                introBanner()
                print(
                    f"Welcome to the password updation section of TITAN PASSWORD MANAGER\n")

                storedWebSites = self.retrieveWebsiteFromDB(username)
                if storedWebSites is not None:
                    for i, item in enumerate(storedWebSites, start=1):
                        print(f"  {color_blue}{i}.{color_reset} {item[0]}  ")
                    print()
                    print(f" {color_blue}99.{color_reset} Go back a menu.\n")
                    while True:
                        web_choice = int(input(
                            f"{color_blue}[-]{color_reset} Select one from the stored websites: "))

                        if web_choice == 99:
                            self.afterLoginVerificationMenu(self.username)

                        elif web_choice >= 1 and web_choice <= len(storedWebSites):
                            selected_website = storedWebSites[web_choice - 1][0]
                            dec_password = self.retrievePwdFromDBPwd(
                                self.username, selected_website)
                            if dec_password is not None:
                                while True:
                                    orig_pwd = getpass.getpass(
                                        f"{color_blue}[-]{color_reset} Enter the old Password for this website: ")
                                    if orig_pwd != dec_password:
                                        print(
                                            f"{color_red}[!] Passwords do not match. {color_reset}")
                                    else:
                                        new_pwd = getpass.getpass(
                                            f"{color_blue}[-]{color_reset} Enter new Password: ")
                                        re_new_pwd = getpass.getpass(
                                            f"{color_blue}[-]{color_reset} Re-enter new Password: ")

                                        if new_pwd == re_new_pwd:
                                            enc_pwd = self.encPwdForPwdStorage(
                                                new_pwd)
                                            status = self.update_WebPwd(
                                                username, enc_pwd, selected_website)
                                            if status:
                                                print(
                                                    f"{color_green}[*] Password updated successfully..")
                                                time.sleep(1)
                                                self.afterLoginVerificationMenu(
                                                    username)
                                            else:
                                                print(
                                                    f"{color_red}[!] error while updating the password{color_reset}")
                                        else:
                                            print(
                                                f"{color_yellow}[!] Passwords do not match. Please try again.{color_reset}")
                                else:
                                    pass
                            else:
                                print(
                                    f"{color_red}[!] Invalid input. Select a valid one.{color_reset}")
                        else:
                            print(
                                f"{color_yellow}  No passwords were found. Start by storing a new password from the \"Store Password Menu\"{color_reset}\n")
            except KeyboardInterrupt:
                self.afterLoginVerificationMenu(username)

        def genPwd(self, complexity):
            if complexity == "l":
                char = string.ascii_letters + string.digits + string.punctuation
                pwd = ''.join(random.choice(char) for _ in range(7))
                return pwd
            elif complexity == "m":
                char = string.ascii_letters + string.digits + string.punctuation
                pwd = ''.join(random.choice(char) for _ in range(10))
                return pwd
            if complexity == "h":
                char = string.ascii_letters + string.digits + string.punctuation
                pwd = ''.join(random.choice(char) for _ in range(16))
                return pwd

        def genPwdMenu(self, username):
            try:
                self.username = username
                introBanner()
                print("Welcome to the Password Generating menu. Here you'll be able to generate a password according\nto your preferences and TITAN will do its work for you.\n")
                complexity = input(
                    f"  {color_blue}[-]{color_reset} Complexity level (Low[l]/Medium[m]/High[h]): ")

                generatedPwd = self.genPwd(complexity)
                print(
                    f"\n{color_green}  [-]{color_reset} Generated Password: {generatedPwd}\n")
                print(
                    f"{color_red}[+]{color_reset} What do you want to do with this new password?:\n")
                print(
                    f"  {color_blue}1. {color_reset}Store this password for a new website. ")
                print(
                    f"  {color_blue}2. {color_reset}Update this password for an already existing website. ")
                print(
                    f"  {color_blue}3. {color_reset}Do nothing. I was just exploring.")

                while True:
                    choice_of_new_pwd = input("\nYour choice: ")

                    # will work afterwards on this one
                    if choice_of_new_pwd == "1":
                        print()
                        # while True:
                        try:
                            new_web = input(
                                f"{color_blue}  [-]{color_reset} Enter the name of the website: ")
                            enc_Pwd = self.encPwdForPwdStorage(generatedPwd)
                            if enc_Pwd:
                                status = self.sqlConnectionToStorePwd(
                                    username, new_web, enc_Pwd)
                                if status:
                                    print(
                                        f"{color_green}  [*] Password inserted successfully {color_reset}")
                                    time.sleep(1)
                                else:
                                    print(
                                        f"{color_red}  [!] Failed to insert the password{color_reset}")
                            else:
                                print(
                                    f"{color_red}  [!] Something's wrong..{color_reset}")
                        except Exception as e:
                            print(f"{color_red}[!] Program error: {e.message}")

                    elif choice_of_new_pwd == "2":
                        print()
                        enc_Pwd = self.encPwdForPwdStorage(generatedPwd)
                        records = self.retrieveWebsiteFromDB(username)
                        if records is not None:
                            for i, item in enumerate(records, start=1):
                                print(
                                    f"{color_blue}  {i}. {color_reset}{item[0]}")
                            print(
                                f"{color_blue}\n 99.{color_reset} Back to the previous menu\n")

                            web_choice = int(input("Enter your choice: "))
                            if web_choice == 99:
                                self.afterLoginVerification(username)
                            elif web_choice >= 1 and web_choice <= len(records):
                                selected_website = records[web_choice - 1][0]
                                status = self.update_WebPwd(
                                    username, enc_Pwd, selected_website)
                                if status:
                                    print(
                                        f"{color_green}  [-] Password updated for the website: {selected_website}{color_reset}")
                                    time.sleep(1)
                                    self.afterLoginVerificationMenu(username)
                                else:
                                    print(
                                        f"{color_red}  [!] Error occured while updating the password {color_reset}")
                                    time.sleep(1)
                        else:
                            print(
                                f"{color_red} [!] Something's wrong..{color_reset}")

                    elif choice_of_new_pwd == "3":
                        self.afterLoginVerificationMenu(username)

            except KeyboardInterrupt:
                self.afterLoginVerificationMenu(username)

        def loginMenu(self):
            try:
                introBanner()
                print(
                    f"{color_green}[+] Login with your Master Credentials{color_reset}\n")

                login_username = input(
                    f"{color_green_bold}  [-]{color_reset} Enter your username: ")

                i = 1
                while (i <= 4):
                    login_password = getpass.getpass(
                        f"{color_green_bold}  [-]{color_reset} Enter your master password: ")

                    decryptedPwd = self.checkMasterCredentials(
                        login_username, login_password)

                    if (i == 4):
                        print(
                            f"{color_red}  [!] 3 incorrect password attempts. Please wait for 40 seconds before trying again..!{color_reset}")
                        self.countdown(40)
                        self.loginMenu()

                    if decryptedPwd != login_password:
                        print(
                            f"{color_red}  [!]{color_reset} Passwords do not match. Please try again. (chance: {i})")
                        i = i + 1
                    else:
                        print(
                            f"{color_green_bold}  [*] Password accepted..!{color_reset}")
                        time.sleep(1)
                        self.afterLoginVerificationMenu(login_username)

            except KeyboardInterrupt:
                self.MainMenu()

        def afterLoginVerificationMenu(self, login_username):
            try:
                introBanner()
                print(
                    f"Welcome to the TITAN Password Manager: {color_green}{login_username}{color_reset}\n")
                print(
                    f"{color_blue_bold}[*]{color_reset} Select an option:\n")
                print(f"   {color_blue}1.{color_reset} Store a password.")
                print(
                    f"   {color_blue}2.{color_reset} Retrieve a password.")
                print(
                    f"   {color_blue}3.{color_reset} Delete an inserted password.")
                print(
                    f"   {color_blue}4.{color_reset} Update an inserted password.")
                print(
                    f"   {color_blue}5.{color_reset} Export passwords.")
                print(
                    f"   {color_blue}6.{color_reset} Import password.")
                print(
                    f"   {color_blue}7.{color_reset} Generate a strong password.")
                print(f"   {color_blue}8.{color_reset} Secure notes")
                print(
                    f"   {color_blue}9.{color_reset} Check password leaks")
                print(f"  {color_blue}10.{color_reset} Settings\n")
                print(f"  {color_blue}99.{color_reset} Logout.\n")
                while True:
                    choice = input(
                        f"{color_blue}{under}titan{color_reset}:{color_blue}{under}home{color_reset} > ")

                    if choice == "99":
                        print(
                            f"{color_green_bold}[-]{color_reset} Loggin you out.")
                        time.sleep(1)
                        self.MainMenu()
                    elif choice == "1":
                        self.storePwdMenu(login_username)
                    elif choice == "2":
                        self.retrievePwdMenu(login_username)
                    elif choice == "3":
                        self.deletePwdMenu(login_username)
                    elif choice == "4":
                        self.updatePwdMenu(login_username)
                    elif choice == "5":
                        print(
                            f"  {color_yellow}\n  This feature is under development.\n {color_reset}")
                        # self.export_pwd(login_username)
                    elif choice == "6":
                        print(
                            f"  {color_yellow}\n  This feature is under development.\n {color_reset}")
                        # self.import_pwd(login_username)
                    elif choice == "7":
                        self.genPwdMenu(login_username)
                    elif choice == "8":
                        sec_notes(login_username)
                    elif choice == "9":
                        check_pwned(login_username)
                    elif choice == "10":
                        self.settingMenu(login_username)
                    else:
                        print(
                            f"{color_red}[!] Provide a valid choice{color_reset}")

            except KeyboardInterrupt:
                choice = input(
                    f"{color_red}\n[!] Keyboard Interrupt detected. Do you want to logout of your account? [y/n]: {color_reset}")
                if choice.lower == 'y':
                    print(f"{color_green}[*] Logging you out{color_reset}")
                    time.sleep(1)
                    self.MainMenu()
                else:
                    self.afterLoginVerificationMenu(login_username)

        def settingMenu(self, username):
            try:
                self.username = username
                introBanner()
                print(
                    f"{color_blue}[*]{color_reset} Choose one from the following:\n")
                print(
                    f"  {color_blue}1.{color_reset} Change your master password")
                print(f"  {color_blue}2.{color_reset} Enable 2FA Authentication")
                print(f"  {color_blue}3.{color_reset} Deactivate your account\n")
                print(f" {color_blue}99.{color_reset} Go back to previous menu\n")

                while True:
                    choice = int(input(
                        f"{color_blue}{under}titan{color_reset}:{color_blue}{under}home{color_reset}:{color_blue}{under}settings{color_reset} > "))
                    if choice == 1:
                        self.chngMasterPwd(username)
                    elif choice == 2:
                        print(
                            f"{color_yellow}\n  This feature is under development.\n {color_reset}")
                        # enable2FA()
                    elif choice == 3:
                        self.delAccountMenu(self.username)
                    elif choice == 99:
                        self.afterLoginVerificationMenu(self.username)
                    else:
                        print(
                            f"{color_red}[!]{color_reset} Please enter a valid option.")

            except KeyboardInterrupt:
                self.afterLoginVerificationMenu(self.username)

        def chngMasterPwd(self, username):
            try:
                introBanner()
                print(f"Welcome to the Master Password Changing section.\n")
                orig_Mpwd = getpass.getpass(
                    f"{color_blue}[-]{color_reset} Please enter your current Master password: ")
                decrypted_pwd = self.checkMasterCredentials(
                    username, orig_Mpwd)
                if decrypted_pwd != orig_Mpwd:
                    print(
                        f"{color_red}[!] Incorrect password entered. Please try again.{color_reset}")
                else:
                    while True:
                        new_Mpwd = getpass.getpass(
                            f"{color_blue}[-]{color_reset} Enter your new Master Password: ")
                        confirm_new_Mpwd = getpass.getpass(
                            f"{color_blue}[-]{color_reset} Re-enter your new Master Password: ")

                        if (new_Mpwd != confirm_new_Mpwd):
                            print(
                                f"{color_red}[!] Passwords do not match. Please try again.{color_reset}")
                        else:
                            # retrieve master password
                            db_stored_password = self.retrieveMasterPwd(
                                username)
                            if db_stored_password == confirm_new_Mpwd:
                                print(
                                    f"{color_yellow_bold}[!]{color_reset} The new Master password cannot be same as the old one.")
                            else:
                                verified_pwd = validate_password(
                                    confirm_new_Mpwd)
                                if verified_pwd:
                                    encrypted_new_Mpwd = self.encPwd(new_Mpwd)
                                    status = self.update_Mpwd(
                                        username, encrypted_new_Mpwd)
                                    if status:
                                        print(
                                            f"\n{color_green}[-] Master Password changed successfully.{color_reset}")
                                        print(
                                            f"\n{color_green}[-]{color_reset} Kindly login again with your new credentials.")
                                        print(
                                            f"\n{color_green}[+]{color_reset} Redirecting to the Main Menu...")
                                        time.sleep(1)
                                        self.MainMenu()
                                    else:
                                        print(
                                            f"{color_red}[!] Error updating your master password.")
            except KeyboardInterrupt:
                self.settingMenu(username)

        def delAccountMenu(self, username):
            try:
                self.username = username
                introBanner()
                print(
                    f"{color_red}[!] Deleting your account can result in the loss of passwords. Kindly backup or export\nyour passwords so that the passwords are saved with you.{color_reset}\n")
                try:
                    while True:
                        confirm_Mpwd = getpass.getpass(
                            "  Confirm your Master Password: ")
                        decryptedPwd = self.checkMasterCredentials(
                            username, confirm_Mpwd)
                        if confirm_Mpwd == decryptedPwd:
                            status = self.delAccount(self.username)
                            if status:
                                print(
                                    f"{color_green}  [-] Your account deleted successfully...{color_reset}\n")
                                print(
                                    f"{color_blue}  [-] Redirecting you to the Main Menu.{color_reset}")
                                time.sleep(1)
                                self.MainMenu()
                            else:
                                print(
                                    f"{color_red}[!] Error while deleting your account.{color_reset}")
                                sys.exit()
                        else:
                            print(
                                f"{color_red}  [!] Passwords do not match! Enter your Master Password again to verify if its you.{color_reset}")
                except Exception as e:
                    print(e)
            except KeyboardInterrupt:
                self.settingMenu(username)

        def ArgumentParse(self):
            introBanner()

            # initializing argparser.
            parser = argparse.ArgumentParser(
                description="TITAN Password Manager help section.")
            parser.add_argument(
                "-a", "--action",
                help="action can contain either 'login' or 'register' parameters. ",
                type=str)

            parseArgs = parser.parse_args()

            if (parseArgs.action == "login" or parseArgs.action == "LOGIN"):
                self.loginMenu()

            elif (parseArgs.action == "register" or parseArgs.action == "REGISTER"):
                self.registrationMenu()

        def MainMenu(self):
            try:
                # checking the acceptance of user agreement
                checkUser()
                logging.info("Titan Password manager initialized.")
                introBanner()
                # self.platform_check()
                status = check_internet_connection()
                if status:
                    print(
                        f"{color_green}[*] Network connection deteted.{color_reset}\n")
                else:
                    print(
                        f"{color_red}[!] Network connection not detected. Some modules may not work properly{color_reset}\n")

                print(f"{color_blue_bold}[*] Select an option:{color_reset}\n")
                print(f"   {color_blue}1.{color_reset} Register an account")
                print(f"   {color_blue}2.{color_reset} Login Menu")
                print(f"   {color_blue}3.{color_reset} About/Usage\n")
                print(
                    f"  {color_blue}99.{color_reset} Exit the Titan Password Manager\n")

                while True:
                    option = input(f"{color_blue}{under}titan{color_reset} > ")

                    if option == '1':
                        self.registrationMenu()
                    elif option == '2':
                        self.loginMenu()
                    elif option == '3':
                        Manual()
                        input(
                            f"  Press {color_red}<enter>{color_reset} to continue")
                        if input:
                            self.MainMenu()
                    elif option == '99' or option == 'bye' or option == 'exit':
                        print(
                            f"\n Thank you for choosing and using {color_red}TITAN Password Manager{color_reset}.\n")
                        print(
                            f" Goodbye and stay secure! And remember, strong passwords unlock a {color_green}\"world of safety\"{color_reset}\n")
                        sys.exit(0)
                    else:
                        print(
                            f"{color_red}[!]{color_reset} Invalid option. Please select a valid one.")

            except KeyboardInterrupt:
                print(
                    f"\n\n Thank you for choosing and using {color_red}TITAN{color_reset} Password Manager.\n")
                print(
                    f" Goodbye, stay secure! And remember, strong passwords unlocks a {color_green}\"world of safety\"{color_reset}\n")
                sys.exit(0)

    if __name__ == '__main__':
        obj = PasswordManager()
        if len(sys.argv) >= 2:
            obj.ArgumentParse()
        obj.MainMenu()

except SyntaxError as s:
    print(s)
