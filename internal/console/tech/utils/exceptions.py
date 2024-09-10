from typing import Any


class CancelInput(Exception):
    def __init__(self, detail: Any = None):
        super().__init__(detail)
