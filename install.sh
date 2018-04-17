#!/bin/sh

sudo clear
git clone https://github.com/solinium/mppf /tmp/mppf
if [ -d '$HOME/.mppf' ]; then
    rm -rf $HOME/.mppf
fi
mkdir $HOME/.mppf
mv -r /tmp/mppf/modules $HOME/.mppf
sudo mv /tmp/mppf/mppf.py /usr/bin/mppf
sudo chmod +x /usr/bin/mppf
rm -rf /tmp/mppf
clear
echo "Install completed, launch with 'mppf'."