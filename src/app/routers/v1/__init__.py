from fastapi import APIRouter

from .user_router import router as user_router

v1_routers = APIRouter(prefix="/v1")
v1_routers.include_router(user_router)
