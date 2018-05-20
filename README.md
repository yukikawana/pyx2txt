# pyx2txt
pyx2txt is a stand-alone python-based CUI image viewer.
It converts an image to unicode characters and display it on a terminal.

![Alt ss](samples/car.png)

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
