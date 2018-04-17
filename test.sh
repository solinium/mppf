#!/bin/sh

if [ ! -d '$HOME/.mppf' ]; then
	mkdir $HOME/.mppf
else
	rm -rf $HOME/.mppf
	mkdir -p $HOME/.mppf
fi
cp -r modules $HOME/.mppf
pyver=`python -c 'import sys; print("%i" % (sys.hexversion<0x03000000))'`
if [ $pyver -eq 0 ]; then
	python mppf.py
else
	python3 mppf.py
fi