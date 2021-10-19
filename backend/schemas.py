from os import environ

from pydantic import BaseModel
from typing import Optional


class Transaction(BaseModel):
    '''
        Transaction data necessary to operate.
    '''
    token_1: str
    token_2: str
    swap: str
    amount: float
    wallet: Optional[str] = environ.get('WALLET')
    private_key: Optional[str] = environ.get('PRIVATE_KEY')
    dry_run: Optional[bool] = True