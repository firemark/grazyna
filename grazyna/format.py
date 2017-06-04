'''
Created on 09-06-2012

@author: firemark

Formatting IRC messages.
Colors, bolding...
'''


def bold(msg):
    return "\x02%s\x02" % msg


def underline(msg):
    return "\x1F%s\x1F" % msg


def italic(msg):
    return "\x16%s\x16" % msg


def color(msg, front, back=None):
    if back:
        front = '%d,%d' % (front, back)
    else:
        front = str(front)
    return "\x03%s%s\x03" % (front, msg)

# colors
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
