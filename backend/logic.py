from json import loads
from asyncio import create_task
from typing import Collection

from db import collection
from helpers import update_tokens_info_fixture
from integrations.pancake import Pancake
from integrations.sushi import Sushi
from integrations.uni import Uni
from schemas import Transaction


async def get_price(token_1: str, token_2: str):
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
        token_1_settings = collection.find_one({'ticker': token_1})
        token_2_settings = collection.find_one({'ticker': token_2})
        
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
        res = {'data': 'Could not retrieve tokens, try calling the seed endpoint => "/seed"'}
    return res


# This will be migrated to Vue.JS front end for simplicity.
def swap(trx: Transaction):
    '''
        Performs swap operation between two tokens at a given swap platform
        for a given amount, expressed on token_1.
        Test it as:
        >> curl -X POST -H "Content-Type: application/json" -d\
        '{"token_1": "test1", "token_2": "test2", "swap": "testswap", "amount": , "wallet":"testaddress", "private_key": "sample"}'\
        0.0.0.0:8000/trx

        {"tokens": "test1 vs test2", "swap_platform":"testswap", "amount_to_be_swapped":"10.5 in test1", "dry_run":true}
    '''
    if trx.wallet and trx.private_key:
        if trx.dry_run:
            res = {
                'tokens': f'{trx.token_1} vs {trx.token_2}',
                'swap_platform': f'{trx.swap}',
                'amount_to_be_swapped': f'{trx.amount} in {trx.token_1}',
                'dry_run': True
            }
        else:
            res = {
                'tokens': f'{trx.token_1} vs {trx.token_2}',
                'swap_platform': f'{trx.swap}',
                'amount_to_be_swapped': f'{trx.amount} in {trx.token_1}',
                'dry_run': False
            }
    else:
        res = {
            'data': (
                'Set up a wallet address and its private key at your own .env file, or add the keys'
                ' wallet and private_key to the BODY of the request.'
            )
        }

    return res