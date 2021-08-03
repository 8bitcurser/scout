from uniswap import Uniswap


# or None if you're not going to make transactions
address = None
# or None if you're not going to make transactions
private_key = None
# specify which version of Uniswap to use
version = 3
# can also be set through the environment variable `PROVIDER`
provider = "https://mainnet.infura.io/v3/441ffc385a06434f9facf1956bb24ab8"
uniswap = Uniswap(address=address, private_key=private_key, version=version, provider=provider)
