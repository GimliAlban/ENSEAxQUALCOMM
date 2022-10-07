from lef_parser import *
import os

with open("src/test.txt") as fileLef:
    stringLef = fileLef.read()

lefCell = LefCell("Hello", stringLef)
lefCell.get_ports()