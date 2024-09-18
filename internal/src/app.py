import time

from fastapi import FastAPI, Request

from container.container import Container
from api.router.animal import router as router_animal
from api.router.user import router as router_user
from api.router.show import router as router_show
from api.router.auth import router as router_auth
from api.router.score import router as router_score


class AppCreator:
    def __init__(self):
        self.app = FastAPI()
        self.container = Container()

        @self.app.get("/")
        def root():
            return "app is working"

        @self.app.middleware("http")
        async def add_process_time_header(request: Request, call_next):
            start_time = time.time()
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response

        self.app.include_router(router_animal)
        self.app.include_router(router_user)
        self.app.include_router(router_show)
        self.app.include_router(router_auth)
        self.app.include_router(router_score)


app_creator = AppCreator()
app = app_creator.app