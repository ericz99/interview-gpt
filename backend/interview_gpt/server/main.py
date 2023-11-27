from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import settings
from sockets.manager import socket_manager

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# mount socketio to fastapi
socket_manager.mount_to('/ws', app=app)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def root():
    return {"message": "Hello World!!!"}

print('hello world')