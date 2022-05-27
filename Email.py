import email
import imaplib
import os
import pathlib
import sys
import json
import time


class GMAIL_EXTRACTOR():

    def helloWorld(self):
        print("\nWelcome to Gmail extractor")

    def initializeVariables(self):
        self.usr = ""
        self.pwd = ""
        self.mail = object
        self.mailbox = ""
        self.mailCount = 0
        self.destFolder = ""
        self.data = []
        self.ids = []
        self.idsList = []
        self.latest_email = []
        self.whileCount = 0
        self.file_path = pathlib.Path("./xtracted/")

    def getLogin(self):
        print("\nLoading please wait")
        username = input("Input your gmail/yahoo address:")
        password = input("Enter your password:")

        self.usr = username
        self.pwd = password

    def attemptLogin(self):
        while True:
            gmail_imap = "imap.gmail.com"
            yahoo_imap = "imap.mail.yahoo.com"
            mailChoice = ""
            try:
                Choice = int(input("Enter 1 for gmail services or 2 for Yahoo mail service: "))
                break


            except ValueError:
                print("please enter appropriate input")
                continue
        if Choice == 1:
            mailChoice = gmail_imap

        elif Choice == 2:
            mailChoice = yahoo_imap

        self.mail = imaplib.IMAP4_SSL(mailChoice, 993)

        if self.mail.login(self.usr, self.pwd):
            print("\nLogin SUCCESSFUL")
            self.destFolder = "./xtracted/"
            # if not self.destFolder.endswith("/"): self.destFolder += "/"
            return True
        else:
            print("\nLogon FAILED")
            return False

    # def checkIfUsersWantsToContinue(self):
    # print("\nWe have found " + str(self.mailCount) + " emails in the mailbox " + self.mailbox + ".")
    # return True if input(
    # "Do you wish to continue extracting all the emails into " + self.destFolder + "? (y/N) ").lower().strip()[
    # :1] == "y" else False

    def selectMailbox(self):

        self.mailbox = "INBOX"
        bin_count = self.mail.select(self.mailbox)[1]
        self.mailCount = int(bin_count[0].decode("utf-8"))
        return True if self.mailCount > 0 else False

    def searchThroughMailbox(self):
        type, self.data = self.mail.search(None,
                                           '(FROM "uba.alert@ubagroup.com" SUBJECT "UBA CREDIT Transaction Notification")')
        print("\nGetting desired mail from inbox")
        self.ids = self.data[0]
        self.idsList = self.ids.split()
        self.latest_email = self.idsList[-10:]

        print("Processing %d emails...\n" % (len(self.latest_email)))

    def parseEmails(self):
        jsonOutput = {}
        self.ids = self.data[0]
        self.idsList = self.ids.split()
        self.latest_email = self.idsList[-10:]

        for anEmail in self.latest_email:
            type, self.latest_email = self.mail.fetch(anEmail, '(UID RFC822)')
            raw = self.latest_email[0][1]
            try:
                raw_str = raw.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    raw_str = raw.decode("ISO-8859-1")  # ANSI support
                except UnicodeDecodeError:
                    try:
                        raw_str = raw.decode("ascii")  # ASCII ?
                    except UnicodeDecodeError:
                        pass

            msg = email.message_from_string(raw_str)

            jsonOutput['subject'] = msg['subject']
            jsonOutput['from'] = msg['from']
            jsonOutput['date'] = msg['date']

            raw = self.latest_email[0][0]
            raw_str = raw.decode("utf-8")
            uid = raw_str.split()[2]

            # Body #
            if msg.is_multipart():
                for part in msg.walk():
                    partType = part.get_content_type()
                    ## Get Body ##
                    if partType == "text/plain" and "attachment" not in part:
                        jsonOutput['body'] = part.get_payload()
                    ## Get Attachments ##
                    if part.get('Content-Disposition') is None:
                        attchName = part.get_filename()
                        if bool(attchName):
                            attchFilePath = str(self.destFolder) + str(uid) + str("/") + str(attchName)
                            os.makedirs(os.path.dirname(attchFilePath), exist_ok=True)
                            with open(attchFilePath, "wb") as f:
                                f.write(part.get_payload(decode=True))
            else:
                jsonOutput['body'] = msg.get_payload(decode=True).decode(
                    "utf-8")  # Non-multipart email, perhaps no attachments or just text.

            outputDump = json.dumps(jsonOutput)
            emailInfoFilePath = str(self.destFolder) + str(uid) + str("/") + str(uid) + str(".json")
            existed_file = os.path.exists(str(self.destFolder) + str(uid) + str("/") + str(uid) + str(".json"))
            existFile = [existed_file]
            Length = len(existFile)

            if len(existFile) > 0:
                print("no new emails found\nTotal existed mail is:", Length)

            else:
                os.makedirs(os.path.dirname(emailInfoFilePath), exist_ok=False)
                print('New emails detected...\nExtracting new emails,please wait...')
                with open(emailInfoFilePath, "w") as f:
                    f.write(outputDump)


def __init__(self):
    self.initializeVariables()
    self.helloWorld()
    self.getLogin()
    if self.attemptLogin():
        not self.selectMailbox() and sys.exit()
    else:
        sys.exit()
    # not self.checkIfUsersWantsToContinue() and sys.exit()
    while True:
        self.searchThroughMailbox()
        self.parseEmails()
        time.sleep(2)
        self.whileCount += 1
        print("checking for new transaction mail for the", self.whileCount, "times")


if __name__ == "__main__":
    run = GMAIL_EXTRACTOR()
