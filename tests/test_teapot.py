import pytest

from teapot.exceptions import TeapotError
from teapot.teapot import Teapot
from teapot.types import TeapotState


def test_empty_teapot_cant_be_activated():
    teapot = Teapot()

    with pytest.raises(TeapotError):
        teapot.activate()

    assert teapot.state == TeapotState.INACTIVE, 'Неверное состояние чайника'


@pytest.mark.parametrize('value', [
    -5,
    0,
    'Hello',
    -0.5,
    '1',
])
def test_cant_pour_incorrect_amount_of_water(value):
    teapot = Teapot(volume=2.0)

    with pytest.raises(TeapotError):
        teapot.pour_water(value)


@pytest.mark.parametrize('value', [
    1.5,
    2,
    'Hello',
    '1',
])
def test_cant_pour_out_incorrect_amount_of_water(value):
    teapot = Teapot(volume=2.0)
    teapot.pour_water(1)

    with pytest.raises(TeapotError):
        teapot.pour_out_water(value)


def test_success_activate():
    teapot = Teapot(volume=1.0, boiling_time=1)
    teapot.pour_water(1)
    teapot.activate()

    assert teapot.state == TeapotState.BOILED, 'Неверный статус чайника'


