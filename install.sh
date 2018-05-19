#!/bin/bash
python3path=$(which python)
if [ $python3path ]; then
	echo "found python2.x in $python3path"
	pip3path=$(which pip)
	if [ $pip3path ]; then
		echo "found pip in $pip3path"
		pyinpath=$(pip list | grep -F PyInstaller | awk '{print $1}')
		numpypath=$(pip list | grep -F numpy | awk '{print $1}')
		pillowpath=$(pip list | grep -F Pillow | awk '{print $1}')
		if [ ! $numpypath ]; then
			echo "numpy needs to be installed"
			return 0
		else
			echo "numpy found"
		fi
		if [ ! $pillowpath ]; then
			echo "pillow needs to be installed"
			return 0
		else
			echo "pillow found"
		fi
		if [ $pyinpath ]; then
			echo "PyIntaller installed"
			pyinstaller pyx2txt.spec
			cp dist/p2t /usr/local/bin
		else
			echo "PyInstaller needs to be installed"
			return 0
		fi

	else
		echo "pip needs to be installed"
		return 0
	fi
else
	echo "python2.x needs to be installedt"
	return 0
fi
