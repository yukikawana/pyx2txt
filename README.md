# pyx2txt

pyx2txt is a stand-alone python-based CUI image viewer. 

pyx2txt converts an image to unicode characters and display it on a terminal.

Unicode characters for image rendering are carefully chosen for iOS terminal, especially for [WebSSH](https://itunes.apple.com/jp/app/webssh-pro/).

![Alt s](samples/car.png)

## Requirements
- python 2.x (currently python3 is not supported)
- joblib
- pip
- numpy
- Pillow
- PyInstaller

## Installation
```bash
git clone https://github.com/yukikawana/pyx2txt --recursive
cd pyx2txt
sudo sh install.sh
```

## Usage
```bash
p2t image/test.jpg
```
For further usage see
```bash
p2t -h
```
