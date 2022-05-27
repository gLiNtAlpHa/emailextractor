import email
import imaplib
import os
import threading
import sys
import json
import time


class THREADING_EXTRACTOR():

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
        self.thCount = 0
        self.file_path = ""

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

    def Threaded_searchThroughMailbox(self):
        type, self.data = self.mail.search(None, 'All', ('FROM "oreoluwaa08@gmail.com" SUBJECT "Hy"'))
        self.idss = self.data[0]
        self.idsList1 = self.idss.split()

        if len(self.idsList1) == 0:
            print(" please check your searching criteria")
            sys.exit()
        else:
            self.ids = self.data[0]
            self.idsList = self.ids.split()
            self.latest_email = self.idsList[:]

            # print("Processing %d emails...\n" % (len(self.latest_email)))
            print("checking for available new emails")

    def searchThroughMailbox(self):
        type, self.data = self.mail.search(None, 'Unseen', ('FROM "oreoluwaa08@gmail.com" SUBJECT "Hy"'))
        self.idss = self.data[0]
        self.idsList1 = self.idss.split()

        if len(self.idsList1) == 0:
            print("No data found please check your searching criteria")

        else:
            self.ids = self.data[0]
            self.idsList = self.ids.split()
            self.latest_email = self.idsList[-20:]

            # print("Processing %d emails...\n" % (len(self.latest_email)))
            print("checking for available new emails")

    def checkFiles(self):
        self.existFile = self.idsList[-20:]
        for fileXsit in self.existFile:
            type, self.existFile = self.mail.fetch(fileXsit, '(UID RFC822)')
            raw1 = self.existFile[0][0]
            # getting unique identification number
            raw_str1 = raw1.decode("utf-8")
            uid1 = raw_str1.split()[2]
            self.file_path = os.path.exists(str(self.destFolder) + str(uid1) + str("/"))
            print(self.file_path)

        # input time in seconds

    def parseEmails(self):
        jsonOutput = {}
        self.ids = self.data[0]
        self.idsList = self.ids.split()
        self.latest_email = self.idsList[-20:]

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
                            os.makedirs(os.path.dirname(attchFilePath), exist_ok=False)
                            with open(attchFilePath, "wb") as f:
                                f.write(part.get_payload(decode=True))
            else:
                jsonOutput['body'] = msg.get_payload(decode=True).decode(
                    "utf-8")  # Non-multipart email, perhaps no attachments or just text.

            outputDump = json.dumps(jsonOutput)
            self.emailInfoFilePath = str(self.destFolder) + str(uid) + str("/") + str(uid) + str(".json")

            os.makedirs(os.path.dirname(self.emailInfoFilePath), exist_ok=False)
            print('New emails detected...\nExtracting new emails,please wait...')
            with open(self.emailInfoFilePath, "w") as f:
                f.write(outputDump)
                f.close()
                print('Done')

    def Threaded_parseEmails(self):
        jsonOutput = {}
        self.ids = self.data[0]
        self.idsList = self.ids.split()
        self.latest_email = self.idsList[-20:]

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
                            os.makedirs(os.path.dirname(attchFilePath), exist_ok=False)
                            with open(attchFilePath, "wb") as f:
                                f.write(part.get_payload(decode=True))
            else:
                jsonOutput['body'] = msg.get_payload(decode=True).decode(
                    "utf-8")  # Non-multipart email, perhaps no attachments or just text.

            outputDump = json.dumps(jsonOutput)
            self.emailInfoFilePath = str(self.destFolder) + str(uid) + str("/") + str(uid) + str(".json")
            self.file_path = os.path.exists(str(self.destFolder) + str(uid) + str("/"))
            if not self.file_path:
                os.makedirs(os.path.dirname(self.emailInfoFilePath), exist_ok=False)
                print('New emails detected...\nExtracting new emails,please wait...')
                with open(self.emailInfoFilePath, "w") as f:
                    f.write(outputDump)
                    f.close()
                    print('Done')
            else:
                print("no new  mails found...")

    def collect_THREADED(self):
        not self.selectMailbox() and sys.exit()
        self.Threaded_searchThroughMailbox()
        self.Threaded_parseEmails()

    def __init__(self):
        self.initializeVariables()
        self.helloWorld()
        self.getLogin()
        if self.attemptLogin():
            while True:
                not self.selectMailbox() and sys.exit()
                # not self.checkIfUsersWantsToContinue() and sys.exit()

                self.searchThroughMailbox()

                # self.checkFiles()
                self.parseEmails()
                self.whileCount += 1
                print("\nchecking for new transaction mail for the", self.whileCount, "times")
                time.sleep(4)
                break

            delay = 6
            print ('thread')
            start_time = threading.Timer(delay, self.collect_THREADED)
            print("THREAD!")
            while True:
                print('yeah')
                start_time.start()
                self.thCount +=1
                print("\nchecking for new transaction mail for the", self.thCount, "times")
                time.sleep(1)



        else:
            sys.exit()


if __name__ == "__main__":
    run = THREADING_EXTRACTOR()
