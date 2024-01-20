import os
from contextlib import asynccontextmanager
from subprocess import run

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    dataset_path = os.path.join(os.path.dirname(__file__), "..", "data", "make_dataset.py")
    run(["python", dataset_path])
    print(os.getcwd())
    yield
