from requests import get

class Pancake:
    '''Pancakeswap adaptor.'''

    def __init__(self, *args, **kwargs):
        self.base_url = 'https://api.pancakeswap.info/api/v2/{action}'

    async def get_pair(self, token_1, token_2):
        tokens_url = self.base_url.format(action='tokens')
        tokens_1_url = f"{tokens_url}/{token_1}"
        tokens_2_url = f"{tokens_url}/{token_2}"
        res_tokens_1 = get(tokens_1_url)
        res_tokens_2 = get(tokens_2_url)

        if res_tokens_1.status_code == 200 and res_tokens_2.status_code == 200:
            price_token_1 = res_tokens_1.json()['data']['price']
            price_token_2 = res_tokens_2.json()['data']['price']
            ret = float(price_token_1) / float(price_token_2)
        else:
            ret = None
        return ret
    
    def get_token(self, token_name: str = None):
        tokens_url = self.base_url.format(action='tokens')
        res = get(tokens_url)
        if res.status_code == 200:
            ret = res.json()['data']
            if token_name is not None:
                token = [
                    token for token in ret
                    if ret[token]['symbol'].lower() == token_name
                ]
                ret = token[0] if token else {}
        else:
            ret = {}
        return ret
