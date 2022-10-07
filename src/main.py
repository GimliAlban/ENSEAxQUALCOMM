from lef_parser import *
import os

with open("src/test.txt") as fileLef:
    stringLef = fileLef.read()

lefPort = LefPort("Hello", stringLef)
lefPort.get_polygon()