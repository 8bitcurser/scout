from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/{name}")
def root(name: str = "World"):
    return {"Welcome": f"{name}"}