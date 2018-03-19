#!/usr/bin/env python3

import os
import sys
import time
import json
import importlib


def main():
    cmd = None
    while True:
        while not cmdParse(cmd)[0]:
            print('\033[2J\033[1;1H', end='')
            print(
                f"\u001b[32;1mmodules\u001b[0m\n{'-' * 7}\n{os.listdir('/etc/ppet/modules')}")
            cmd = input("\n> ")
        cmdMod(cmdParse(cmd)[1])


def checkModule(module):
    if not os.path.isdir(f'/etc/ppet/modules/{module}'):
        eout(
            f"Module {module} does not exist in /etc/ppet/modules! (look at modules/example for help)")
    if not os.path.isfile(f'/etc/ppet/modules/{module}/{module}.py'):
        pass
    if not os.path.isfile(f'/etc/ppet/modules/{module}/module.json'):
        pass
    if module != json.load(open(f'/etc/ppet/modules/{module}/module.json'))['moduleName'].lower():
        eout("Module name does not match json file!")


def eout(error):
    print('\033[2J\033[1;1H', end='')
    print(error)
    input("\n\e[2mpress enter to continue\n")
    main()


def cmdParse(cmd):
    if cmd == None:
        return False, None
    elif cmd == "help":
        print('\033[2J\033[1;1H\u001b[32;1mhelp\u001b[0m\n----')
        print('\ncommand examples:\nuse (module)\nhelp (module)\nexit')
        input("\n\e[2mpress enter to continue\n")
        return False, None
    elif cmd[0:5] == "help ":
        checkModule(cmd[5:])
        print('\033[2J\033[1;1H', end='')
        print(open(f'/etc/ppet/modules/{cmd[5:]}/help').read())
        input("\n\e[2mpress enter to continue\n")
        return False, None
    elif cmd[0:4] == "use ":
        checkModule(cmd[4:])
        return True, cmd[4:].lower()
    elif cmd == "exit":
        print('\033[2J\033[1;1H', end='')
        exit()
    elif cmd == "":
        return False, None
    else:
        eout("Invalid input!")


def cmdMod(module):
    sys.path.insert(0, f'/etc/ppet/modules/{module}')
    if not importlib.util.find_spec(module) is None:
        module = importlib.import_module(module)
    else:
        eout(f"{module} cannot be imported!")
    try:
        module.init()
    except AttributeError:
        pass
    print('\033[2J\033[1;1H', end='')
    print(f"\u001b[32;1m{module}\u001b[0m\n{'-' * len(module)}")
    moduleJSON = json.load(open(f'/etc/ppet/modules/{module}/module.json'))
    cmdInput = input('\n> ')
    if cmdInput.lower() == "exit":
        print('\033[2J\033[1;1H', end='')
        exit()
    elif cmdInput.lower() == "help":
        print('\033[2J\033[1;1H', end='')
        print(f"\u001b[32;1m{module}\u001b[0m\n{'-' * len(module)}\n")
        jsonID = 0
        while jsonID < len(moduleJSON['commands']) - 1:
            jsonID += 1
            print(
                f"{moduleJSON['commands'][jsonID]['name']} - {moduleJSON['commands'][jsonID]['description']}\n")
        input("\n(press enter to continue)\n")
        cmdMod(module)
    jsonID = 0
    while cmdInput.lower() != moduleJSON['commands'][jsonID]['name'].lower():
        if jsonID < (len(moduleJSON['commands']) - 1):
            jsonID += 1
        else:
            eout("Invalid command!")
    try:
        callable(getattr(module, moduleJSON['commands'][jsonID]['function']))
    except AttributeError:
        eout(
            f"Function '{moduleJSON['commands'][jsonID]['function']}' does not exist!")
    _ = getattr(module, moduleJSON['commands'][jsonID]['function'])()


if __name__ == "__main__":
    print('\033[2J\033[1;1H', end='')
    print('\33]0;Python Privilege Escalation Toolkit\a', end='', flush=True)
    print(
        "\u001b[32;1mWelcome to the Python Privilege Escalation Toolkit!\u001b[0m")
    time.sleep(2.5)
    main()
