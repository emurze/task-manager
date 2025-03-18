from fastapi import APIRouter
from starlette import status

router = APIRouter()


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    response_model=dict,
)
async def health():
    return {"status": "ok"}
