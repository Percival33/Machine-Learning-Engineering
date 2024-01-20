import json
import os
from contextlib import asynccontextmanager
from enum import Enum
from subprocess import CalledProcessError

from fastapi import FastAPI, Query, Path, HTTPException
import uvicorn
from starlette.responses import RedirectResponse
from config import settings
from db import db
from lifespan import lifespan
from runner import run_model


class ModelName(str, Enum):
    BASE = "base"
    ADVANCED = "advanced"


env = None

app = FastAPI(lifespan=lifespan)


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")


@app.get("/predict/model/{model_type}")
async def predict_model(
    model_type: ModelName = Path(..., description="The model type"),
):
    try:
        output = run_model(model_type, settings.TRACKS_NO)
    except CalledProcessError:
        raise HTTPException(status_code=500, detail=output)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=output)

    if output.stderr:
        raise HTTPException(status_code=500, detail=f"Error in model: {output.stderr}")

    return {"model_type": model_type, "playlists": json.loads(output.stdout)}


@app.get("/next-playlist/{user_id}")
async def playlist(user_id: int):
    model = ModelName.ADVANCED if user_id % 2 else ModelName.BASE

    print(f"Used model: {model}")

    try:
        output = run_model(model, settings.TRACKS_NO)
    except CalledProcessError:
        raise HTTPException(status_code=500, detail=output)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=output)

    if output.stderr:
        raise HTTPException(status_code=500, detail=f"Error in model: {output.stderr}")

    return {"playlist": json.loads(output.stdout)}


if __name__ == "__main__":
    uvicorn.run("service:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG_MODE)
