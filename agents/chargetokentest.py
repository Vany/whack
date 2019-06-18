import chargetoken

 
from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address

taker = Entity()
api = chargetoken.api
chargetoken.GrantBalance(taker, 77)
print(chargetoken.Contract.action(api, 'TEST', 100, [taker]))
print(chargetoken.Contract.query(api, 'total', owner=Address(taker)))
#print(api.contracts.query(chargetoken.Contract.digest, taker, 'total', owner=Address(taker)))
