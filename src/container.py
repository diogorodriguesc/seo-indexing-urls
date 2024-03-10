import yaml

from configuration import Configuration
from logger.formatters.text_formatter import TextFormatter
from logger.logger import Logger
from logger.logger_interface import LoggerInterface

CONFIG_FILES = {'dev': '../config/dev/parameters.yaml', 'prod': '../config/prod/parameters.yaml'}
ENVIRONMENTS = ['dev', 'test', 'prod']


class Container:
    __logger: any
    __environment: str
    __parameters: dict
    __configuration: any

    def __init__(self, environment: str) -> None:
        self.__configuration = self.__logger = None
        if environment not in ENVIRONMENTS:
            raise Exception(f'Environment {environment} is not valid! It must be one of: {ENVIRONMENTS}')

        self.__environment = environment
        with open(CONFIG_FILES.get(environment), 'r') as file:
            self.__parameters = yaml.safe_load(file)['parameters']

        self.get_logger().info(f'Environment selected: {self.__environment}')

    def get_logger(self) -> LoggerInterface:
        if self.__logger is None:
            self.__logger = Logger(self.get_parameters().get('logger'), TextFormatter())

        return self.__logger
    
    def get_google_configuration(self) -> Configuration:
        if self.__configuration is None:
            self.__configuration = Configuration(self.get_parameters().get('google'), self.get_logger())

        return self.__configuration
    
    def get_parameters(self) -> dict:
        return self.__parameters
