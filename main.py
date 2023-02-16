import logging
import os
import sys
from pathlib import Path

from console.console import Console
from console.commands import ActivateTeapot, PourWater, PourOutWater, GetTeapotState, DeactivateTeapot

sys.path.append(os.path.join(Path(__file__).resolve().parent, ''))

from teapot.teapot import Teapot


fmt = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Логгирование в консоль
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
sh.setFormatter(fmt)

# Логгирование в файл
fh = logging.FileHandler('info.log')
fh.setLevel(logging.INFO)
fh.setFormatter(fmt)

logger_teapot = logging.getLogger()
logger_teapot.setLevel(logging.INFO)

logger_teapot.addHandler(sh)
logger_teapot.addHandler(fh)


def main():
    teapot = Teapot()

    console = Console([
        ActivateTeapot(teapot=teapot, number=1, description='Включить чайник'),
        PourWater(teapot=teapot, number=2, description='Налить воды в чайник'),
        PourOutWater(teapot=teapot, number=3, description='Вылить воду из чайника'),
        GetTeapotState(teapot=teapot, number=4, description='Состояние чайника'),
        DeactivateTeapot(teapot=teapot, number=5, description='Отключить чайник')
    ])

    console.start()


if __name__ == '__main__':
    main()
