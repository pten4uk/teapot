from enum import Enum
from typing import TypeVar


Seconds = TypeVar('Seconds', bound=int)
Liters = TypeVar('Liters', bound=float)


class TeapotState(Enum):
    INACTIVE = 'Выключен'
    ACTIVE = 'Включен'
    BOILED = 'Закипел'
    STOPPED = 'Остановлен'

