from libraries import filelib as fl
from libraries import emailLib as el
import accountSettings as acs
import getpass
from tqdm import tqdm


class Settings:
    """
    Get and set all of the basic required information neccessary for the
    email app to work.
    """

    def __init__(self, default=True):
        self.default = default
        self.authenPath = self.getPath("authen")
        accounts = self.setupAccounts()
        self.hotmailAcc = accounts[0]
        self.gmailAcc = accounts[1]
        self.unknownAcc = accounts[2]
        self.spamListPath = self.getPath("spam")
        self.spamList = self.getSpamList()

    def getPath(self, fileType):
        """
        This will return the file path of the predeclared fileType.
        If not using default path and values, update the
        useDefaultPath method in the filelib.py file.
        Manual keyed inputs will not be saved.
        """
        _file = fl.FileSystem()
        if self.default is True:
            # Change or add default path at filelib.py if not using default
            _file.useDefaultPath(fileType)
        else:
            if fileType == "authen":
                print("Please create an authenticaton.txt file.")
            elif fileType == "spam":
                print("Please create a spam_list.txt file.")
        # Create txt file if does not exist, else pass.
        _file.createFile()  # if default is not True, set path then create.
        return _file.filePath

    def setupAccounts(self):
        """
        Get all of the saved accounts from the authentication.txt
        and sort the accounts according to the domain type.
        """
        if fl.FileSystem.isEmpty(self.authenPath):
            text = input("Please enter your email address or environment "
                         "variable\n> ")
            fl.FileSystem.editFile(self.authenPath, text)
            text = getpass.getpass("Please enter your email password or "
                                   "environment variable\n> ")
            fl.FileSystem.editFile(self.authenPath, text)
        acc = acs.AccountsManager()
        acc.getAccounts(self.authenPath)
        # Sort accounts into domain types
        acc.categorize()
        return (acc.hotmailAcc, acc.gmailAcc, acc.uncategorizedAcc)

    def getSpamList(self):
        """Retrieve and return the spam list from the spam_list.txt file."""
        if fl.FileSystem.isEmpty(self.spamListPath):
            self.addSpam()
        with open(self.spamListPath, 'r') as rf:
            spamList = rf.read().split("\n")
        # Remove empty line
        spamList.pop()
        return spamList

    def addSpam(self):
        text = input("Please add the spam email address to delete.\n> ")
        fl.FileSystem.editFile(self.spamListPath, text)


class RunEmail:
    """
    Set server related settings, then run desired task.
    When implementing a new domain type support, must create a new classmethod
    similar to useGmailSettings method, unless it has similar settings to the
    default settings.
    """

    flag = "+FLAGS"
    trash = r"(\\Deleted)"
    spamBox = "junk"

    def __init__(self, default=True):
        self.settings = Settings(default)
        self.domain = None
        self.accounts = None

    @classmethod
    def useGmailSettings(cls):
        cls.flag = "X-GM-LABELS"
        cls.trash = "\\Trash"
        cls.spamBox = "[Gmail]/Spam"

    @classmethod
    def useDefaultSettings(cls):
        """Reset default settings if changed."""
        cls.flag = "+FLAGS"
        cls.trash = r"(\\Deleted)"
        cls.spamBox = "junk"

    def _getStatus(self, user, numUnreadMails, numSpamMails):
        print(f"Login to {user} successfully")
        print(f"You have {numUnreadMails} unread emails and",
              f"{numSpamMails} spam emails.")

    def setServer(self, domainName):
        """Update this if adding new domain support."""
        if domainName == "gmail":
            self.useGmailSettings()
            self.accounts = self.settings.gmailAcc.items()
        elif domainName == "hotmail":
            self.useDefaultSettings()
            self.accounts = self.settings.hotmailAcc.items()
        else:
            raise ValueError(f"{domainName} domain is not supported!")
        self.domain = domainName

    def _deleteMail(self, mailBox, acc):
        print(f"Searching and deleting SPAMS in {mailBox}...")
        totalIDs = []
        acc.selectFolder(mailBox)
        for spamMail in tqdm(self.settings.spamList):
            totalIDs += acc.getIDs(self._getSearch("from", spamMail))
        acc.deleteMsg(totalIDs, self.flag, self.trash)

    def deleteMail(self, acc, user, password):
        self._deleteMail("inbox", acc)
        self._deleteMail(self.spamBox, acc)
        acc.closeServer()
        print("All spam mails have been deleted from INBOX and JUNK!")
        acc.logoffServer()
        print("Logout successfully!\n")

    def _getSearch(self, _type, spamMail):
        """
        _type should be FROM, SUBJECT
        """
        return f"{_type.upper()} {spamMail}"

    def runTask(self, task):
        for user, password in self.accounts:
            acc = el.UseIMAP(user, password,
                             self.domain, self.settings.spamList)
            self._getStatus(user, acc.getNumOfEmails("inbox", "unseen"),
                            acc.getNumOfEmails(self.spamBox, "messages"))
            task(acc, user, password)


def addSpam():
    Settings().addSpam()


def runDeleteMail(domainName, run):
    run.setServer(domainName)
    run.runTask(run.deleteMail)


def main(default):
    if default:
        run = RunEmail(default)
    else:
        run = RunEmail(default)
    runDeleteMail("hotmail", run)
    runDeleteMail("gmail", run)


def showHelp():
    print("--------------HELP MENU--------------")
    print("[+] If this is your first time"
          "\n>>> python run.py manual")
    print("\n[+] If you have already saved all required settings",
          "and do not wish to be prompted"
          "\n>>> python run.py")
