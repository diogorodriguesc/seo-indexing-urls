from abc import abstractmethod
from typing import final

from logger.formatters import FormatterInterface

LOG_LEVELS = ['critical', 'error', 'warning', 'info', 'debug']


class LoggerInterface:
    @abstractmethod
    def critical(self, message: str) -> str:
        """Logs critical message into specific output channel."""

    @abstractmethod
    def error(self, message: str) -> str:
        """Logs error message into specific output channel."""

    @abstractmethod
    def warning(self, message: str) -> str:
        """Logs warning message into specific output channel."""

    @abstractmethod
    def info(self, message: str) -> str:
        """Logs info message into specific output channel."""

    @abstractmethod
    def debug(self, message: str) -> str:
        """Logs debug message into specific output channel."""


@final # pylint: disable=using-final-decorator-in-unsupported-version
class Logger(LoggerInterface):
    __fingers_cross: bool
    __fingers_cross_log_level: str
    __log_queue: list = []
    __formatter: FormatterInterface

    def __init__(self, config: dict, formatter: FormatterInterface) -> None:
        log_level = config.get('fingers_cross_log_level')
        fingers_cross = config.get('fingers_cross', False)

        if fingers_cross and log_level not in LOG_LEVELS:
            raise Exception(f'fingers cross error level is invalid. The valid log levels are {LOG_LEVELS}')
        self.__fingers_cross_log_level = log_level

        self.__fingers_cross = fingers_cross
        self.__formatter = formatter

    def critical(self, message: str) -> None:
        self.__release_message(self.__formatter.format(message, 'critical'), 'critical')

    def error(self, message: str) -> None:
        self.__release_message(self.__formatter.format(message, 'error'), 'error')

    def warning(self, message: str) -> None:
        self.__release_message(self.__formatter.format(message, 'warning'), 'warning')

    def info(self, message: str) -> None:
        self.__release_message(self.__formatter.format(message, 'info'), 'info')

    def debug(self, message: str) -> None:
        self.__release_message(self.__formatter.format(message, 'debug'), 'debug')

    def __release_message(self, message: str, log_level: str) -> None:
        if self.__fingers_cross is True:
            if log_level == self.__fingers_cross_log_level:
                self.__log_queue.append(message)
            else:
                for log in self.__log_queue:
                    print(log)
                print(message)

                self.__log_queue = []
        else:
            print(message)
