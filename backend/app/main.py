from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
async def root(req: Request):
    return req.json