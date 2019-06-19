#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#
#   Copyright 2018 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------
import json
import sys
from scooter_schema import *
from oef.agents import OEFAgent

from oef.proxy import PROPOSE_TYPES
from oef.query import *
from oef.query import Query
from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address
import binascii
import time

#contract_addr = Address('Ch9EPpgfwJWUiHeSWWcxSr29pfWLgZ9RPRU2BT5CKVNEabLJc')
contract_addr = Address('Won2CpQEJHaLRmL1x5sNFvDNFwbM6YLh3qq6H3ME6ngzVCa5V')
contract_owner = Address('atsREugsanXS828FnTvmLM9vCkBsWnDgushDH9YjEgsdBuRGv')

class RiderAgent(OEFAgent):

    def __init__(self, *args, **kwargs):
        super(RiderAgent, self).__init__(*args, **kwargs)

        riders = [ '904f302f980617d5f40219337ef826cdf64992e577676cdd83295f189af82ff4',
                '03f807bbf02cf849145fc51d7dd4438559dc4756a3b2321bbdf42e8f7910a3df',
                'dfe06a3baa93ad1d2f248317c601f710821cc1916e09d7c6e261f432563e50f1',
                'a92e7c9a1c091bb7bc70874da36fdc44a8217577758a061e008344bd402a6118',
                '672ebe1ef50a3c49532fe2118686d7025048de51e4f77ed8d0880cd52efe80a7']
        self._entity = Entity.from_hex(riders[int(sys.argv[1])-1])
        self._address = Address(self._entity)
        self._api = LedgerApi('127.0.0.1', 8000)
        self._api.sync(self._api.tokens.wealth(self._entity, 5000000))

    def on_search_result(self, search_id: int, agents: List[str]):
        """For every agent returned in the service search, send a CFP to obtain resources from them."""
        if len(agents) == 0:
            print("[{}]: No agent found. Stopping...".format(self.public_key))
            self.stop()
            return

        print("[{0}]: Agent found: {1}".format(self.public_key, agents))
        for agent in agents:
            print("[{0}]: Sending to agent {1}".format(self.public_key, agent))
            # we send a 'None' query, meaning "give me all the resources you can propose."
            query = None
            # CFP is Call For Proposal
            self.send_cfp(1, 0, agent, 0, query)

    def on_propose(self, msg_id: int, dialogue_id: int, origin: str, target: int, proposals: PROPOSE_TYPES):
        """When we receive a Propose message, answer with an Accept."""
        print("[{0}]: Received propose from agent {1}".format(self.public_key, origin))
        for i, p in enumerate(proposals):
            print("[{0}]: Proposal {1}: {2}".format(self.public_key, i, p.values))
        print("[{0}]: Accepting Propose.".format(self.public_key))
        self.send_accept(msg_id, dialogue_id, origin, msg_id + 1)

    def on_message(self, msg_id: int, dialogue_id: int, origin: str, content: bytes):
        """Extract and print data from incoming (simple) messages."""

        # PLACE HOLDER TO SIGN AND SUBMIT TRANSACTION
        transaction = json.loads(content.decode("utf-8"))
        charge_station_address = Address(binascii.unhexlify(transaction['address']))

        print("[{0}]: Received contract from {1}".format(self.public_key, origin))
        print("READY TO SUBMIT to address: ", charge_station_address, " value: ", transaction['value'])

        #self._api.sync(self._contract.action(self._api, 'transfer', 40, [self._entity], self._address, charge_station_address, transaction['value']))
        self._api.sync(self._api.contracts.action(contract_addr, contract_owner, 'transfer', 40, [self._entity], self._address, charge_station_address, transaction['value']))

        #time.sleep(10)

        #print(self._contract.query(self._api, 'balanceOf', owner=charge_station_address))
        #print(self._api.contracts.query(contract_addr, contract_owner, 'balanceOf', owner=charge_station_address))
        #print(self._api.contracts.query(contract_addr, contract_owner, 'balanceOf', owner=self._address))

        self._api.sync(self._api.contracts.action(Address('QguxAD9FTj2MTnvNbdr15MGPMftXW8qdcewa4X96JEx2SU6hg'), contract_owner, 'transfer', 40, [Entity.from_hex('c25ace8a7a485b396f30e4a0332d0d18fd2e462b3f1404f85a1b7bcac4b4b19d')], contract_owner, self._address, transaction['value'] + transaction['bonus']))

        self.stop()


if __name__ == "__main__":
    # create and connect the agent
    agent = RiderAgent("RiderAgent", oef_addr="127.0.0.1", oef_port=10000)
    agent.connect()

    time.sleep(2)

    # query = Query([Constraint(PRICE_PER_KM.name, Eq(1))],
    #               JOURNEY_MODEL

    query = Query([Constraint(PRICE_KWH.name, Lt(56)),
                   Constraint(CHARGER_AVAILABLE.name, Eq(True)),
                   Constraint(CHARGER_BONUS.name, Gt(0))
                   ])

    # query = Query([Constraint(CHARGER_LOCATION.name, Distance(Location(52.2057092, 0.1183431), 100.0))])

    agent.search_services(0, query)

    time.sleep(1)
    try:
        agent.run()
        time.sleep(3)
    except Exception as ex:
        print("EXCEPTION:", ex)
    finally:
        try:
            agent.stop()
            agent.disconnect()
        except:
            pass
