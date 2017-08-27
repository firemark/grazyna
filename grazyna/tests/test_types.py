from grazyna.utils.types import range_int, is_chan, regexp

import pytest


def test_range_int():
    typer = range_int(1, 3)
    assert typer('4') == 3
    assert typer('0') == 1
    assert typer('2') == 2


def test_range_int_without_ranges():
    typer = range_int()
    assert typer('0') == 0


def test_is_chan():
    assert is_chan('#czarnobyl') == '#czarnobyl'
    with pytest.raises(TypeError):
        is_chan('socek')


def test_regexp():
    typer = regexp(r'001+')
    match = typer('0011')
    assert match.group(0) == '0011'
    with pytest.raises(TypeError):
        typer('2')

