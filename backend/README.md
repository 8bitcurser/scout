## Mounting the project for development

1. Create python virtual environment `python3 -m venv env`
2. Create a .env file the backend folder with the following statement `PROVIDER={YOUR w3 PROVIDER URL}`
3. Activate it `source ./env/bin/activate`
4. Build requirements `pip3 -m requirements.txt`
5. Run project from within backend folder `uvicorn main:app --reload`


## Current endpoints

### Root: [GET] /

This is the root endpoint, it returns an empty json object.

*Can be accessed through*: `localhost:8000/`

**Sample response**:

```json
    {}
```

-----

### Prices of a pair per exchange: [GET] /price/{token1_symbol}/{token2_symbol}

By passing two symbols such as:

* ETH
* USDT
* USDC
* DAI

The user may obtain the exchange rate of a given pair.

> The exchange rait meaning at which price will I be able to buy token2 having token1.

*Can be accessed through*: `localhost:8000/price/USDT/USDC`

**Sample Response**:

```json
{
    "uniswap": "{token1} vs {token2} = X",
    "sushiswap": "{token1} vs {token2} = X",
    "pancakeswap": "{token1} vs {token2} = X",
}
```

## Next Steps:

- [ ] Allow users to input their wallet addresses.
- [ ] Add tests.
- [ ] Include Smart Contract integration.
- [ ] Endpoint for executing transactions at the possible platforms.
- [ ] Metamask integration. 