#!/usr/bin/python3

from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address

owner = Entity()

api = LedgerApi('127.0.0.1', 8000)

api.sync(api.tokens.wealth(owner, 59000000))

contract = SmartContract(open("erc20.etch", "r").read())

api.sync(api.contracts.create(owner, contract, 2456766))

print(contract.action(api, 'TEST', 100, [owner]))
f = open("chargetoken.py", "w+")
f.write(""" 
from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address

api = LedgerApi('127.0.0.1', 8000)

""")

f.write("Owner = Entity.loads(\"" + owner.dumps().replace('"', '\\"') + "\")\n")
f.write("Contract = SmartContract.loads(\"" + contract.dumps().replace('"', '\\"') + "\")\n")


f.write("""
def GrantBalance(addr, v):
    api.sync(Contract.action(api, 'transfer', 100, [Owner], Address(Owner), Address(addr), v))
   # api.contracts.query(Contract, Owner, 'transfer', **{'from':Owner, 'to':addr, 'value':v})
""")