import os
import subprocess
from shutil import which


def main():
    if which('uname') != None:
        print("uname\n-----")
        os.system('uname -a')
        print('\n')
    if os.path.isfile('/etc/issue'):
        print("/etc/issue\n----------")
        os.system('cat /etc/issue')
        print('\n')
    if os.path.isfile('/etc/lsb-release') or os.path.isfile('/etc/redhat-release'):
        print("/etc/*-release\n--------------")
        os.system('cat /etc/*-release')
        print('\n')


# def cmdOutput(cmd):
#    output = subprocess.check_output(cmd, shell=True)
#    return str(output)
