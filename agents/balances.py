from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address


contract_owner = Entity.from_hex('c25ace8a7a485b396f30e4a0332d0d18fd2e462b3f1404f85a1b7bcac4b4b19d')
contract_owner_address = Address(contract_owner) # atsREugsanXS828FnTvmLM9vCkBsWnDgushDH9YjEgsdBuRGv
#contract_address = Address('Ch9EPpgfwJWUiHeSWWcxSr29pfWLgZ9RPRU2BT5CKVNEabLJc')
chrg_contract_address = Address('Won2CpQEJHaLRmL1x5sNFvDNFwbM6YLh3qq6H3ME6ngzVCa5V')
cbns_contract_address = Address('QguxAD9FTj2MTnvNbdr15MGPMftXW8qdcewa4X96JEx2SU6hg')

api = LedgerApi('127.0.0.1', 8000)
#print('owner', contract_owner_address, api.contracts.query(chrg_contract_address,
#    contract_owner_address, 'balanceOf', owner=contract_owner_address),
#    api.contracts.query(cbns_contract_address, contract_owner_address, 'balanceOf', owner=contract_owner_address))

riders = ['WfQDBasLx396CCxWvUoa4BmEsStPNRUi9iA45zu6k3eeaUMGs',
        'pUkSDemAkhTob8UiqmRoRbjBW2rwTdnDR68thfToZwYrYHdGr',
        '2GNnBTmnkUwDeJfuig3hxN77gteXixw45mhita58MzZyMoqQ9u',
        'fzoGmzeHN3EkvtbgTNYxuP1Zokpn7AZy5eiSSdP9Rw7KwitPW',
        '2R6SJK7hoiVTQbMVQDMpB86NaHX9CAXBb5hmH5kyTHCndsNSfe']
cnt = 1
for rider in riders:
    print('rider', cnt, "\t balance: ", api.contracts.query(chrg_contract_address, contract_owner_address,
        'balanceOf', owner=Address(rider))[1]['result'], "\t bonus balance: ", api.contracts.query(cbns_contract_address,
            contract_owner_address, 'balanceOf', owner=Address(rider))[1]['result'])
    cnt = cnt + 1

chargers = ['Do2W1zBm4VSsVhqtP48TDRZf35Sfjy8guMpqFwJYpDW4Y6U1E',
    'RWuCaax6jpRCBrDvfk6awXtt5UBTUsaQCZb7wCm9av3NBaPn4',
    '2aZcFnGahqPMrpr6DmEq7LmDcQS9xHgTHdFGHs2MgRYZaqsvyX',
    '26GfX7AUUik6cxPrzskyHsNMpmRjAqmUQutydwsZTMhZcMUgzu',
    '2oZixVsU7fRpH83qoLxXstpfDFXjkjZWucsXXQVbmrQ8A7GxN'];
cnt = 1
for charger in chargers:
    print('charger', cnt, "\t balance: ", api.contracts.query(chrg_contract_address, contract_owner_address,
        'balanceOf', owner=Address(charger))[1]['result'])
    cnt = cnt + 1
