#!/bin/bash
python3path=$(which python3)
if [ $python3path ]; then
	echo "found python3 in $python3path"
	pip3path=$(which pip3)
	if [ $pip3path ]; then
		echo "found pip3 in $pip3path"
		pyinpath=$(pip3 list | grep -F PyInstaller | awk '{print $1}')
		if [ $pyinpath ]; then
			echo "PyIntaller installed"
			2to3 -w extra
			pyinstaller pyx2txt.spec
			cp dist/p2t /usr/local/bin
		else
			echo "PyInstaller needs to be installed"
		fi

	else
		echo "pip3 needs to be installed"
	fi
	echo $pippath
else
	echo "python3 needs to be installedt"
fi
