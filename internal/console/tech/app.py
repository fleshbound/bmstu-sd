from dependency_injector.wiring import Provide, inject

from container import Container
from tech.console import ConsoleHandler
from utils.logger.logger import set_logger


@inject
def main(console: ConsoleHandler = Provide[Container.console_handler]) -> None:
    console.run()


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__])
    set_logger()
    main()
