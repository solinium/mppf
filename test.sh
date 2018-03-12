#!/bin/sh

sudo rm -rf /etc/ppet
sudo mkdir -p /etc/ppet
sudo cp -r modules /etc/ppet/modules
pyver=`python -c 'import sys; print("%i" % (sys.hexversion<0x03000000))'`
if [ $pyver -eq 0 ]; then
	python ppet.py
else 
	python3 ppet.py
fi