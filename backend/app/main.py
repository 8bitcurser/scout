from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    'http://localhost:8080'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods=['GET'],
    allow_headers=['*']
)

@app.get("/")
async def root(req: Request):
    return req.json