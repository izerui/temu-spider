#!/bin/bash
rm -rf build dist
# https://pyinstaller.org/en/stable/usage.html
pyinstaller -n temu-spider -w -i icon.icns main.py