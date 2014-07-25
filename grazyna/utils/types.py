'''
Types to arguments
'''


def range_int(left=None, right=None):

    def func(x):
        x = int(x)
        if left != None:
            x = max(left, x)
        if right != None:
            x = min(right, x)

        return x
    return func


def is_chan(chan):
    if chan and chan[0] != '#':
        raise TypeError('Is not a channel')
    return chan
