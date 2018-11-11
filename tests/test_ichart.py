import pytest
from instiz import iChart


@pytest.fixture
def class_init():
    ichart = iChart()
    return ichart


def test_10(class_init):
    assert len(class_init.realtime_top_10()) == 10


def test_refresh(class_init):
    x = class_init.refresh()
    assert isinstance(x, iChart)


def test_get_rank(class_init):
    x = class_init.get_next_entry()
    assert next(x).rank == 1
