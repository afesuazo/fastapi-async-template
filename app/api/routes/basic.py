from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def ping() -> dict[str, str]:
    return {"ping": "pong!"}
