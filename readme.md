# Spam Email Automation
* The purpose of this app is to delete all of my spam emails automatically for me.
* The downside of this is that no AI is implemented, therefore, spam emails are not automatically detected.
* This means that you have to update the spam_list.txt manually.

## Tests
* Tested on Mac OSX Mojave.
    * linux should work, but yet to be tested.
* Python 3.6 and above should work.

## How to get it to work?
* No additional installation required. Only Python needs to be installed.
* Default mode: all files are created, opened, and saved automatically
    * If you cloned this app, no files will be created, only filling of sensitive information (email, password) and editing of spam_list.txt is required.
    * If the required text files are not included, it will be automatically be created and you will be prompted to fill in the required information.
    * To run
    > python run.py

* Manual mode: all files are manually created.
    * All files created and the values stored will be saved at the path keyed during prompt.
    * However, these files and paths have to be added to the useDefault method in the fileLib.py located in the libraries folder.
    * Any further changes, please refer to the docs written in the files, which states that it has to be updated.
    * To run
    > python run.py manual

* Help mode: display help menu if you forgotten the simple commands.
    * To run
    > python run.py help


