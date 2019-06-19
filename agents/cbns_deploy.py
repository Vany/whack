from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address
import time

contract_owner = Entity.from_hex('c25ace8a7a485b396f30e4a0332d0d18fd2e462b3f1404f85a1b7bcac4b4b19d')
contract_owner_address = Address(contract_owner) # atsREugsanXS828FnTvmLM9vCkBsWnDgushDH9YjEgsdBuRGv
with open("./cbns_token.etch", "r") as fb:
    contract_source = fb.read()
api = LedgerApi('127.0.0.1', 8000)
api.sync(api.tokens.wealth(contract_owner, 5000000))
contract = SmartContract(contract_source)
api.sync(api.contracts.create(contract_owner, contract, 2456766))


time.sleep(10)
print('Deployed contract address:', Address(contract.digest))

print('my balance:', contract.query(api, 'balanceOf', owner=contract_owner_address))
