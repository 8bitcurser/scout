from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from json import dumps

from helpers import token_addresses

from integrations.pancake import Pancake
from integrations.sushi import Sushi
from integrations.uni import uniswap


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
    """Return price for two given tickers"""
    token_1_settings = token_addresses.get(token_1.lower(), '')
    token_2_settings = token_addresses.get(token_2.lower(), '')
    token_1_addr = token_1_settings[0]
    token_2_addr = token_2_settings[0]
    # for more details on this look at https://github.com/uniswap-python/uniswap-python/issues/12
    # and https://github.com/uniswap-python/uniswap-python/issues/41
    min_unit_of_token_multiplier = token_1_settings[1]
    # Uniswap obtention
    uni_res = uniswap.get_price_input(
        token_1_addr, token_2_addr, min_unit_of_token_multiplier
    )
    # conversion to decimal unit
    uni_res = uni_res / min_unit_of_token_multiplier
    # Sushiswap obtention
    sushi = Sushi()
    sushi_pairs = sushi.get_all_pairs()

    # Pairs in uniswap are not necessarily generated in a particular order
    # therefor usdt/usdc could be swapped into usdc/usdt but only 1 pair with
    # both contracts will exist.
    look_pair = [
        pair for pair in sushi_pairs
        if (
            pair['Token_1_symbol'].lower() == token_1.lower() and
            pair['Token_2_symbol'].lower() == token_2.lower()
        ) or (
            pair['Token_2_symbol'].lower() == token_1.lower() and
            pair['Token_1_symbol'].lower() == token_2.lower()
        ) 
    ]


    if look_pair:
        if len(look_pair) == 1:
            # As pairs are not necessarily in the correct order the prices aren't either
            # we need to divide in the proper order.
            if look_pair[0]["Token_1_symbol"].lower() == token_1.lower():
                sushi_res = look_pair[0]["Token_1_price"] / look_pair[0]["Token_2_price"]
            else:
                sushi_res = look_pair[0]["Token_2_price"] / look_pair[0]["Token_1_price"]
        else:
            sushi_res = "Too many results"
    else:
        sushi_res = None

    pancake = Pancake()
    token_1_bep_addr = pancake.get_token(token_1.lower())
    token_2_bep_addr = pancake.get_token(token_2.lower())
    pancake_res = pancake.get_pair(token_1_bep_addr, token_2_bep_addr)
    res = {
        'uniswap': f'{token_1} vs {token_2} = {uni_res}',
        'sushiswap': f'{token_1} vs {token_2} = {sushi_res}',
        'pancakeswap': f'{token_1} vs {token_2} = {pancake_res}'
    }
    return dumps(res)