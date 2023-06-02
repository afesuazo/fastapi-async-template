from fastapi import APIRouter

from app.api.routes import basic

api_router = APIRouter()

api_router.include_router(basic.router, tags=["basic"])
