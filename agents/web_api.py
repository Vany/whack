import asyncio
from typing import Dict

from flask import Flask
from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address
import sys
import time
import json

from oef.agents import OEFAgent
from oef.proxy import PROPOSE_TYPES
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

class ApiAgent(OEFAgent):
    chargerList = Dict[str, ATTRIBUTE_TYPES]

    @property
    def chargers(self) -> List[Description]:
        return self.chargerList

    def on_search_result(self, search_id: int, agents: List[str]):
        """For every agent returned in the service search, send a CFP to obtain resources from them."""
        if len(agents) == 0:
            print("[{}]: No agent found. Stopping...".format(self.public_key))
            self.stop()
            return

        print("[{0}]: Agent found: {1}".format(self.public_key, agents))
        for agent in agents:
            print("[{0}]: Sending to agent {1}".format(self.public_key, agent))
            # CFP is Call For Proposal
            self.send_cfp(1, 0, agent, 0, None)

    def on_propose(self, msg_id: int, dialogue_id: int, origin: str, target: int, proposals: PROPOSE_TYPES):
        """When we receive a Propose message, answer with an Accept."""
        print("[{0}]: Received propose from agent {1}".format(self.public_key, origin))
        self.chargerList = proposals
        # for i, p in enumerate(proposals):
        #     print("[{0}]: Proposal {1}: {2}".format(self.public_key, i, p.values))

        # TODO: save proposals to global var
        print("[{0}]: Decline Propose.".format(self.public_key))
        self.send_decline(msg_id, dialogue_id, origin, msg_id + 1)

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
    agent = ApiAgent("ApiAgent", oef_addr="127.0.0.1", oef_port=10000, loop=loop)

    agent.connect()
    time.sleep(1)

    query = Query([Constraint(CHARGER_AVAILABLE.name, Eq(True))])
    agent.search_services(0, query)

    time.sleep(1)
    try:
        agent.run()
        time.sleep(2)
        # for i, p in enumerate(agent.chargerList):
        #     print("Charger {}: {}".format(i, p.values))

        agent.stop()
        agent.disconnect()
        return json.dumps({"chargers": "len(agent.chargers)"})
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