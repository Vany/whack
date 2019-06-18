from flask import Flask
from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address
import sys
import time
import json

app            = Flask(__name__)
wallet_owner   = Entity()
wallet_address = Address(wallet_owner)
api = LedgerApi('127.0.0.1', 8100)
contracts = {}

# Need funds to deploy contract
# print(dir(api.tokens))

@app.route('/balance')
def balance():
    balance =  api.tokens.balance(wallet_address)
    return json.dumps({"address": str(wallet_address), "balance":balance})


@app.route('/address')
def address():
    return json.dumps({"address", str(wallet_address)})


@app.route('/create-tokens')
def create_tokens():
    """Creates 10k tokens """
    api.sync(api.tokens.wealth(wallet_owner, 100000))
    return json.dumps({"status":"done"})
