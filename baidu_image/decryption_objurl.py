#!-*-coding:utf-8-*-

import json
import re

string = "ippr_z2C$qAzdH3FAzdH3F5ff_z&e3Bi7wg2yjbb_z&e3BgjpAzdH3FstejAzdH3F7fj6AzdH3Fdcbldn0AzdH3F8cddbdd08na0adcmbaa-a_z&e3B3r2"

data_1 = {
        "_z2C$q": ":",
        "AzdH3F": "/",
        "_z&e3B": "."
   		 }
data_2 = {
        "0": "7",
        "1": "d",
        "2": "g",
        "3": "j",
        "4": "m",
        "5": "o",
        "6": "r",
        "7": "u",
        "8": "1",
        "9": "4",
        "O": "O",
        "N": "N",
        "R": "R",
        "z": "z",
        "e": "v",
        "o": "w",
        "x": "x",
        "M": "M",
        "p": "t",
        "j": "e",
        "H": "H",
        "A": "A",
        "S": "S",
        "i": "h",
        "k": "b",
        "g": "n",
        "_": "_",
        "C": "C",
        "d": "2",
        "m": "6",
        ":": ":",
        "n": "3",
        "u": "f",
        "D": "D",
        "B": "B",
        "/": "/",
        "w": "a",
        "f": "s",
        ".": ".",
        "T": "T",
        "%": "%",
        "s": "l",
        "r": "p",
        "E": "E",
        "l": "9",
        "a": "0",
        "t": "i",
        "-": "-",
        "v": "c",
        "b": "8",
        "L": "L",
        "Q": "Q",
        "c": "5",
        "=": "=",
        "h": "k"
    }
k_value =list(data_1.keys())    
v_list = list(data_1.values())

for i in range(0,len(k_value)):
	string = string.replace(k_value[i],v_list[i])
string = list(string)

objs = []
for i in range(0,len(string)):
	for key in data_2.keys():
		if string[i] == key:
			objs.append(data_2[key])
objurl = ''.join(objs)
print(objurl)
