import os
import shutil
import subprocess


def main():
    '''Does the basic printing, no arguments.'''
    if shutil.which('uname') != None:
        print("\u001b[32;1muname\u001b[0m\n-----")
        os.system('uname -a')
        print('\n')
    if os.path.isfile('/etc/issue'):
        print("\u001b[32;1m/etc/issue\u001b[0m\n----------")
        os.system('cat /etc/issue')
        print('\n')
    if os.path.isfile('/etc/lsb-release') or os.path.isfile('/etc/redhat-release'):
        print("\u001b[32;1m/etc/*-release\u001b[0m\n--------------")
        subprocess.run(['cat', '/etc/*-release'],
                       stdout=subprocess.PIPE).stdout.decode('utf-8')
        print('\n')
