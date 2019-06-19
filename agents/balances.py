from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address


contract_owner = Entity.from_hex('c25ace8a7a485b396f30e4a0332d0d18fd2e462b3f1404f85a1b7bcac4b4b19d')
contract_owner_address = Address(contract_owner) # atsREugsanXS828FnTvmLM9vCkBsWnDgushDH9YjEgsdBuRGv
print('owner address',contract_owner_address)

api = LedgerApi('127.0.0.1', 8000)

riders = ['WfQDBasLx396CCxWvUoa4BmEsStPNRUi9iA45zu6k3eeaUMGs',
        'pUkSDemAkhTob8UiqmRoRbjBW2rwTdnDR68thfToZwYrYHdGr',
        '2GNnBTmnkUwDeJfuig3hxN77gteXixw45mhita58MzZyMoqQ9u',
        'fzoGmzeHN3EkvtbgTNYxuP1Zokpn7AZy5eiSSdP9Rw7KwitPW',
        '2R6SJK7hoiVTQbMVQDMpB86NaHX9CAXBb5hmH5kyTHCndsNSfe']
for rider in riders:
    print(api.contracts.query(Address('Ch9EPpgfwJWUiHeSWWcxSr29pfWLgZ9RPRU2BT5CKVNEabLJc'), contract_owner_address,
        'balanceOf', owner=Address(rider)))

