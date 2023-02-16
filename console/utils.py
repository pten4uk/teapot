from logging import getLogger

from teapot.exceptions import TeapotError

logger = getLogger(__file__)


def get_number_from_input(string: str):
    """ Приводит строку string к типу float, возвращает  """

    try:
        amount = float(string)
    except ValueError:
        raise TeapotError('Ошибка! Нужно ввести число')
    else:
        return amount
