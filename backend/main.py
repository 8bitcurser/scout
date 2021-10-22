from asyncio import create_task

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from helpers import database_seed
from logic import get_price
from schemas import Transaction

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

@app.get("/seed")
async def seed_tokens():
    '''
        Creates a seeded fixture with the tokens from etherscan.io and seeds the information
        with sushiswap addresses.
    '''
    create_task(database_seed())
    return {'data': 'Database seeding is scheduled, return in around ~2 minutes.'}

@app.get('/price/{token_1}/{token_2}')
async def price(token_1: str, token_2: str):
    return await get_price(token_1, token_2)

@app.post('/trx')
async def swap(trx: Transaction):
    return swap(trx)