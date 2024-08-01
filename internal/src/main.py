import time

from fastapi import FastAPI, Request

from container import Container
from core.animal.api.router.animal import router as router_animal
from core.user.api.router.user import router as router_user
from core.group.api.router.group import router as router_group
from core.species.api.router.species import router as router_species
from core.breed.api.router.breed import router as router_breed


class AppCreator:
    def __init__(self):
        self.app = FastAPI()
        self.container = Container()

        @self.app.get("/")
        def root():
            return "service is working"

        @self.app.middleware("http")
        async def add_process_time_header(request: Request, call_next):
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response

        self.app.include_router(router_animal)
        self.app.include_router(router_user)
        self.app.include_router(router_breed)
        self.app.include_router(router_species)
        self.app.include_router(router_group)


app_creator = AppCreator()
app = app_creator.app