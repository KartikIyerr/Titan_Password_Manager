#!/usr/bin/env python

#########################################################################################
#                                                                                       #
#   Titan Password Manager - Secure and Easy-to-Use Password Management Solution        #
#                                                                                       #
#   COPYRIGHT (c) 2023 - All Rights Reserved                                            #
#                                                                                       #
#   Author: Kartik Iyer                                                                 #
#   License: This product is licensed under the terms of the GNU Public License.        #
#   Github: www.github.com/KartikIyerr/Titan_Password_Manager                           #
#                                                                                       #
#   WARNING: DO NOT MODIFY THIS CODE UNLESS YOU FULLY UNDERSTAND ITS FUNCTIONALITY.     #
#            MAKING CHANGES WITHOUT PROPER KNOWLEDGE CAN COMPROMISE                     #
#            THE SECURITY AND FUNCTIONALITY OF THE PASSWORD MANAGER.                    #
#                                                                                       #
#########################################################################################


import sys              # for checking platform and arguments
import os               # for the file manipulations
import getpass          # for getting user passwords
import sqlite3          # for database functionalities
import time             # for measuring time
import base64           # for the base64 encoding/decoding functions
import argparse         # for parsing arguments
import random           # for generating random passwords
import string           # for generating a string of ascii characters and numbers
import logging          # for maintaining logs
import pyperclip        # for copying the passwords to the clipboard

sys.dont_write_bytecode = True

####################
# GLOBAL VARIABLES #
####################

# color codes
R = '\033[91m'
RB = '\033[1;91m'
G = '\033[92m'
GB = '\033[1;92m'
Y = '\033[93m'
YB = '\033[1;93m'
B = '\033[94m'
BB = '\033[1;94m'
UN = '\033[4m'
CR = '\033[0m'

titan_code_dir = os.getcwd()
home_dir = os.path.expanduser("~")
titan_home = "TitanPwdManager"
config_folder = "TitanConfig"
comp_dir = os.path.join(home_dir, titan_home)
os.chdir(home_dir)
os.makedirs(comp_dir, exist_ok=True)
os.chdir(comp_dir)
os.makedirs(config_folder, exist_ok=True)


###############################
# Importing dependent modules #
###############################

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
    print(f"{R}[!]{CR} Error importing the packages. {i}")
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


#############
# MAIN CODE #
#############

try:
    class PasswordManager(EncryptionDecryption, DBConnectionProcedures):
        def __init__(self):
            self.cipher = None
            logging.basicConfig(filename="titan.log",
                                level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        def platform_check(self):
            # checking the platform
            if (sys.platform == 'win32'):
                print(
                    f"{RB}[-]{CR} Operating system detected: Windows \n")
                logging.info("Operating System detected: Windows.")
            elif (sys.platform == 'linux'):
                print(
                    f"{RB}[-]{CR} Operating system detected: Linux ")

                # checking for root
                if os.geteuid() != 0:
                    print(
                        f"\n  TITAN Password Manager - By Kartik Iyer")
                    print(
                        f"  Not running as {R}root{CR}. Exiting the TITAN Password Manager.\n")
                    sys.exit()
            else:
                print(
                    f"  {RB}[!]{CR} This tool does not support your device.")

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
                                f"{Y}  [!] Are you a new user? Maybe you should register with us!{CR}")
                            while True:
                                user_choice = input(
                                    f"{BB}  [-]{CR} Can I take you to the Registration process? (y/n): ")
                                if user_choice == "y" or user_choice == "Y":

                                    self.registrationMenu()
                                elif user_choice == "n" or user_choice == "N":
                                    introBanner()
                                    self.MainMenu()
                                else:
                                    raise ValueError(
                                        f"{R}[!]{CR} Enter a proper value")
                    else:
                        print(
                            f"{R}[!] Problem connecting with the database.")
                else:
                    print(
                        f"{R}  [!]{CR} No database initialized. Maybe you have not yet registered with us...")
                    sys.exit(0)
            except Exception as e:
                print(
                    f"{Y}  [!] Are you a new user? Maybe you should register with us!{CR}")
                time.sleep(1)
                self.MainMenu()

        def registrationMenu(self):
            try:
                introBanner()
                logging.info("User selected registration menu.")
                print(f"Welcome to the Registration section of Titan Password manager. Create your new vault\nby providing us the required information and be sure to keep the master password SAFE.\n")
                print(
                    f"{R}Warning:{CR} Master password is non-recoverable. Please keep it in a safe place.\n")
                print(
                    f"{GB}[+] Create Master Credentials{CR}")

                while True:
                    new_username = input(
                        f"{GB}[-]{CR} Enter a unique username: ")
                    logging.info(f"User entered username as: {new_username}.")
                    status = self.checkMasterUser(new_username)

                    if not status:
                        new_password = getpass.getpass(
                            f"{GB}[-]{CR} Enter a new master password: ")
                        logging.info(f"User entered the password.")
                        confirm_password = getpass.getpass(
                            f"{GB}[-]{CR} Confirm master password: ")

                        if new_password != confirm_password:
                            print(
                                f"{R}[!] Passwords do not match. Please try again.{CR}")
                        else:
                            validationStatusOfPwd = validate_password(
                                new_password)

                            if (validationStatusOfPwd):
                                encryptedPassword = self.encPwd(new_password)
                                self.sqlConnectionMaster(
                                    new_username, encryptedPassword)
                                print(
                                    f"{G}[*]{CR} Your account is created!")
                                print(
                                    f"{B}[*]{CR} Performing the necessary configurations!")
                                time.sleep(1.5)
                                print(
                                    f"{B}[*]{CR} Done..\n")

                                while True:
                                    after_reg_input = input(
                                        f"{B}[-]{CR} Do you want to login into your TITAN Account? [y/n]: ")

                                    if (after_reg_input == "y" or after_reg_input == "Y"):
                                        self.loginMenu()
                                    elif (after_reg_input == "n" or after_reg_input == "N"):
                                        self.MainMenu()
                                    else:
                                        print(
                                            f"{RB}[!]{CR} Please enter a proper value")
                    else:
                        print(
                            f"{Y}[!] This username already exists. Try to be more creative.{CR}")
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
                    f"{B}[*] Store your passwords with us.{CR}\n")
                website = input(
                    f"  {B}[-]{CR} Enter the name of the website (just the name): ")
                pwdToStore = getpass.getpass(
                    f"  {B}[-]{CR} Enter the password to store: ")
                encryptedPwd = self.encPwdForPwdStorage(pwdToStore)
                status = self.sqlConnectionToStorePwd(
                    login_username, website, encryptedPwd)

                if status:
                    print(
                        f"  {GB}[*]{CR} Your password is successfully stored.")
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
                        print(f"  {B}{i}.{CR} {item[0]}  ")
                    print()
                    print(f" {B}99.{CR} Go back a menu.\n")
                    while True:
                        web_choice = int(input(
                            f"{B}[-]{CR} Enter your choice: "))

                        if web_choice == 99:
                            self.afterLoginVerificationMenu(self.username)

                        elif web_choice >= 1 and web_choice <= len(storedWebSites):
                            selected_website = storedWebSites[web_choice - 1][0]
                            password = self.retrievePwdFromDBPwd(
                                self.username, selected_website)
                            if password is not None:
                                print(
                                    f"{G}=>{CR} Password:{G} {password}{CR}")
                        else:
                            print(
                                f"{R}[!] Invalid input. Select a valid one.{CR}")
                else:
                    print(
                        f"{Y}  No passwords were found. Start by storing a new password from the \"Store Password Menu\"{CR}\n")

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
                        f"{Y}  No passwords were found. Start by storing a new password from the \"Store Password Menu\"{CR}\n")
                else:
                    for i, item in enumerate(storedWebSites, start=1):
                        print(f"  {B}{i}.{CR} {item[0]}  ")
                    print()
                    print(f" {B}99.{CR} Go back a menu.\n")
                    while True:
                        web_choice = int(input(
                            f"{B}[-]{CR} Enter your choice: "))

                        if web_choice == 99:
                            self.afterLoginVerificationMenu(self.username)

                        elif web_choice >= 1 and web_choice <= len(storedWebSites):
                            selected_website = storedWebSites[web_choice - 1][0]
                            status_of_deletion = self.deletePwd(
                                self.username, selected_website)
                            if status_of_deletion:
                                print(
                                    f"{G}[*]{CR} Password deleted successfully.")
                        else:
                            print(
                                f"{R}[!] Invalid input. Select a valid one.{CR}")
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
                        print(f"  {B}{i}.{CR} {item[0]}  ")
                    print()
                    print(f" {B}99.{CR} Go back a menu.\n")
                    while True:
                        web_choice = int(input(
                            f"{B}[-]{CR} Select one from the stored websites: "))

                        if web_choice == 99:
                            self.afterLoginVerificationMenu(self.username)

                        elif web_choice >= 1 and web_choice <= len(storedWebSites):
                            selected_website = storedWebSites[web_choice - 1][0]
                            dec_password = self.retrievePwdFromDBPwd(
                                self.username, selected_website)
                            if dec_password is not None:
                                while True:
                                    orig_pwd = getpass.getpass(
                                        f"{B}[-]{CR} Enter the old Password for this website: ")
                                    if orig_pwd != dec_password:
                                        print(
                                            f"{R}[!] Passwords do not match. {CR}")
                                    else:
                                        new_pwd = getpass.getpass(
                                            f"{B}[-]{CR} Enter new Password: ")
                                        re_new_pwd = getpass.getpass(
                                            f"{B}[-]{CR} Re-enter new Password: ")

                                        if new_pwd == re_new_pwd:
                                            enc_pwd = self.encPwdForPwdStorage(
                                                new_pwd)
                                            status = self.update_WebPwd(
                                                username, enc_pwd, selected_website)
                                            if status:
                                                print(
                                                    f"{G}[*] Password updated successfully..")
                                                time.sleep(1)
                                                self.afterLoginVerificationMenu(
                                                    username)
                                            else:
                                                print(
                                                    f"{R}[!] error while updating the password{CR}")
                                        else:
                                            print(
                                                f"{Y}[!] Passwords do not match. Please try again.{CR}")
                                else:
                                    pass
                            else:
                                print(
                                    f"{R}[!] Invalid input. Select a valid one.{CR}")
                        else:
                            print(
                                f"{Y}  No passwords were found. Start by storing a new password from the \"Store Password Menu\"{CR}\n")
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
                    f"  {B}[-]{CR} Complexity level (Low[l]/Medium[m]/High[h]): ")

                generatedPwd = self.genPwd(complexity)
                print(
                    f"\n{G}  [-]{CR} Generated Password: {generatedPwd}")
                pyperclip.copy(generatedPwd)
                print(
                    f"{Y}  [Password is also copied to clipboard]{CR}\n")
                print(
                    f"{R}[+]{CR} What do you want to do with this new password?:\n")
                print(
                    f"  {B}1. {CR}Store this password for a new website. ")
                print(
                    f"  {B}2. {CR}Update this password for an already existing website. ")
                print(
                    f"  {B}3. {CR}Do nothing. I was just exploring.")

                while True:
                    choice_of_new_pwd = input("\nYour choice: ")

                    # will work afterwards on this one
                    if choice_of_new_pwd == "1":
                        print()
                        # while True:
                        try:
                            new_web = input(
                                f"{B}  [-]{CR} Enter the name of the website: ")
                            enc_Pwd = self.encPwdForPwdStorage(generatedPwd)
                            if enc_Pwd:
                                status = self.sqlConnectionToStorePwd(
                                    username, new_web, enc_Pwd)
                                if status:
                                    print(
                                        f"{G}  [*] Password inserted successfully {CR}")
                                    time.sleep(1)
                                else:
                                    print(
                                        f"{R}  [!] Failed to insert the password{CR}")
                            else:
                                print(
                                    f"{R}  [!] Something's wrong..{CR}")
                        except Exception as e:
                            print(f"{R}[!] Program error: {e.message}")

                    elif choice_of_new_pwd == "2":
                        print()
                        enc_Pwd = self.encPwdForPwdStorage(generatedPwd)
                        records = self.retrieveWebsiteFromDB(username)
                        if records is not None:
                            for i, item in enumerate(records, start=1):
                                print(
                                    f"{B}  {i}. {CR}{item[0]}")
                            print(
                                f"{B}\n 99.{CR} Back to the previous menu\n")

                            web_choice = int(input("Enter your choice: "))
                            if web_choice == 99:
                                self.afterLoginVerification(username)
                            elif web_choice >= 1 and web_choice <= len(records):
                                selected_website = records[web_choice - 1][0]
                                status = self.update_WebPwd(
                                    username, enc_Pwd, selected_website)
                                if status:
                                    print(
                                        f"{G}  [-] Password updated for the website: {selected_website}{CR}")
                                    time.sleep(1)
                                    self.afterLoginVerificationMenu(username)
                                else:
                                    print(
                                        f"{R}  [!] Error occured while updating the password {CR}")
                                    time.sleep(1)
                        else:
                            print(
                                f"{R} [!] Something's wrong..{CR}")

                    elif choice_of_new_pwd == "3":
                        self.afterLoginVerificationMenu(username)

            except KeyboardInterrupt:
                self.afterLoginVerificationMenu(username)

        def loginMenu(self):
            try:
                introBanner()
                print(
                    f"{G}[+] Login with your Master Credentials{CR}\n")

                login_username = input(
                    f"{GB}  [-]{CR} Enter your username: ")

                i = 1
                while (i <= 4):
                    login_password = getpass.getpass(
                        f"{GB}  [-]{CR} Enter your master password: ")

                    decryptedPwd = self.checkMasterCredentials(
                        login_username, login_password)

                    if (i == 4):
                        print(
                            f"{R}  [!] 3 incorrect password attempts. Please wait for 40 seconds before trying again..!{CR}")
                        self.countdown(40)
                        self.loginMenu()

                    if decryptedPwd != login_password:
                        print(
                            f"{R}  [!]{CR} Passwords do not match. Please try again. (chance: {i})")
                        i = i + 1
                    else:
                        print(
                            f"{GB}  [*] Password accepted..!{CR}")
                        time.sleep(1)
                        self.afterLoginVerificationMenu(login_username)

            except KeyboardInterrupt:
                self.MainMenu()

        def afterLoginVerificationMenu(self, login_username):
            try:
                introBanner()
                print(
                    f"Welcome to the TITAN Password Manager: {G}{login_username}{CR}\n")
                print(
                    f"{BB}[*]{CR} Select an option:\n")
                print(f"   {B}1.{CR} Store a password.")
                print(
                    f"   {B}2.{CR} Retrieve a password.")
                print(
                    f"   {B}3.{CR} Delete an inserted password.")
                print(
                    f"   {B}4.{CR} Update an inserted password.")
                print(
                    f"   {B}5.{CR} Export passwords.")
                print(
                    f"   {B}6.{CR} Import password.")
                print(
                    f"   {B}7.{CR} Generate a strong password.")
                print(f"   {B}8.{CR} Secure notes")
                print(
                    f"   {B}9.{CR} Check password leaks")
                print(f"  {B}10.{CR} Settings\n")
                print(f"  {B}99.{CR} Logout.\n")
                while True:
                    choice = input(
                        f"{B}{UN}titan{CR}:{B}{UN}home{CR} > ")

                    if choice == "99":
                        print(
                            f"{GB}[-]{CR} Loggin you out.")
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
                            f"  {Y}\n  This feature is UN development.\n {CR}")
                        # self.export_pwd(login_username)
                    elif choice == "6":
                        print(
                            f"  {Y}\n  This feature is UN development.\n {CR}")
                        # self.import_pwd(login_username)
                    elif choice == "7":
                        self.genPwdMenu(login_username)
                    elif choice == "8":
                        sec_notes(login_username)
                    elif choice == "9":
                        status = check_pwned(login_username)
                        if not status:
                            print(
                                f"{R}[!] You are not connected to the internet. Exiting.\n")
                        time.sleep(1)
                        self.afterLoginVerificationMenu(login_username)
                    elif choice == "10":
                        self.settingMenu(login_username)
                    else:
                        print(
                            f"{R}[!] Provide a valid choice{CR}")

            except KeyboardInterrupt:
                choice = input(
                    f"{R}\n[!] Keyboard Interrupt detected. Do you want to logout of your account? [y/n]: {CR}")
                if choice.lower == 'y':
                    print(f"{G}[*] Logging you out{CR}")
                    time.sleep(1)
                    self.MainMenu()
                else:
                    self.afterLoginVerificationMenu(login_username)

        def settingMenu(self, username):
            try:
                self.username = username
                introBanner()
                print(
                    f"{B}[*]{CR} Choose one from the following:\n")
                print(
                    f"  {B}1.{CR} Change your master password")
                print(f"  {B}2.{CR} Enable 2FA Authentication")
                print(f"  {B}3.{CR} Deactivate your account\n")
                print(f" {B}99.{CR} Go back to previous menu\n")

                while True:
                    choice = int(input(
                        f"{B}{UN}titan{CR}:{B}{UN}home{CR}:{B}{UN}settings{CR} > "))
                    if choice == 1:
                        self.chngMasterPwd(username)
                    elif choice == 2:
                        print(
                            f"{Y}\n  This feature is UN development.\n {CR}")
                        # enable2FA()
                    elif choice == 3:
                        self.delAccountMenu(self.username)
                    elif choice == 99:
                        self.afterLoginVerificationMenu(self.username)
                    else:
                        print(
                            f"{R}[!]{CR} Please enter a valid option.")

            except KeyboardInterrupt:
                self.afterLoginVerificationMenu(self.username)

        def chngMasterPwd(self, username):
            try:
                introBanner()
                print(f"Welcome to the Master Password Changing section.\n")
                orig_Mpwd = getpass.getpass(
                    f"{B}[-]{CR} Please enter your current Master password: ")
                decrypted_pwd = self.checkMasterCredentials(
                    username, orig_Mpwd)
                if decrypted_pwd != orig_Mpwd:
                    print(
                        f"{R}[!] Incorrect password entered. Please try again.{CR}")
                else:
                    while True:
                        new_Mpwd = getpass.getpass(
                            f"{B}[-]{CR} Enter your new Master Password: ")
                        confirm_new_Mpwd = getpass.getpass(
                            f"{B}[-]{CR} Re-enter your new Master Password: ")

                        if (new_Mpwd != confirm_new_Mpwd):
                            print(
                                f"{R}[!] Passwords do not match. Please try again.{CR}")
                        else:
                            # retrieve master password
                            db_stored_password = self.retrieveMasterPwd(
                                username)
                            if db_stored_password == confirm_new_Mpwd:
                                print(
                                    f"{YB}[!]{CR} The new Master password cannot be same as the old one.")
                            else:
                                verified_pwd = validate_password(
                                    confirm_new_Mpwd)
                                if verified_pwd:
                                    encrypted_new_Mpwd = self.encPwd(new_Mpwd)
                                    status = self.update_Mpwd(
                                        username, encrypted_new_Mpwd)
                                    if status:
                                        print(
                                            f"\n{G}[-] Master Password changed successfully.{CR}")
                                        print(
                                            f"\n{G}[-]{CR} Kindly login again with your new credentials.")
                                        print(
                                            f"\n{G}[+]{CR} Redirecting to the Main Menu...")
                                        time.sleep(1)
                                        self.MainMenu()
                                    else:
                                        print(
                                            f"{R}[!] Error updating your master password.")
            except KeyboardInterrupt:
                self.settingMenu(username)

        def delAccountMenu(self, username):
            try:
                self.username = username
                introBanner()
                print(
                    f"{R}[!] Deleting your account can result in the loss of passwords. Kindly backup or export\nyour passwords so that the passwords are saved with you.{CR}\n")
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
                                    f"{G}  [-] Your account deleted successfully...{CR}\n")
                                print(
                                    f"{B}  [-] Redirecting you to the Main Menu.{CR}")
                                time.sleep(1)
                                self.MainMenu()
                            else:
                                print(
                                    f"{R}[!] Error while deleting your account.{CR}")
                                sys.exit()
                        else:
                            print(
                                f"{R}  [!] Passwords do not match! Enter your Master Password again to verify if its you.{CR}")
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
                type=str
            )
            # parser.add_argument(
            #     "-u", "--username",
            #     help="Enter username to login",
            #     type=str
            # )
            # parser.add_argument(
            #     "-p", "--password",
            #     help="Enter password to login"
            # )

            parseArgs = parser.parse_args()

            if parseArgs.action == "login" or parseArgs.action == "LOGIN":
                self.loginMenu()

            elif parseArgs.action == "register" or parseArgs.action == "REGISTER":
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
                        f"{G}[*] Network connection deteted.{CR}\n")
                else:
                    print(
                        f"{R}[!]{CR} Network connection not detected.\n")
                tip = tips()
                print(f"{Y}Tip: {tip}{CR}\n")

                print(f"{BB}[*] Select an option:{CR}\n")
                print(f"   {B}1.{CR} Register an account")
                print(f"   {B}2.{CR} Login Menu")
                print(f"   {B}3.{CR} About/Usage\n")
                print(
                    f"  {B}99.{CR} Exit the Titan Password Manager\n")

                while True:
                    option = input(f"{B}{UN}titan{CR} > ")

                    if option == '1':
                        self.registrationMenu()
                    elif option == '2':
                        self.loginMenu()
                    elif option == '3':
                        Manual()
                        input(
                            f"  Press {R}<enter>{CR} to continue")
                        if input:
                            self.MainMenu()
                    elif option == '99' or option == 'bye' or option == 'exit':
                        print(
                            f"\n Thank you for choosing and using {R}TITAN Password Manager{CR}.\n")
                        print(
                            f" Goodbye and stay secure! And remember, strong passwords unlock a {G}\"world of safety\"{CR}\n")
                        sys.exit(0)
                    else:
                        print(
                            f"{R}[!]{CR} Invalid option. Please select a valid one.")

            except KeyboardInterrupt:
                print(
                    f"\n\n Thank you for choosing and using {R}TITAN{CR} Password Manager.\n")
                print(
                    f" Goodbye, stay secure! And remember, strong passwords unlocks a {G}\"world of safety\"{CR}\n")
                sys.exit(0)

    if __name__ == '__main__':
        obj = PasswordManager()
        if len(sys.argv) >= 2:
            obj.ArgumentParse()
        obj.MainMenu()

except SyntaxError as s:
    print(s)
