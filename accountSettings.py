import os
from libraries import filelib as fl


def getSensitiveInfo(savedInput):
    """
    Retrieve and return sensitive information stored in environment variables.
    e.g.: email, password
    For mac & linux, refer to the video link for more information.
    https://www.youtube.com/watch?v=5iWhQWVXosU
    For windows
    https://www.youtube.com/watch?v=IolxqkL7cD8
    """
    return os.environ.get(savedInput)


class AccountsManager:

    accounts = {}
    hotmailAcc = {}
    gmailAcc = {}
    uncategorizedAcc = {}

    def getAccounts(self, _filePath):
        """
        Check if file path exists, then check if file is empty.
        File path must comprise of the location and file
        where the email and password accounts are stored.
        e.g.: /path/myFolder/file.txt
        For security reasons, saving emails and passwords directly in this
        text file is not recommended.
        """
        accountsList = fl.FileSystem().getContents(_filePath)
        for i in range(0, len(accountsList), 2):
            self.accounts[accountsList[i]] = accountsList[i+1]
        del accountsList

    def categorize(self):
        hotmail = "@hotmail.com"
        gmail = "@gmail.com"
        for email in self.accounts.keys():
            if hotmail in email:
                self.hotmailAcc[email] = self.accounts[email]
            elif gmail in email:
                self.gmailAcc[email] = self.accounts[email]
            else:
                if getSensitiveInfo(email):
                    if hotmail in getSensitiveInfo(email):
                        self.hotmailAcc[getSensitiveInfo(email)] = \
                            getSensitiveInfo(self.accounts[email])
                    elif gmail in getSensitiveInfo(email):
                        self.gmailAcc[getSensitiveInfo(email)] = \
                            getSensitiveInfo(self.accounts[email])
                    else:
                        print(f"Domain in {getSensitiveInfo(email)}",
                              "is not supported!")
                        print(f"Transferring to uncategorized section.")
                        self.uncategorizedAcc[getSensitiveInfo(email)] = \
                            getSensitiveInfo(self.accounts[email])
                else:
                    print(f"Domain in {email} is not supported!")
                    print(f"Transferring to uncategorized section.")
                    self.uncategorizedAcc[email] = self.accounts[email]
        # Remove unused space
        self.accounts.clear()
