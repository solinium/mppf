#!/usr/bin/env python3

import os
import sys
import json
import importlib
from time import sleep


def main():
    os.system('clear')
    print(
        '''\u001b[32;1mWelcome to the Python Privilege Escalation Toolkit!\u001b[0m''')
    sleep(2.5)
    cmd()


def checkModule(module):
    if not(os.path.isdir("/etc/ppet/modules/" + module)) or not(os.path.isfile('/etc/ppet/modules/' + module + '/' + module + '.py')) or not(os.path.isfile('/etc/ppet/modules/' + module + '/module.json')):
        eout("Not a valid module! (look at modules/example for help)")


def eout(error):
    os.system('clear')
    input(error + "\n| press enter to continue |\n")
    cmd()


def cmd():
    os.system('clear')
    print("\u001b[32;1mmodules available\u001b[0m\n-----------------\n",
          os.listdir("/etc/ppet/modules"))
    cmdInput = input("\n> ")
    if cmdInput.lower() == "help":
        os.system('clear')
        print(
            "\u001b[32;1mhelp\u001b[0m\n----\n\ncommand examples:\nuse (module)\nhelp (module)\nexit")
        input("\n| press enter to continue |\n")
        cmd()
    elif cmdInput[0:4].lower() == "use ":
        checkModule(cmdInput[4:].lower())
        cmdMod(cmdInput[4:].lower())
    elif cmdInput[0:5].lower() == "help ":
        checkModule(cmdInput[5:].lower())
        os.system('clear')
        os.system("cat /etc/ppet/modules/" +
                  cmdInput[5:].lower() + "/help")
        input("\n| press enter to continue |\n")
        cmd()
    elif cmdInput.lower() == "exit":
        os.system('clear')
        exit()
    elif cmdInput == "":
        eout("Input cannot be empty!")
    else:
        eout("Invalid input!")


def cmdMod(mod):
    os.system('clear')
    print('\u001b[32;1m' + mod + '\u001b[0m' + '\n' + ('-' * len(mod)))
    sys.path.insert(0, '/etc/ppet/modules/' + mod)
    module = importlib.import_module(mod)
    try:
        moduleJSON = json.load(
            open('/etc/ppet/modules/' + mod + '/module.json'))
    except FileNotFoundError:
        eout("module.json invalid or non-existent!")
    if mod != moduleJSON['moduleName'].lower():
        eout("module does not match JSON file!")
    cmdInput = input("\n> ")
    if cmdInput.lower() == "exit":
        os.system('clear')
        exit()
    elif cmdInput.lower() == "help":
        os.system('clear')
        print('\u001b[32;1m' + mod + '\u001b[0m' +
              '\n' + ('-' * len(mod)) + '\n')
        jsonID = 0
        while jsonID < (int(moduleJSON['commandCount']) - 1):
            jsonID += 1
            print(mod + " - " + moduleJSON['commands']
                  [jsonID]['description'] + '\n')
            input("\n| press enter to continue |\n")
            cmdMod(mod)
    """ if cmdInput.lower() == "run":
        os.system('clear')
        module.main()
    elif cmdInput.lower() == "help":
        os.system('clear')
        os.system("cat /etc/ppet/modules/" + mod + "/help")
        input("\n| press enter to continue |\n")
        cmdMod(mod)
    elif cmdInput.lower() == "exit":
        os.system('clear')
        exit()
    else:
        print("Invalid command!")
        eout() """
    jsonID = 0
    while cmdInput.lower() != moduleJSON['commands'][jsonID]['name'].lower():
        if jsonID < (int(moduleJSON['commandCount']) - 1):
            jsonID += 1
        else:
            eout("Invalid command!")
    _ = getattr(module, moduleJSON['commands'][jsonID]['function'])()


if __name__ == "__main__":
    main()
