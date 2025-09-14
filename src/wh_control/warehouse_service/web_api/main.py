from fastapi import FastAPI

from .auth import router as auth_router
from .dependencies import set_dependency_injection
from warehouse_service.configure_logging import configure_logger


def init_app() -> FastAPI:
    app = FastAPI()
    configure_logger()
    set_dependency_injection(app)
    app.include_router(auth_router)
    return app
