from fastapi import FastAPI

from .auth import router as auth_router
from .dependencies import set_dependency_injection


def init_app() -> FastAPI:
    app = FastAPI()
    set_dependency_injection(app)
    app.include_router(auth_router)
    return app
