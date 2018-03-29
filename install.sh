#!/bin/sh

sudo clear
git clone https://github.com/solinium/mppf /tmp/mppf
sudo mkdir /etc/mppf
sudo cp -r /tmp/mppf/modules /etc/mppf/
sudo cp /tmp/ppet/mppf.py /usr/bin/mppf
sudo chmod +x /usr/bin/mppf
rm -rf /tmp/mppf/
clear
echo "Install completed, launch with 'mppf'."