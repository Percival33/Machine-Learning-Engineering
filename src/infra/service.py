import json
import os
from contextlib import asynccontextmanager
from enum import Enum
from fastapi import FastAPI, Query, Path, HTTPException
import uvicorn
from subprocess import run, CalledProcessError

from starlette.responses import RedirectResponse


class ModelName(str, Enum):
    base = "base"
    advanced = "advanced"


env = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    dataset_path = os.path.join(os.path.dirname(__file__), "..", "data", "make_dataset.py")
    run(["python", dataset_path])
    print(os.getcwd())
    global env
    env = os.environ.copy()
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    env["PYTHONPATH"] = f'{root_dir}:{os.path.join(root_dir, "src")}'
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/", include_in_schema=False)
async def index():
    return RedirectResponse(url="/docs")


@app.get("/predict/model/{model_type}")
async def predict_model(
    model_type: ModelName = Path(..., description="The model type"),
    tracks: int = Query(10, description="Number of tracks", ge=10, le=20),
):
    model_path = os.path.join(
        os.path.dirname(__file__), "..", "models", f"{model_type.value}_model.py"
    )
    print(model_path, env)
    try:
        result = run(
            ["python", model_path, str(tracks)],
            capture_output=True,
            text=True,
            check=True,
            env=env,
        )
    except CalledProcessError as e:
        print(e.output, e.stderr, e.stdout)
        raise HTTPException(status_code=500, detail=f"Model script execution failed: {e.output}")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Invalid model type")

    if result.stderr:
        raise HTTPException(status_code=500, detail=f"Error in model: {result.stderr}")

    return {"model_type": model_type, "playlists": json.loads(result.stdout)}


if __name__ == "__main__":
    uvicorn.run("service:app", host="0.0.0.0", port=8000, reload=True)
