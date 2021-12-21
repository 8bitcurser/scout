from json import dumps, loads

from requests import get

from db import collection

class Sushi:
    '''Sushiswap adaptor.'''

    def __init__(self, *args, **kwargs):
        self.base_url = 'https://api2.sushipro.io?action={}'


    def get_all_tokens(self):
        all_tokens_url = self.base_url.format('all_tokens')
        res = get(all_tokens_url)
        if res.status_code == 200:
            tokens = res.json()[1]
            for token in tokens:
                collection.update_one(
                    {'ticker': token['Symbol']},
                    { '$set': {'sushi_address': token['Contract']}}
                )
            return "Success seeding fixtures with sushiswap data"
        else:
            return "Failed to seed fixtures with sushiswap data"

    async def get_pairs(self, token_1, token_2):
        t1 = collection.find_one({'ticker': token_1})
        t2 = collection.find_one({'ticker': token_2})
        address_t1 = t1.get('sushi_address', '')
        address_t2 = t2.get('sushi_address', '')
        sushi_pairs = []
        all_pairs_url_t1 = self.base_url.format(f'get_pairs_by_token&token={address_t1}')
        res_1 = get(all_pairs_url_t1)
        all_pairs_url_t2 = self.base_url.format(f'get_pairs_by_token&token={address_t2}')
        res_2 = get(all_pairs_url_t2)
        pairs_1 = res_1.json()[1] if res_1.status_code == 200 else []
        pairs_2 = res_2.json()[1] if res_2.status_code == 200 else []
        sushi_pairs.extend(pairs_1)
        sushi_pairs.extend(pairs_2)
        
        # Pairs in uniswap are not necessarily generated in a particular order
        # therefor usdt/usdc could be swapped into usdc/usdt but only 1 pair with
        # both contracts will exist.
        look_pair = [
            pair for pair in sushi_pairs
            if (
                pair['Token_1_symbol'] == token_1 and
                pair['Token_2_symbol'] == token_2
            ) or (
                pair['Token_2_symbol'] == token_1 and
                pair['Token_1_symbol'] == token_2
            ) 
        ]
        if look_pair:
            # As pairs are not necessarily in the correct order the prices aren't either
            # we need to divide in the proper order.
            look_pair = look_pair[0]
            
            if look_pair["Token_1_symbol"] == token_1:
                sushi_res = look_pair["Token_2_price"]
            else:
                sushi_res = look_pair["Token_1_price"]
        else:
            sushi_res = None

        return sushi_res