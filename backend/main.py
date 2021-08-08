from asyncio import create_task
from json import loads

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from helpers import create_tokens_fixture, update_tokens_info_fixture

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

@app.get("/seed")
async def seed_tokens():
    create_task(create_tokens_fixture())

    return {'data': 'Fixtures creation is scheduled, return in around ~5 minutes.'}


@app.get('/price/{token_1}/{token_2}')
async def price(token_1: str, token_2: str):
    """Return exchange price for two given tickers on different platforms."""
    token_1 = token_1.upper()
    token_2 = token_2.upper()

    sushi = Sushi()
    uni = Uni()
    pancake = Pancake()    

    with open('fixtures_tokens.json', 'r') as tokens:
        cached_fixture = loads(tokens.read())

    sanitized_addresses = cached_fixture

    if sanitized_addresses:
        token_1_settings = sanitized_addresses.get(token_1, {})
        token_2_settings = sanitized_addresses.get(token_2, {})
        
        token_1_addr = token_1_settings.get('address')
        token_2_addr = token_2_settings.get('address')

        # Obtain uniswap tokens addresses
        token_1_uni_address = sanitized_addresses.get(token_1, {}).get('uni_address')
        token_2_uni_address = sanitized_addresses.get(token_2, {}).get('uni_address')
    
        # Retrieve them if they do not exist on the fixture and update the file
        if token_1_uni_address is None or token_2_uni_address is None:
            if token_1_uni_address is None:
                token_1_uni_address = uni.get_token(token_1_addr).address
            
            if token_2_uni_address is None:
                token_2_uni_address = uni.get_token(token_2_addr).address
            
            create_task(update_tokens_info_fixture(
                sanitized_addresses,
                token_1,
                token_2,
                'uni_address',
                token_1_uni_address,
                token_2_uni_address
            ))
    
        # Retrieve decimals from each token to reproduce the correct value of the
        # exchange. For more details on this look at
        # https://github.com/uniswap-python/uniswap-python/issues/12
        # and https://github.com/uniswap-python/uniswap-python/issues/41
        decimals_1 = token_1_settings.get('decimals')
        decimals_2 = token_2_settings.get('decimals') 
        
        if decimals_1 is None or decimals_2 is None:
            if  decimals_1 is None:
                decimals_1 = uni.get_token(token_1_uni_address).decimals

            if decimals_2 is None:
                decimals_2 = uni.get_token(token_2_uni_address).decimals
        
            create_task(update_tokens_info_fixture(
                sanitized_addresses,
                token_1,
                token_2,
                'decimals',
                decimals_1,
                decimals_2
            ))

        min_unit_of_token_multiplier = 10 ** decimals_1

        # Uniswap price obtention
        uni_res = await uni.get_pair_price(
            token_1_uni_address,
            token_2_uni_address,
            min_unit_of_token_multiplier
        )
        # Sushiswap price obtention    
        sushi_res = await sushi.get_pairs(token_1, token_2)

        # Obtain Pancakeswap tokens addresses
        token_1_bep_address = sanitized_addresses.get(token_1, {}).get('bep_address')
        token_2_bep_address = sanitized_addresses.get(token_2, {}).get('bep_address')

        # Retrieve them if they do not exist on the fixture and update the file
        if token_1_bep_address is None or token_2_bep_address is None:
            if token_1_bep_address is None:
                token_1_bep_address = pancake.get_token(token_1)
            
            if token_2_bep_address is None:
                token_2_bep_address = pancake.get_token(token_2)
            
            create_task(update_tokens_info_fixture(
                sanitized_addresses,
                token_1,
                token_2,
                'bep_address',
                token_1_bep_address,
                token_2_bep_address
            ))
    
        # Pancakeswap price obtention
        pancake_res = await pancake.get_pair(
            token_1_bep_address,
            token_2_bep_address
        )

        res = {
            'uniswap': f'{token_1} vs {token_2} = {uni_res / (10 ** decimals_2)}',
            'sushiswap': f'{token_1} vs {token_2} = {sushi_res}',
            'pancakeswap': f'{token_1} vs {token_2} = {pancake_res}'
        }
    else:
        res = {'data': 'Could not retrieve tokens, try calling the root endpoint "/"'}
    return res