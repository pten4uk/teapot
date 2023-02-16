import time
from logging import getLogger

from teapot.exceptions import TeapotError
from teapot.types import TeapotState, Seconds, Liters
import config

logger = getLogger(__file__)


class Teapot:
    """
    Чайник обыкновенный.

    Использование:
    pour_water() - налить воды в чайник (без воды не запустится)
    activate() - включить чайник

    При KeyboardInterrupt нагрев чайника экстренно останавливается.
    """

    _state: TeapotState

    _MIN_TEMP = 0
    _MAX_TEMP = 100
    _DEFAULT_AMOUNT_OF_WATER = 0.0
    _DEFAULT_TEMPERATURE = 0
    _DEFAULT_STATE = TeapotState.INACTIVE

    def __init__(self, volume: Liters = config.VOLUME, boiling_time: Seconds = config.BOILING_TIME):
        """

        :param volume: Максимально допустимое количество воды в чайнике
        :param boiling_time: Время закипания чайника
        """

        self.state = self._DEFAULT_STATE
        self.temperature = self._DEFAULT_TEMPERATURE
        self.amount_of_water = self._DEFAULT_AMOUNT_OF_WATER

        self.volume = volume
        self.boiling_time = boiling_time

    @property
    def state(self) -> TeapotState:
        return self._state

    @state.setter
    def state(self, value: TeapotState):
        assert isinstance(value, TeapotState), 'Атрибут state должен быть типом TeapotState'
        self._state = value
        logger.info(f'Чайник {self.state.value}!')

    @property
    def temperature(self) -> int:
        return self._temperature

    @temperature.setter
    def temperature(self, value: int):
        if type(value) != int or not self._MIN_TEMP <= value <= self._MAX_TEMP:
            raise TeapotError(
                f'Температура может быть только целым числом в диапазоне от {self._MIN_TEMP} до {self._MAX_TEMP}'
                f' (Передано: {value})'
            )
        self._temperature = value

    @property
    def amount_of_water(self) -> Liters:
        return self._amount_of_water

    @amount_of_water.setter
    def amount_of_water(self, value: Liters):
        if not isinstance(value, Liters.__bound__):
            raise TeapotError('Некорректное значение количества воды')
        if hasattr(self, '_amount_of_water') and value > self.volume:
            raise TeapotError('Нельзя налить в чайник больше максимально допустимого значения')
        if hasattr(self, '_amount_of_water') and value < 0:
            raise TeapotError('Нельзя вылить больше воды чем есть в чайнике')

        self._amount_of_water = value

    @property
    def boiling_time(self):
        return self._boiling_time

    @boiling_time.setter
    def boiling_time(self, value: Seconds):
        if not isinstance(value, Seconds.__bound__) or value < 0:
            raise TeapotError('Атрибут boiling_time должен быть положительным числом')

        self._boiling_time = value

    def _calculate_temp_diff(self) -> int:
        """ Высчитывает, на какое количество градусов должна
        увеличиваться температура чайника каждую секунду """

        return self._MAX_TEMP // self.boiling_time

    def _check_can_be_activated(self):
        """ Проверяет может ли чайник быть включен """

        if self.amount_of_water == 0.0:
            raise TeapotError('Чайник пустой')

    def _check_amount(self, amount: Liters):
        """ Проверяет, что передано корректное значение литров воды.
        Выбрасывает исключение, если это не так """

        if type(amount) != int and type(amount) != float or amount <= 0:
            raise TeapotError('Недопустимое значение количества воды')

    def _run_heating(self):
        """ Запускает нагрев чайника """

        self.state = TeapotState.ACTIVE
        temp_diff = self._calculate_temp_diff()

        while self.temperature + temp_diff <= self._MAX_TEMP:
            time.sleep(1)
            self.temperature += temp_diff
            logger.info(f'Чайник нагревается... Температура: {self.temperature}')

        self.state = TeapotState.BOILED

    def pour_water(self, amount: Liters):
        """ Налить воды в чайник """

        self._check_amount(amount)
        self.amount_of_water += amount
        logger.info(f'Вода налита в чайник. Количество воды в чайнике: {self.amount_of_water}')

    def pour_out_water(self, amount: Liters):
        """ Вылить воду из чайника """

        self._check_amount(amount)
        self.amount_of_water -= amount
        logger.info(f'Вода вылита из чайника. Остаток: {self.amount_of_water}')

    def activate(self):
        self._check_can_be_activated()

        try:
            self._run_heating()
        except KeyboardInterrupt:
            self.state = TeapotState.STOPPED
            logger.info(f'Чайник остановлен! Температура: {self.temperature}')
