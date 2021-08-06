from uniswap import Uniswap
from web3 import Web3


class Uni:
    def __init__(self, *args, **kwargs):
        # or None if you're not going to make transactions
        self.address = None
        # or None if you're not going to make transactions
        self.private_key = None
        # specify which version of Uniswap to use
        self.version = 3
        # can also be set through the environment variable `PROVIDER`
        self.uniswap = Uniswap(
            address=self.address, private_key=self.private_key,
            version=self.version
        )
    
    async def get_pair_price(self, token_1_addr, token_2_addr, decimals):
        token_1_addr = Web3.toChecksumAddress(token_1_addr)
        token_2_addr = Web3.toChecksumAddress(token_2_addr)

        ret = self.uniswap.get_price_input(
            token_1_addr, token_2_addr, decimals
        )

        return ret

    def get_token(self, token_address):
        ret = self.uniswap.get_token(token_address)
        return ret
