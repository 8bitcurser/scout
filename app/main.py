from typing import Optional

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="app/templates")
app = FastAPI()


@app.get("/")
async def root(req: Request):
    template = templates.TemplateResponse(
        "index.html",
        {'request': req}
    )

    return template