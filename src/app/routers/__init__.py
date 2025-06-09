from fastapi import APIRouter

from .v1 import v1_routers

api_routers = APIRouter(prefix="/api")
api_routers.include_router(v1_routers)
