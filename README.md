# emailextractor
Email Extractor Script

This is a Python script that allows you to extract emails from email accounts and display them on a GUI (Graphical User Interface). The script uses the IMAP protocol to connect to an email server and extract emails.

Prerequisites

Before using the script, you will need to have the following:

Python 3 installed on your computer
An email account with IMAP access enabled
Installation

Clone the repository to your local machine:
bash

git clone https://github.com/gLiNtAlpHa/emailextractor.git
Navigate to the project directory:
bash

cd email-extractor
Install the required packages:
bash

pip install -r requirements.txt
Usage

Open the email_extractor.py file and update the following variables with your email account information:


# Email account information
EMAIL_ADDRESS = "your-email@example.com"
PASSWORD = "your-password"
IMAP_SERVER = "imap.example.com"
Run the script:
bash

python email_extractor.py
The GUI will appear and display your email account inbox. Click on the "Extract Emails" button to extract the emails and display them on the GUI.
You can use the search box to search for specific emails or use the "Clear" button to clear the search results.
License

This project is licensed under the MIT License. See the LICENSE file for more information.
