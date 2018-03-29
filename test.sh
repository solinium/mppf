#!/bin/sh
# before first run do sudo mkdir /etc/mppf

sudo rm -rf /etc/mppf
sudo mkdir -p /etc/mppf
sudo cp -r modules /etc/mppf/modules
pyver=`python -c 'import sys; print("%i" % (sys.hexversion<0x03000000))'`
if [ $pyver -eq 0 ]; then
	python mppf.py
else 
	python3 mppf.py
fi