from grazyna.utils.types import range_int, is_chan, regexp

import pytest


def test_range_int():
    typer = range_int(1, 3)
    with pytest.raises(TypeError):
        typer('4')
    with pytest.raises(TypeError):
        typer('0')

    assert typer('2') == 2


def test_range_int_without_ranges():
    typer = range_int()
    assert typer('0') == 0


def test_is_chan():
    assert is_chan('#czarnobyl') is True
    assert is_chan('socek') is False


def test_regexp():
    typer = is_chan()
