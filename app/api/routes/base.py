from fastapi import APIRouter

from app.api.routes import basic, users

api_router = APIRouter()

api_router.include_router(basic.router, tags=["basic"])
api_router.include_router(users.router, tags=["users"], prefix="/users")
