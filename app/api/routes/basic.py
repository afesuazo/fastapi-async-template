from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def index() -> str:
    return "Hello World!"
