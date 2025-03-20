from fastapi import FastAPI
from routers.hotels import router as router_hotels

app = FastAPI()
app.include_router(router_hotels)
