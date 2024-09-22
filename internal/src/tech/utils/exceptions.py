from typing import Any


class InputException(Exception):
    def __init__(self, detail: Any = None):
        super().__init__(detail)


class CancelInput(InputException):
    def __init__(self, detail: Any = None):
        super().__init__(detail)


class InvalidFloatInput(InputException):
    def __init__(self, detail: Any = None):
        super().__init__(detail)


class InvalidSexInput(InputException):
    def __init__(self, detail: Any = None):
        super().__init__(detail)


class InvalidScoreInput(InputException):
    def __init__(self, detail: Any = None):
        super().__init__(detail)


class InvalidBooleanInput(InputException):
    def __init__(self, detail: Any = None):
        super().__init__(detail)
