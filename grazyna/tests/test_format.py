from grazyna import format


def test__bold():
    assert format.bold('socek') == '\x02socek\x02'


def test__underline():
    assert format.underline('socek') == '\x1Fsocek\x1F'


def test__italic():
    assert format.italic('socek') == '\x16socek\x16'


def test__color_without_background():
    msg = format.color('socek', format.color.white)
    assert msg == '\x030socek\x03'


def test__color_with_background():
    msg = format.color('socek', format.color.white, format.color.black)
    assert msg == '\x030,1socek\x03'
