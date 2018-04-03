#!/bin/sh

if [ ! -d '/etc/mppf' ]; then
	sudo mkdir /etc/mppf 
else
	sudo rm -rf /etc/mppf
	sudo mkdir -p /etc/mppf
fi
sudo cp -r modules /etc/mppf/modules
pyver=`python -c 'import sys; print("%i" % (sys.hexversion<0x03000000))'`
if [ $pyver -eq 0 ]; then
	python mppf.py
else
	python3 mppf.py
fi