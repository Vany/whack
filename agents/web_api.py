import asyncio

from flask import Flask
from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address
import sys
import time
import json

from oef.query import *

from agents.rider_agent import RiderAgent
from agents.scooter_schema import *

app            = Flask(__name__)
wallet_owner   = Entity()
wallet_address = Address(wallet_owner)
api = LedgerApi('127.0.0.1', 8100)
contracts = {}

loop = asyncio.get_event_loop()


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

@app.route('/chargers')
def chargers():
    agent = RiderAgent("RiderAgent", oef_addr="127.0.0.1", oef_port=10000, loop=loop)

    agent.connect()
    time.sleep(2)

    query = Query([Constraint(CHARGER_AVAILABLE.name, Eq(True))])
    agent.search_services(0, query)

    time.sleep(1)
    try:
        agent.async_run()
        time.sleep(3)
        return json.dumps({"chargers": 1})
    except Exception as ex:
        return json.dumps({"exception": ex})
    finally:
        try:
            agent.stop()
            agent.disconnect()
        except:
            pass



if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
    loop.run_forever()