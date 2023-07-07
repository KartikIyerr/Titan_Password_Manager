import os
import base64
import sqlite3
import csv

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

titan_code_dir = os.getcwd()
home_dir = os.path.expanduser("~")
titan_home = "TitanPwdManager"
config_folder = "TitanConfig"
comp_dir = os.path.join(home_dir, titan_home)
os.chdir(home_dir)
os.makedirs(comp_dir, exist_ok=True)
os.chdir(comp_dir)
os.makedirs(config_folder, exist_ok=True)


class DBConnectionProcedures:
    def sqlConnectionMaster(self, new_username, encryptedPassword):
        encoded_encryptedPwd = base64.b64encode(
            encryptedPassword).decode("utf-8")

        os.chdir(home_dir)
        db_folder = "TitanPwdManager"
        os.makedirs(db_folder, exist_ok=True)
        if os.path.exists(db_folder):
            os.chdir(db_folder)
            conn = sqlite3.connect("TitanDatabase")
            if conn:
                cursor = conn.cursor()
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS StoredMasterPwd (NAME varchar(220), DB_PWD varchar(220))")

                insert_data = cursor.execute(
                    f"INSERT INTO StoredMasterPwd VALUES ('{new_username}', '{encoded_encryptedPwd}')")

                cursor.connection.commit()
                conn.close()

            else:
                raise ConnectionError(
                    f"{color_red}[!]{color_reset} Could not connect to the database.")

        else:
            print(f"{color_red}[!]{color_reset} Error creating the folder")

    def sqlConnectionToStorePwd(self, username, website, webPwd):
        self.username = username
        self.website = website.capitalize()
        self.webPwd = webPwd
        enc_encryptedWebPwd = base64.b64encode(
            self.webPwd).decode("utf-8")
        os.chdir(home_dir)
        if os.path.isdir("TitanPwdManager"):
            os.chdir("TitanPwdManager")
            conn = sqlite3.connect("TitanDatabase")
            if conn:
                cursor = conn.cursor()
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS StoredWebPwd (Username VARCHAR(255) NOT NULL, webName VARCHAR(255) NOT NULL, webPwd VARCHAR(255) NOT NULL)")
                cursor.execute(
                    f"INSERT INTO StoredWebPwd (Username, webName, webPwd) VALUES('{self.username}','{self.website}', '{enc_encryptedWebPwd}')")
                cursor.connection.commit()
                conn.close()
                return True
            else:
                raise ConnectionError(
                    f"{color_red_bold}[!]{color_reset} Error connecting to the database.")
        else:
            print(f"{color_red_bold}[!]{color_reset} No directory exists.")

    def retrieveWebsiteFromDB(self, username):
        self.username = username
        os.chdir(home_dir)
        if os.path.isdir("TitanPwdManager"):
            os.chdir("TitanPwdManager")
            conn = sqlite3.connect("TitanDatabase")
            if conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(StoredWebPwd)")
                table_info = cursor.fetchall()

                if not table_info:
                    conn.close()
                    return None
                else:
                    cursor.execute(
                        f"SELECT webName FROM StoredWebPwd WHERE Username = '{username}'")
                    records = cursor.fetchall()
                    conn.commit()
                    record_list = []

                    for record in records:
                        record_list.append(record)
                    return record_list
            else:
                raise ConnectionError(
                    f"{color_red_bold}[!]{color_reset} Error connecting to the database.")
        else:
            print(f"{color_red_bold}[!]{color_reset} No directory exists.")

    def retrievePwdFromDBPwd(self, username, website):
        os.chdir(home_dir)
        if os.path.isdir("TitanPwdManager"):
            os.chdir("TitanPwdManager")
            conn = sqlite3.connect("TitanDatabase")
            if conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("PRAGMA table_info(StoredWebPwd)")
                    table_info = cursor.fetchall()

                    if not table_info:
                        conn.close()
                        return None
                    else:
                        query = f"SELECT webPwd FROM StoredWebPwd WHERE Username = '{username}' AND webName = '{website}'"
                        cursor.execute(query)
                        pwd_frm_db = cursor.fetchone()
                        if pwd_frm_db:
                            encrypted_pwd = base64.b64decode(pwd_frm_db[0])
                            decryptedPwd = self.decPwdForPwdRetrieval(
                                encrypted_pwd)
                            decryptedPwd = decryptedPwd.decode()
                            conn.commit()
                            cursor.connection.commit()
                            conn.close()
                            return decryptedPwd
                        else:
                            return None
                except Exception as e:
                    print(
                        f"An error occurred while retrieving the password: {str(e)}")
                    return None

            else:
                raise ConnectionError(
                    f"{color_red_bold}[!]{color_reset} Error connecting to the database.")
        else:
            print(f"{color_red_bold}[!]{color_reset} No directory exists.")

    def retrieveMasterPwd(self, username):
        os.chdir(home_dir)
        if os.path.isdir("TitanPwdManager"):
            os.chdir("TitanPwdManager")
            conn = sqlite3.connect("TitanDatabase")
            if conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(StoredMasterPwd)")
                table_info = cursor.fetchall()

                if not table_info:
                    conn.close()
                    return None
                else:
                    query = f"SELECT DB_PWD FROM StoredMasterPwd WHERE NAME = '{username}'"
                    cursor.execute(query)
                    pwd_frm_db = cursor.fetchone()
                    encrypted_pwd = base64.b64decode(pwd_frm_db[0])
                    decryptedPwd = self.decPwd(
                        encrypted_pwd)
                    decryptedPwd = decryptedPwd.decode('utf-8')
                    conn.commit()
                    cursor.connection.commit()
                    conn.close()
                    return decryptedPwd
            else:
                raise ConnectionError(
                    f"{color_red_bold}[!]{color_reset} Error connecting to the database.")
        else:
            print(f"{color_red_bold}[!]{color_reset} No directory exists.")

    def checkMasterUser(self, username):
        os.chdir(home_dir)
        if os.path.isdir("TitanPwdManager"):
            os.chdir("TitanPwdManager")
            conn = sqlite3.connect("TitanDatabase")
            if conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(StoredMasterPwd)")
                table_info = cursor.fetchall()

                if not table_info:
                    conn.close()
                    return None
                else:
                    query = f"SELECT NAME FROM StoredMasterPwd WHERE NAME = '{username}'"
                    cursor.execute(query)
                    result = cursor.fetchone()
                    conn.close()

                    if result:
                        return True
                    else:
                        return False

    def deletePwd(self, username, website):
        os.chdir(home_dir)
        if os.path.isdir("TitanPwdManager"):
            os.chdir("TitanPwdManager")
            conn = sqlite3.connect("TitanDatabase")
            if conn:
                cursor = conn.cursor()
                query = f"DELETE FROM StoredWebPwd WHERE Username = ? AND webName = ?"
                status = cursor.execute(query, [username, website])
                if cursor.rowcount > 0:
                    conn.commit()
                    return True
                else:
                    return False
            else:
                raise ConnectionError(
                    f"{color_red_bold}[!]{color_reset} Error connecting to the database.")
        else:
            print(f"{color_red_bold}[!]{color_reset} No directory exists.")

    def update_Mpwd(self, username, new_Mpassword):
        encoded_encryptedMPwd = base64.b64encode(
            new_Mpassword).decode("utf-8")
        os.chdir(home_dir)
        if os.path.isdir("TitanPwdManager"):
            os.chdir("TitanPwdManager")
            conn = sqlite3.connect("TitanDatabase")
            if conn:
                cursor = conn.cursor()
                query = f"UPDATE StoredMasterPwd SET DB_PWD = '{encoded_encryptedMPwd}' WHERE NAME = '{username}'"
                cursor.execute(query)
                if cursor.rowcount > 0:
                    conn.commit()
                    conn.close()
                    return True
                else:
                    conn.close()
                    return False
            else:
                raise ConnectionError(
                    f"{color_red_bold}[!]{color_reset} Error connecting to the database.")
        else:
            print(f"{color_red_bold}[!]{color_reset} No directory exists.")

    def update_WebPwd(self, username, new_Webpassword, website):
        encoded_encryptedWebPwd = base64.b64encode(
            new_Webpassword).decode("utf-8")
        os.chdir(home_dir)
        if os.path.isdir("TitanPwdManager"):
            os.chdir("TitanPwdManager")
            conn = sqlite3.connect("TitanDatabase")
            if conn:
                cursor = conn.cursor()
                query = f"UPDATE StoredWebPwd SET webPwd = '{encoded_encryptedWebPwd}' WHERE Username = '{username}' AND webName = '{website}'"
                cursor.execute(query)
                if cursor.rowcount > 0:
                    conn.commit()
                    conn.close()
                    return True
                else:
                    conn.close()
                    return False
            else:
                raise ConnectionError(
                    f"{color_red_bold}[!]{color_reset} Error connecting to the database.")
        else:
            print(f"{color_red_bold}[!]{color_reset} No directory exists.")

    def delAccount(self, username):
        self.username = username
        os.chdir(home_dir)
        if os.path.isdir("TitanPwdManager"):
            os.chdir("TitanPwdManager")
            conn = sqlite3.connect("TitanDatabase")
            if conn:
                cursor = conn.cursor()
                query = f"DELETE FROM StoredMasterPwd WHERE NAME = '{self.username}'"
                cursor.execute(query)
                if cursor.rowcount > 0:
                    conn.commit()
                    return True
                else:
                    return False
            else:
                print(
                    f"{color_red}[!] Error connecting to the database.{color_reset}")
        else:
            print(f"{color_red_bold}[!]{color_reset} No directory exists.")

    def export_pwd(self, username):
        os.chdir(home_dir)
        if os.path.isdir("TitanPwdManager"):
            os.chdir("TitanPwdManager")
            conn = sqlite3.connect("TitanDatabase")
            if conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(StoredWebPwd)")
                table_info = cursor.fetchall()

                if not table_info:
                    conn.close()
                    return None
                else:
                    query = f"SELECT webName, webPwd FROM StoredWebPwd WHERE Username = '{username}'"
                    cursor.execute(query)
                    pwd_rows = cursor.fetchall()

                    # Write the passwords to a CSV file
                    with open('passwords.csv', 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        # Write header row
                        writer.writerow(['Website', 'Password'])
                        for pwd_row in pwd_rows:
                            website_name = pwd_row[0]
                            encrypted_pwd = pwd_row[1].encode('utf-8')
                            print(encrypted_pwd)
                            decrypted_pwd = self.decPwdForPwdRetrieval(
                                encrypted_pwd)
                            decrypted_pwd = decrypted_pwd.decode('utf-8')
                            writer.writerow([website_name, decrypted_pwd])

                    conn.commit()
                    cursor.connection.commit()
                    conn.close()
                    return None
            else:
                raise ConnectionError(
                    f"{color_red_bold}[!]{color_reset} Error connecting to the database.")
        else:
            print(f"{color_red_bold}[!]{color_reset} No directory exists.")
