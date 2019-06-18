#!/usr/bin/python3

from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address

owner = Entity()

api = LedgerApi('127.0.0.1', 8000)

api.sync(api.tokens.wealth(owner, 59000000))

contract = SmartContract("erc20.etch")

api.sync(api.contracts.create(owner, contract, 2456766))

f = open("chargetoken.py", "w+")
f.write(""" 
from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address
""")

f.write("TokenOwner = Entity.from_hex(\"" + owner.private_key_hex + "\")")
