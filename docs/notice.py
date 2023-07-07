color_red = '\033[91m'
color_red_bold = '\033[1;91m'
color_green = '\033[92m'
color_green_bold = '\033[1;92m'
color_yellow = '\033[93m'
color_yellow_bold = '\033[1;93m'
color_blue = '\033[94m'
color_blue_bold = '\033[1;94m'
color_reset = '\033[0m'


def display_terms():
    print(f"""

{color_blue}Copyright(c) 2023 - TITAN PASSWORD MANAGER (All rights reserved){color_reset}

By using this password manager command-line tool, you agree to the following:

1. This tool is provided as-is, without any warranties or guarantees. The author
   is not responsible for any damages or losses incurred while using this tool.

2. The tool is still under development and may contain bugs or security
   vulnerabilities. Use it at your own risk.

3. The tool uses encryption to store and retrieve passwords. However, no security
   mechanism is foolproof. It is your responsibility to keep your master password
   and system secure.

4. The tool may require access to your system's resources and may store sensitive
   data on your device. Make sure to review the code and understand its
   functionalities before using it.

5. The developer reserves the right to modify or update these terms and conditions
   at any time without prior notice. It is your responsibility to review the latest
   version of the terms.

{color_red}6. Use the tool responsibly and only for legitimate purposes. Do not use it for any
   illegal or unethical activities.{color_reset}

By using Titan Password Manager, you acknowledge that you have read, understood, and 
agreed to these terms and conditions.

   """)
