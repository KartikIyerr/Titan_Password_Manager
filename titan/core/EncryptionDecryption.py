import os
from cryptography.fernet import Fernet
import pickle
import base64


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


class EncryptionDecryption:
    def __init__(self):
        self.cipher = None  # Initializing cipher attribute

    def genKey(self):
        os.chdir(home_dir)
        db_folder = "TitanPwdManager"
        os.makedirs(db_folder, exist_ok=True)
        os.chdir(db_folder)
        key = Fernet.generate_key()
        serialized_cipher = pickle.dumps(key)
        with open("MasterKey", "wb") as f:
            f.write(serialized_cipher)
            f.close()

    def encPwd(self, password):
        os.chdir(home_dir)
        db_folder = "TitanPwdManager"
        os.makedirs(db_folder, exist_ok=True)
        os.chdir(db_folder)
        if not os.path.isfile("MasterKey"):
            self.genKey()

        with open("MasterKey", "rb") as f:
            key = f.read()
            deserialized_key = pickle.loads(key)
            cipher = Fernet(deserialized_key)

        enc_pwd = cipher.encrypt(password.encode())
        return enc_pwd

    def decPwd(self, password):
        os.chdir(home_dir)
        db_folder = "TitanPwdManager"
        os.makedirs(db_folder, exist_ok=True)
        os.chdir(db_folder)
        # self.genKey()
        # if cipher is None:
        #     raise ValueError(
        #         "Cipher not initialized. Call encPwd method first.")

        with open("MasterKey", "rb") as f:
            key = f.read()
            deserialized_key = pickle.loads(key)
            cipher = Fernet(deserialized_key)

        dec_pwd = cipher.decrypt(password.decode())
        return dec_pwd

    def genKeyForPwdStorage(self):
        os.chdir(home_dir)
        db_folder = "TitanPwdManager"
        os.makedirs(db_folder, exist_ok=True)
        os.chdir(db_folder)
        key = Fernet.generate_key()
        encoded_key = base64.urlsafe_b64encode(key).decode()
        with open("PwdStoreKey", "w") as f:
            f.write(encoded_key)

    def encPwdForPwdStorage(self, password):
        os.chdir(home_dir)
        db_folder = "TitanPwdManager"
        os.makedirs(db_folder, exist_ok=True)
        os.chdir(db_folder)
        if not os.path.isfile("PwdStoreKey"):
            self.genKeyForPwdStorage()

        with open("PwdStoreKey", "r") as f:
            encoded_key = f.read()
            key = base64.urlsafe_b64decode(encoded_key)
            cipher = Fernet(key)
        enc_pwd = cipher.encrypt(password.encode())
        return enc_pwd

    def decPwdForPwdRetrieval(self, password):
        os.chdir(home_dir)
        db_folder = "TitanPwdManager"
        os.makedirs(db_folder, exist_ok=True)
        os.chdir(db_folder)
        with open("PwdStoreKey", "r") as f:
            encoded_key = f.read()
            key = base64.urlsafe_b64decode(encoded_key)
            cipher = Fernet(key)
        dec_pwd = cipher.decrypt(password)
        return dec_pwd
