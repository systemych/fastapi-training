from fastapi import FastAPI

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotels

app = FastAPI()
app.include_router(router_hotels)
