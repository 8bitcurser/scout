from json import loads, dumps
from random import choice
from time import sleep

from db import collection
from integrations.etherscan import Ether
from integrations.sushi import Sushi


async def update_tokens_info_fixture(
    tokens_dict: dict, token_1_symbol: str, token_2_symbol: str, key: str,
    val_1, val_2) -> dict:
    tokens_dict[token_1_symbol][key] = val_1
    tokens_dict[token_2_symbol][key] = val_2

    collection.update_one(
        {'ticker': token_1_symbol},
        {'$set': {key: val_1}}
    )
    collection.update_one(
        {'ticker': token_2_symbol},
        {'$set': {key: val_2}}
    )
    return tokens_dict


async def database_seed():
    ether = Ether()
    sushi = Sushi()
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
                sleep(choice([0.5, 0.4, 0.3, 0.2, 0.1]))
            else:
                break

        for token in ether.tokens:
            record = ether.tokens[token]
            record.update({'ticker': token})
            collection.insert_one(record)
        sushi.get_all_tokens()
    return {'data': 'Finished loading fixture'}