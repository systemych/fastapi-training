from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.init import redis_manager

from src.api.auth import router as router_auth
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.options import router as router_options

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    yield
    await redis_manager.close()

app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_options)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)