from requests import get

class Sushi:
    '''Sushiswap adaptor.'''

    def __init__(self, *args, **kwargs):
        self.base_url = 'https://api2.sushipro.io?action={}'

    def get_pairs(self, token_1, token_2):
        all_pairs_url = self.base_url.format('all_pairs')
        res = get(all_pairs_url)
        if res.status_code == 200:
            sushi_pairs = res.json()[1]
            # Pairs in uniswap are not necessarily generated in a particular order
            # therefor usdt/usdc could be swapped into usdc/usdt but only 1 pair with
            # both contracts will exist.
            look_pair = [
                pair for pair in sushi_pairs
                if (
                    pair['Token_1_symbol'].lower() == token_1 and
                    pair['Token_2_symbol'].lower() == token_2
                ) or (
                    pair['Token_2_symbol'].lower() == token_1 and
                    pair['Token_1_symbol'].lower() == token_2
                ) 
            ]

            if look_pair:
                if len(look_pair) == 1:
                    # As pairs are not necessarily in the correct order the prices aren't either
                    # we need to divide in the proper order.
                    if look_pair[0]["Token_1_symbol"].lower() == token_1:
                        sushi_res = look_pair[0]["Token_1_price"] / look_pair[0]["Token_2_price"]
                    else:
                        sushi_res = look_pair[0]["Token_2_price"] / look_pair[0]["Token_1_price"]
                else:
                    sushi_res = "Too many results"
            else:
                sushi_res = None
        else:
            sushi_res = None
        return sushi_res