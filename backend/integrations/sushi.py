from requests import get

class Sushi:
    '''Sushiswap adaptor.'''

    def __init__(self, *args, **kwargs):
        self.base_url = 'https://api2.sushipro.io?action={}'

    def get_all_pairs(self):
        all_pairs_url = self.base_url.format('all_pairs')
        res = get(all_pairs_url)
        if res.status_code == 200:
            ret = res.json()[1]
        else:
            ret = []
        return ret