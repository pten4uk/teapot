from logging import getLogger

from console.utils import get_number_from_input
from teapot.teapot import Teapot
from teapot.types import TeapotState

logger = getLogger(__file__)


class Command:
    """
    Класс команды для консоли.

    get_number() - возвращает номер команды
    get_description() - возвращает описание команды
    """

    __slots__ = [
        '__number',
        '__description',
        '_teapot'
    ]

    def __init__(self, teapot: Teapot, number: int, description: str):
        if not isinstance(teapot, Teapot):
            raise ValueError(f'teapot должен быть типом {Teapot}')
        if not isinstance(number, int) or number <= 0:
            raise ValueError('Номер команды должен быть целым положительным числом')
        if not isinstance(description, str):
            raise ValueError('Описание должно быть строкой')

        self.__number = number
        self.__description = description
        self._teapot = teapot

    def get_number(self):
        return self.__number

    def get_description(self):
        return self.__description

    def perform(self):
        """ Действие команды """

        raise NotImplementedError()


class ActivateTeapot(Command):
    def perform(self):
        self._teapot.activate()


class PourWater(Command):
    def perform(self):
        amount = input(f'Количество (число от 0 до {self._teapot.volume}): ')
        number = get_number_from_input(amount)
        self._teapot.pour_water(number)


class PourOutWater(Command):
    def perform(self):
        amount = input(f'Количество (число от 0 до {self._teapot.volume}): ')
        number = get_number_from_input(amount)
        self._teapot.pour_out_water(number)


class GetTeapotState(Command):
    def perform(self):
        logger.info(
            f'Чайник {self._teapot.state.value}. '
            f'Температура: {self._teapot.temperature}. '
            f'Количество воды: {self._teapot.amount_of_water}'
        )


class DeactivateTeapot(Command):
    def perform(self):
        self._teapot.state = TeapotState.INACTIVE
        exit(1)
