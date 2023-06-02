from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.base import api_router


def build_app() -> FastAPI:
    application = FastAPI(title="App", debug=True, version="1.0")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(api_router)
    return application


app = build_app()
