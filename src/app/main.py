from os import makedirs

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from src.app.core import app_lifespan, settings
from src.app.exceptions import mount_exception_handler
from src.app.routers import api_routers

app = FastAPI(lifespan=app_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOW_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)

makedirs("static", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), "static")
mount_exception_handler(app)
app.include_router(api_routers)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

print(settings.ALLOW_ORIGINS)
