```plaintext
 _______ _______ _______ _______ _______ 
|_     _|_     _|_     _|   _   |    |  | [-] Welcome to the TITAN Password manager (v1.0) 
  |   |  _|   |_  |   | |       |       | [-] Written By: Kartik Iyer (founder of TaskOne)
  |___| |_______| |___| |___|___|__|____| [-] TITAN is the product of TaskOne  

```
    
# TITAN Password Manager

TITAN Password Manager is a command-line tool for securely managing your passwords. It allows you to store and retrieve passwords for various accounts, ensuring they are encrypted and protected.

## Features

- Securely stores passwords using encryption.
- Generates strong, random passwords.
- Retrieves passwords for specified accounts.
- Updates or deletes existing passwords.
- Simple and intuitive command-line interface.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/yourusername/titan-password-manager.git
Navigate to the project directory:


2. Change your directory to titan-password-manager
   
   ```shell
   cd Titan_password_manager

4. Install the required dependencies:
   
   ```shell
   pip install -r requirements.txt
   
6. Run the password manager:
   
   ```shell
   python titan_password_manager.py

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

## License
This project is licensed under the GNU License