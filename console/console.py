import time
from logging import getLogger
from typing import Optional

from console.commands import Command
from teapot.exceptions import TeapotError

logger = getLogger(__file__)


class Console:
    def __init__(self, commands: list[Command]):
        self._commands = self.__set_commands(commands)

    @staticmethod
    def __set_commands(commands: list[Command]):
        """ Проверяет корректность переданного списка команд """

        for command in commands:
            if not isinstance(command, Command):
                raise TypeError(f'Команда должна быть типом {Command}')

        return commands

    def _search_command(self, command_number: int) -> Optional[Command]:
        """ Ищет команду по номеру command_number """

        for command in self._commands:
            if command.get_number() == command_number:
                return command

    def __representate_command(self, command: Command):
        return f'{command.get_number()}. {command.get_description()}'

    def _representate_command_list(self):
        """ Приводит список команд строке с переносом каждой команды на новую строку """

        representation = ''
        for command in self._commands:
            representation += f'{self.__representate_command(command)}\n'

        return representation

    def _parse_command(self, command_input: str) -> Optional[Command]:
        """ Парсит команду из строки """

        try:
            parsed_command = int(command_input)
        except ValueError:
            logger.warning(f'Введите корректный номер команды!')
        else:
            command = self._search_command(parsed_command)
            return command

    def _perform_command(self, command_input: str):
        """ Выполняет команду по переданному номеру """

        command = self._parse_command(command_input)
        if command is not None:
            try:
                command.perform()
            except TeapotError as e:
                logger.error(e)
                time.sleep(1)

    def _wrap_representation(self, representation: str):
        """ Выделяет представление в консоли сверзу и снизу """

        wrapper = '----------------------------------------------'

        return f'{wrapper}\n{representation}{wrapper}\n'

    def _output_to_console(self):
        """ Выводит в консоль подсказки по командам """

        commands = self._wrap_representation(self._representate_command_list())
        print(commands)

    def start(self):
        print(
            '--------------------------------------------\n'
            'Интерактивный чайник приветствует тебя!\n'
            'Выбери нужное действие из списка ниже и введи номер этого действия :)'
        )
        while True:
            self._output_to_console()
            command_input = input('Введите номер команды: >>> ')
            self._perform_command(command_input)
