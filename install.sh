#!/bin/sh

sudo clear
git clone https://github.com/solinium/ppet /tmp/ppet
sudo mkdir /etc/ppet
sudo cp -r /tmp/ppet/modules /etc/ppet/
sudo cp /tmp/ppet/ppet.py /usr/bin/ppet
sudo chmod +x /usr/bin/ppet
rm -rf /tmp/ppet/
clear
echo "Install completed, launch with 'ppet'."