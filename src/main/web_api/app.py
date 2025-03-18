from fastapi import FastAPI

from api.routers import router
from main.container.app import create_application
from seedwork.config import Config


def create_app(config: Config = Config()) -> FastAPI:
    application = create_application(config)
    app = FastAPI(application=application)
    app.include_router(router)
    return app
