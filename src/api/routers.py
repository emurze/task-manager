from fastapi import APIRouter

from api.tasks.router import router as tasks_router
from api.health.router import router as health_router

router = APIRouter()
router.include_router(tasks_router)
router.include_router(health_router)
