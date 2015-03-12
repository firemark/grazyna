'''
Created on 09-06-2012

@author: firemark

Formatting IRC messages.
Colors, bolding...
'''


def bold(msg):
    return "\x02" + msg + "\x02"


def underline(msg):
    return "\x1F" + msg + "\x1F"


def italic(msg):
    return "\x16" + msg + "\x16"


def color(msg, front, back=None):
    if back:
        front = str(front) + ',' + str(back)
    else:
        front = str(front)
    return "\x03" + front + msg + "\x03"

#colors
color.white = 0
color.black = 1
color.dark_blue = 2
color.green = 3
color.red = 4
color.brown = 5
color.purple = 6
color.olive = 7
color.yellow = 8
color.light_green = 9
color.teal = 10
color.cyan = 11
color.light_blue = 12
color.pink = 13
color.dark_gray = 14
color.light_gray = 15
