```plaintext
 _______ _______ _______ _______ _______ 
|_     _|_     _|_     _|   _   |    |  | [-] Welcome to the TITAN Password manager (v1.0) 
  |   |  _|   |_  |   | |       |       | [-] Written By: Kartik Iyer
  |___| |_______| |___| |___|___|__|____| [-] TITAN is the product of TASK-1  

```
    
# Titan Password Manager

- TITAN stands for "Trusted Information and Technology Access Navigator".
- TITAN Password Manager is a command-line tool for securely managing your passwords. It allows you to store and retrieve passwords for various accounts, ensuring they are encrypted and protected.

## Features

- Securely stores passwords using encryption.
- Generates strong, random passwords.
- Retrieves passwords for specified accounts.
- Updates or deletes existing passwords.
- Simple and intuitive command-line interface.
- Provision of changing your Master Password.
- Provisions of deactivating your current using account.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/KartikIyerr/Titan_password_manager.git

2. Change your directory to Titan_password_manager
   
   ```shell
   cd Titan_password_manager

4. Install the required dependencies:
   
   ```shell
   pip install -r requirements.txt
   
6. Run the password manager:
   
   ```shell
   python tpm.py

## Usage

1. Help menu of Titan Password manager

    ```shell
    usage: tpm.py [-h] [-a ACTION]
    
    TITAN Password Manager help menu.
    
    options:
      -h, --help            show this help message and exit
      -a ACTION, --action ACTION
                            action can contain either 'login' or 'register' parameters. 
   
2. To make Titan Manager display a login menu, use the following command:
   
   ```shell
   python tpm.py --action login

3. To register your account with Titan, use the following command:

   ```shell
    python tpm.py --action register

## Main Menu Snippet
```plaintext
___________________________ _______  _
\__   __/\__   __/\__   __/(  ___  )( (    /|  
   ) (      ) (      ) (   | (   ) ||  \  ( |  
   | |      | |      | |   | (___) ||   \ | |  [-] Welcome to the TITAN Password manager (v1.0)    
   | |      | |      | |   |  ___  || (\ \) |  [-] Author: Kartik Iyer
   | |      | |      | |   | (   ) || | \   |  [-] TITAN is the product of TASK-1
   | |   ___) (___   | |   | )   ( || )  \  |
   )_(   \_______/   )_(   |/     \||/    )_)

Tip: Password managers are your allies in maintaining strong and secure passwords.

[-] Operating system detected: Windows

[*] Select an option:

   1. Register an account
   2. Login Menu
   3. About/Usage

  99. Exit TITAN Password Manager

[-] Enter your choice:

```

## License
- This project is licensed under the GNU License.
- The GNU License governs the usage, modification, and distribution of this project's source code and any derived works.
- By utilizing this project, you agree to abide by the terms and conditions set forth in the GNU License.
- The GNU License promotes the principles of free software, encouraging collaboration and sharing within the developer community.
- We appreciate your interest in this project and invite you to contribute in accordance with the guidelines outlined in the GNU License.
