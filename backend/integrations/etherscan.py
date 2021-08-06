from re import search

from bs4 import BeautifulSoup
from requests import get

from integrations.uni import Uniswap

class Ether:
    '''Etherscan adaptor.'''

    def __init__(self, *args, **kwargs):
        self.base_url = 'https://etherscan.io/tokens?p={}'
        self.headers = {
            "authority": "etherscan.io",
            "cache-control": "max-age=0",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "sec-gpc": "1",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "navigate",
            "sec-fetch-user": "?1",
            "sec-fetch-dest": "document",
            "referer": "https://etherscan.io/tokens",
            "accept-language": "en-US,en;q=0.9",
            "cookie": "ASP.NET_SessionId=kqmzjmcfnxbowxxybaa1geih; __cflb=02DiuFnsSsHWYH8WqVXaqGvd6BSBaXQLTRKLTJUZ53xse; __stripe_mid=f5edd8f6-550e-49ed-bdee-b43aabfcbdd7a29e02"
        }
        self.anchors = []
        self.tokens = {}
        self.uni = Uniswap(address=None, private_key=None)


    def get_page(self, num=1):
        """Retrieves a etherscan page as a Soup object."""
        response = get(
            self.base_url.format(num),
            headers=self.headers
        )
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            return None
    
    def get_anchors(self, soup) -> list:
        self.anchors = soup.find_all('a')
    
    def get_max_pages(self) -> int:
        all_anchors = self.anchors
        link_anchor = [
            anchor for anchor in all_anchors if 'page-link' in anchor.attrs.get('class', [])
            and 'tokens?p' in anchor['href']
        ]
        max_page = max(
            map(int, [anchor['href'].replace('tokens?p=', '') for anchor in link_anchor])
        )

        return max_page

    def get_tokens_from_page(self):
        all_anchors = self.anchors
        token_anchor = [
            anchor for anchor in all_anchors if 'token' in anchor['href']
            and 'text-primary' in anchor.attrs.get('class', [])
        ]
        # data from tokens comes in format "name of token (symbol of token)"
        # the regex retrieves only the symbol of the token
        for token in token_anchor:
            symbol = search(r'(?<=\()[\w\d]+', token.text)
            if symbol is not None:
                symbol = symbol.group(0)
                address = token['href'].replace('/token/', '')
                self.tokens.update(
                    {
                       symbol: {
                           'address': address,
                           'decimals': None,
                       } 
                    }
                )
            else:
                print(f"Could not retrieve possible token: {token.text}")