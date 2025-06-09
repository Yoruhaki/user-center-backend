from src.app.common import StatusCode


class BusinessException(Exception):

    def __init__(self, error_code: StatusCode, description: str = "") -> None:
        self.__code = error_code.value.code
        self.__message = error_code.value.message
        self.__description = description
        super().__init__(self.__code, self.__message, description)


    @property
    def code(self) -> int:
        return self.__code

    @property
    def description(self) -> str:
        return self.__description

    @property
    def message(self) -> str:
        return self.__message
