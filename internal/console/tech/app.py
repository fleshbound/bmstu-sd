from dependency_injector.wiring import Provide
from fastapi import Depends

from container import Container
from tech.console import ConsoleHandler


container = Container()


def main(console: ConsoleHandler = Depends(Provide[Container.console_handler])) -> None:
    console.run()


if __name__ == '__main__':
    main()
