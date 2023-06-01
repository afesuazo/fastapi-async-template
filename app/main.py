from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def build_app() -> FastAPI:
    application = FastAPI(title="App", debug=True, version="1.0")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return application


app = build_app()
