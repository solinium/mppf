#!/usr/bin/env python3

import os
import re
import sys
import time
import json
import shlex
import inspect
import importlib


def main():
    while True:
        cmd = None
        while not cmdParse(cmd):
            print('\033[2J\033[1;1H', end='')
            print(
                f"\u001b[32;1mmodules\u001b[0m\n{'-' * 7}\n{os.listdir('/etc/mppf/modules')}")
            cmd = shlex.split(input('\n> ').lower())
        moduleName = cmd[1]
        moduleJSON = json.load(
            open(f'/etc/mppf/modules/{moduleName}/module.json'))
        module = importModule(moduleName)
        cmd = ['']
        while not cmdParseLoaded(cmd, moduleJSON, module):
            print('\033[2J\033[1;1H', end='')
            print(
                f"\u001b[32;1m{moduleName}\u001b[0m\n{'-' * len(moduleName)}")
            cmd = shlex.split(input('\n> ').lower())
        jsonID = cmdParseLoaded(cmd, moduleJSON, module)[1]
        try:
            callable(
                getattr(module, moduleJSON['commands'][jsonID]['function']))
        except AttributeError:
            err(
                f"Function '{moduleJSON['commands'][jsonID]['function']}' does not exist!")
        print()
        if moduleJSON['commands'][jsonID]['arguments'] != 0:
            args = cmd[1:]
        else:
            args = []
        moduleErr = getattr(
            module, moduleJSON['commands'][jsonID]['function'])(*args)
        if moduleErr != '' and moduleErr != None:
            err(moduleErr)
        input("\n(press enter to continue)\n")


def checkModule(name):
    name = name.lower()
    if not os.path.isdir(f'/etc/mppf/modules/{name}'):
        err(
            f"Module '{name}' does not exist in /etc/mppf/modules! (look at modules/example for help)")
    if not os.path.isfile(f'/etc/mppf/modules/{name}/{name}.py'):
        pass
    if not os.path.isfile(f'/etc/mppf/modules/{name}/module.json'):
        pass
    if name != json.load(open(f'/etc/mppf/modules/{name}/module.json'))['moduleName']:
        err("Module name does not match json file!")


def err(error):
    print('\033[2J\033[1;1H', end='')
    print(error)
    input("\n(press enter to continue)\n")
    main()


def cmdParse(cmd):
    if cmd == None:
        return False
    if cmd == []:
        main()
    if cmd[0] == 'help':
        if len(cmd) == 1:
            print('\033[2J\033[1;1H\u001b[32;1mhelp\u001b[0m\n----')
            print('\ncommand examples:\nuse (module)\nback (in module)\nhelp\nexit')
            input("\n(press enter to continue)\n")
            return False
        elif len(cmd) == 2:
            print('\033[2J\033[1;1H', end='')
            print(open(f'/etc/mppf/modules/{cmd[5:]}/help').read())
            input("\n(press enter to continue)\n")
            return False
        err("Invalid input!")
    elif cmd[0] == 'use':
        checkModule(cmd[1])
        return True
    elif cmd[0] == 'exit' or 'quit':
        print('\033[2J\033[1;1H', end='')
        exit()
    err("Invalid input!")


def cmdParseLoaded(cmd, json, module):
    name = shlex.split(str(module))[1].lower()
    if cmd[0] == '':
        return False
    elif cmd[0] == 'help':
        print('\033[2J\033[1;1H', end='')
        print(
            f"\u001b[32;1m{name}\u001b[0m\n{'-' * len(name)}\n")
        print(f"{json['description']}\n")
        jsonID = 0
        while jsonID < len(json['commands']):
            print(
                f"{json['commands'][jsonID]['name']} - {inspect.getdoc(getattr(module, json['commands'][jsonID]['function']))}\n")
            jsonID += 1
        input("\n(press enter to continue)\n")
        return False
    elif cmd[0] == 'back':
        main()
    elif cmd[0] == 'exit':
        print('\033[2J\033[1;1H', end='')
        exit()
    jsonID = 0
    while cmd[0] != json['commands'][jsonID]['name'].lower():
        if jsonID < len(json['commands']) - 1:
            jsonID += 1
        else:
            err("Invalid command!")
    return True, jsonID


# def cmdParseArguments(cmd, num, json):


def importModule(name):
    name = name.lower()
    sys.path.insert(0, f'/etc/mppf/modules/{name}')
    try:
        module = importlib.import_module(name)
    except AttributeError:
        err(f"{name} cannot be imported!")
    try:
        module.init()
    except AttributeError:
        pass
    return module


if __name__ == "__main__":
    print('\033[2J\033[1;1H', end='')
    print('\33]0;Mediocre Python Penetration Framework\a', end='', flush=True)
    print(
        "\u001b[32;1mWelcome to the Mediocre Python Penetration Framework!\u001b[0m")
    time.sleep(2.5)
    main()
