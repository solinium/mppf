#!/usr/bin/env python3

import os
import re
import sys
import time
import json
import shlex
import inspect
import importlib

# change main to not accept bool
#


def main(keepLoaded):
    moduleName = None
    moduleJson = None
    while True:
        if keepLoaded:
            mainLoaded(moduleJson, importModule(moduleName, False), moduleName)
        cmd = None
        keepLoaded = False
        while not cmdParse(cmd):
            print('\033[2J\033[1;1H', end='')
            folderList = os.listdir(f'{os.environ["HOME"]}/.mppf/modules')
            modules = {'standard': [], 'scanners': [], 'exploits': []}
            for x in folderList:
                jsonIndex = json.load(
                    open(f'{os.environ["HOME"]}/.mppf/modules/{folderList[folderList.index(x)]}/module.json'))
                if jsonIndex['type'] == 'standard':
                    modules['standard'].append(jsonIndex['name'])
                elif jsonIndex['type'] == 'scanner':
                    modules['scanners'].append(jsonIndex['name'])
                elif jsonIndex['type'] == 'exploit':
                    modules['exploits'].append(jsonIndex['name'])
                else:
                    error("Invalid module type!")
            if modules['standard'] != []:
                print(
                    f"\u001b[32;1mstandard\u001b[0m\n-------\n{modules['standard']}")
            if modules['scanners'] != []:
                if modules['standard'] != []:
                    print('\n')
                print(
                    f"\u001b[32;1mscanners\u001b[0m\n--------\n{modules['scanners']}")
            if modules['exploits'] != []:
                if modules['scanners'] != []:
                    print('\n')
                elif modules['standard'] != []:
                    print('\n')
                print(
                    f"\n\u001b[32;1mexploits\u001b[0m\n--------\n{modules['exploits']}")
            cmd = shlex.split(input('\n> ').lower())
        moduleName = cmd[1]
        moduleJSON = json.load(
            open(f'{os.environ["HOME"]}/.mppf/modules/{moduleName}/module.json'))
        keepLoaded = mainLoaded(
            moduleJSON, importModule(moduleName, True), moduleName)


def mainLoaded(json, module, moduleName):
    cmd = ['']
    while not cmdParseLoaded(cmd, json, module):
        print('\033[2J\033[1;1H', end='')
        print(
            f"\u001b[32;1m{moduleName}\u001b[0m\n{'-' * len(moduleName)}")
        cmd = shlex.split(input('\n> ').lower())
    jsonID = cmdParseLoaded(cmd, json, module)[1]
    try:
        callable(getattr(module, json['commands'][jsonID]['function']))
    except AttributeError:
        error(
            f"Function '{json['commands'][jsonID]['function']}' does not exist!")
    print()
    args = []
    if json['commands'][jsonID]['arguments'] != 0:
        args = cmd[1:]
    moduleErr = getattr(module, json['commands'][jsonID]['function'])(*args)
    # (*args)
    if moduleErr != '' and None:
        error(moduleErr)
    input("\n(press enter to continue)\n")
    return True


def checkModule(name):
    name = name.lower()
    if not os.path.isdir(f'{os.environ["HOME"]}/.mppf/modules/{name}'):
        error(
            f"Module '{name}' does not exist in {os.environ['HOME']}/.mppf/modules! (look at modules/example for help)")
    if not os.path.isfile(f'{os.environ["HOME"]}/.mppf/modules/{name}/{name}.py'):
        pass
    if not os.path.isfile(f'{os.environ["HOME"]}/.mppf/modules/{name}/module.json'):
        pass
    if name != json.load(open(f'{os.environ["HOME"]}/.mppf/modules/{name}/module.json'))['name'].lower():
        error("Module name does not match json file!")


def error(err):
    print('\033[2J\033[1;1H', end='')
    print(f"\033[38;5;1mError\n-----\033[0m\n{err}\n")
    input("(press enter to continue)\n")
    main(False)


def cmdParse(cmd):
    if cmd == None:
        return False
    if cmd == []:
        main(False)
    if cmd[0] == 'help' and len(cmd) == 1:
        print('\033[2J\033[1;1H\u001b[32;1mhelp\u001b[0m\n----')
        print('\ncommand examples:\nuse (module)\nback (in module)\nhelp\nexit')
        input("\n(press enter to continue)\n")
        return False
    elif cmd[0] == 'use' and (len(cmd) == 1 or 2):
        checkModule(cmd[1])
        return True
    elif cmd[0] == 'exit' or 'e' or 'quit' or 'q':
        print('\033[2J\033[1;1H', end='')
        exit()
    error("Invalid input!")


def cmdParseLoaded(cmd, json, module):
    name = shlex.split(str(module))[1].lower()
    if cmd[0] == '':
        return False
    elif cmd[0] == 'help':
        print('\033[2J\033[1;1H', end='')
        print(
            f"\u001b[32;1m{name}\u001b[0m\n{'-' * len(name)}\n")
        print(f"{json['description']}")
        print('-' * len(json['description']) + '\n')
        jsonID = 0
        while jsonID < len(json['commands'])-1:
            print(
                f"{json['commands'][jsonID]['name']} - {inspect.getdoc(getattr(module, json['commands'][jsonID]['function']))}\n")
            jsonID += 1
        input("\n(press enter to continue)\n")
        return False
    elif cmd[0] == 'back':
        main(False)
    elif cmd[0] == 'exit':
        print('\033[2J\033[1;1H', end='')
        exit()
    jsonID = 0
    while cmd[0] != json['commands'][jsonID]['name'].lower():
        if jsonID < len(json['commands']) - 1:
            jsonID += 1
        else:
            error("Invalid command!")
    return True, jsonID


def importModule(name, init):
    name = name.lower()
    sys.path.insert(0, f'{os.environ["HOME"]}/.mppf/modules/{name}')
    try:
        module = importlib.import_module(name)
    except AttributeError:
        error(f"{name} cannot be imported!")
    if init:
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
    main(False)
