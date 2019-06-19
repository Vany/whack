from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address
import time

contract_owner = Entity.from_hex('c25ace8a7a485b396f30e4a0332d0d18fd2e462b3f1404f85a1b7bcac4b4b19d')
contract_owner_address = Address(contract_owner) # atsREugsanXS828FnTvmLM9vCkBsWnDgushDH9YjEgsdBuRGv
with open("./chrg_token.etch", "r") as fb:
    contract_source = fb.read()
api = LedgerApi('127.0.0.1', 8000)
api.sync(api.tokens.wealth(contract_owner, 5000000))
contract = SmartContract(contract_source)
api.sync(api.contracts.create(contract_owner, contract, 2456766))


time.sleep(10)
print('Deployed contract address:', Address(contract.digest))

riders = ['WfQDBasLx396CCxWvUoa4BmEsStPNRUi9iA45zu6k3eeaUMGs',
        'pUkSDemAkhTob8UiqmRoRbjBW2rwTdnDR68thfToZwYrYHdGr',
        '2GNnBTmnkUwDeJfuig3hxN77gteXixw45mhita58MzZyMoqQ9u',
        'fzoGmzeHN3EkvtbgTNYxuP1Zokpn7AZy5eiSSdP9Rw7KwitPW',
        '2R6SJK7hoiVTQbMVQDMpB86NaHX9CAXBb5hmH5kyTHCndsNSfe']
for rider in riders:
    api.sync(contract.action(api, 'transfer', 100, [contract_owner], contract_owner_address, Address(rider), 100000))


print('my balance:', contract.query(api, 'balanceOf', owner=contract_owner_address))
