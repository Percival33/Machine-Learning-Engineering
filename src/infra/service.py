import json
import subprocess
from enum import Enum
from subprocess import CalledProcessError

from fastapi import FastAPI, Path, HTTPException, Depends
import uvicorn
from starlette.responses import RedirectResponse
from config import settings
from lifespan import lifespan
from runner import run_model


class ModelName(str, Enum):
    BASE = "base"
    ADVANCED = "advanced"


app = FastAPI(lifespan=lifespan)


async def run_model_dependency(model_type: ModelName):
    try:
        output = await run_model(model_type, settings.TRACKS_NO)
        if output.stderr:
            raise HTTPException(status_code=500, detail=f"Error in model: {output.stderr}")
        return output
    except CalledProcessError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


async def run_model_for_user(user_id: int):
    model_type = ModelName.ADVANCED if user_id % 2 else ModelName.BASE
    # print(model_type)
    return await run_model_dependency(model_type)


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")


@app.get("/predict/model/{model_type}")
async def predict_model(
    model_type: ModelName = Path(..., description="The model type"),
    output: subprocess.CompletedProcess = Depends(run_model_dependency),
):
    return {"model_type": model_type, "playlists": json.loads(output.stdout)}


@app.get("/playlists/{user_id}")
async def playlist(
    user_id: int, output: subprocess.CompletedProcess = Depends(run_model_for_user)
):
    return {"playlist": json.loads(output.stdout)}


if __name__ == "__main__":
    uvicorn.run("service:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG_MODE)
