from typing import Optional

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

app.mount("/statics", StaticFiles(directory="statics"), name="statics")

@app.get("/")
async def root(req: Request):
    template = templates.TemplateResponse(
        "index.html",
        {'request': req}
    )

    return template