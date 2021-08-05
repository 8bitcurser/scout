from asyncio import create_task

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from helpers import token_addresses

from integrations.pancake import Pancake
from integrations.sushi import Sushi
from integrations.uni import Uni


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


@app.get('/price/{token_1}/{token_2}')
async def price(token_1: str, token_2: str):
    """Return exchange price for two given tickers on different platforms."""
    token_1 = token_1.lower()
    token_2 = token_2.lower()
    token_1_settings = token_addresses.get(token_1, '')
    token_2_settings = token_addresses.get(token_2, '')
    token_1_addr = token_1_settings[0]
    token_2_addr = token_2_settings[0]
    # for more details on this look at
    # https://github.com/uniswap-python/uniswap-python/issues/12
    # and https://github.com/uniswap-python/uniswap-python/issues/41
    min_unit_of_token_multiplier = token_1_settings[1]
    # Uniswap obtention
    uni = Uni()
    uni_res = await uni.get_pair_price(
        token_1_addr, token_2_addr, min_unit_of_token_multiplier
    )
    # Sushiswap obtention
    sushi = Sushi()
    sushi_res = await sushi.get_pairs(token_1, token_2)

    # Pancakeswap obtention
    pancake = Pancake()
    # pancake swap works with bep20 addresses we need to find those first.
    token_1_bep_addr = pancake.get_token(token_1)
    token_2_bep_addr = pancake.get_token(token_2)
    pancake_res = await pancake.get_pair(token_1_bep_addr, token_2_bep_addr)
    
    # conversion to decimal unit for uniswap response
    uni_res = uni_res / min_unit_of_token_multiplier
    
    res = {
        'uniswap': f'{token_1} vs {token_2} = {uni_res}',
        'sushiswap': f'{token_1} vs {token_2} = {sushi_res}',
        'pancakeswap': f'{token_1} vs {token_2} = {pancake_res}'
    }
    return res