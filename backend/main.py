from json import dumps, loads
from re import search
from time import sleep


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from requests import get

from integrations.etherscan import Ether
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
async def seed_tokens():
    ether = Ether()
    main_page = ether.get_page()
    if main_page is not None:
        ether.get_anchors(main_page)
        max_page = ether.get_max_pages()
        pages = list(range(2, max_page+1))
        ether.get_tokens_from_page()
        for page in pages:
            page = ether.get_page(num=page)
            ether.get_anchors(page)
            if page is not None:
                ether.get_tokens_from_page()
                sleep(0.5)
            else:
                ret = "Could not retrieve information from etherscan.io"
                break

        with open('fixtures_tokens.json', 'w') as fix:
            fix.write(dumps(ether.tokens, sort_keys=True, indent=4))
        
        ret = "Succesfully seeded platform with tokens"
        
    else:
        ret = 'Could not retrieve information from etherscan.io'

    return {'data': ret}


@app.get('/price/{token_1}/{token_2}')
async def price(token_1: str, token_2: str):
    """Return exchange price for two given tickers on different platforms."""
    token_1 = token_1.lower()
    token_2 = token_2.lower()

    sushi = Sushi()
    uni = Uni()
    pancake = Pancake()    

    with open('fixtures_tokens.json', 'r') as fix:
        sanitized_addresses_dict = loads(fix.read())

    if sanitized_addresses_dict:
        token_1_settings = sanitized_addresses_dict.get(token_1, {})
        token_2_settings = sanitized_addresses_dict.get(token_2, {})

        token_1_addr = token_1_settings.get('contract')
        token_2_addr = token_2_settings.get('contract')
        # for more details on this look at
        # https://github.com/uniswap-python/uniswap-python/issues/12
        # and https://github.com/uniswap-python/uniswap-python/issues/41
        min_unit_of_token_multiplier = 10**token_1_settings.get('decimals')
        # Uniswap obtention
        uni_res = await uni.get_pair_price(
            token_1_addr, token_2_addr, min_unit_of_token_multiplier
        )
        # Sushiswap obtention    
        sushi_res = await sushi.get_pairs(token_1, token_2)

        # Pancakeswap obtention
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
    else:
        res = {'data': 'Could not retrieve tokens, try calling the root endpoint "/"'}
    return res