#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from agents.scooter_schema import CHARGING_MODEL
from oef.agents import OEFAgent
from oef.messages import CFP_TYPES
from oef.schema import Description, Location
from fetchai.ledger.api import LedgerApi
from fetchai.ledger.contract import SmartContract
from fetchai.ledger.crypto import Entity, Address


class ChargerAgent(OEFAgent):
    """Class that implements the behaviour of the charger agent."""

    price_kwh = 55
    location = Location(52.2057092, 0.1183431)
    charger_description = Description(
        {
            "price_kilowatt_hour": price_kwh,
            "charger_location": location,
            "charger_available": True,
        },
        CHARGING_MODEL
    )

    def __init__(self, *args, **kwargs):
        super(ChargerAgent, self).__init__(*args, **kwargs)

        self._entity = Entity()
        self._address = Address(self._entity)

    #      with open("./full_contract.etch", "r") as fb:
    #          self._source = fb.read()

    #      self.prepare_contract()

    def prepare_contract(self):
        # Setting API up
        self._api = LedgerApi('127.0.0.1', 8100)

        # Need funds to deploy contract
        self._api.sync(self._api.tokens.wealth(self._entity, 5000000))

        # Create contract
        self._contract = SmartContract(self._source)

        # Deploy contract
        self._api.sync(self._api.contracts.create(self._entity, self._contract, 2456766))

    def on_cfp(self, msg_id: int, dialogue_id: int, origin: str, target: int, query: CFP_TYPES):
        """Send a simple Propose to the sender of the CFP."""
        print("[{0}]: Received CFP from {1}".format(self.public_key, origin))

        # prepare the proposal with a given price.
        proposal = Description({"price_kilowatt_hour": self.price_kwh, "charger_location": self.location})
        print("[{}]: Sending propose at price: {} location {},{}".format(self.public_key, self.price_kwh, self.location.latitude, self.location.longitude))
        self.send_propose(msg_id + 1, dialogue_id, origin, target + 1, [proposal])

    def on_accept(self, msg_id: int, dialogue_id: int, origin: str, target: int):
        """Once we received an Accept, send the requested data."""
        print("[{0}]: Received accept from {1}."
              .format(self.public_key, origin))

        # Preparing contract
        # PLACE HOLDER TO PREPARE AND SIGN TRANSACTION
        contract = {"contract": "data"}

        # Sending contract
        encoded_data = json.dumps(contract).encode("utf-8")
        print("[{0}]: Sending contract to {1}".format(self.public_key, origin))
        self.send_message(0, dialogue_id, origin, encoded_data)


if __name__ == "__main__":
    agent = ChargerAgent("charger", oef_addr="127.0.0.1", oef_port=10000)
    agent.connect()
    agent.register_service(77, agent.charger_description)

    print("[{}]: Waiting for clients...".format(agent.public_key))
    try:
        agent.run()
    finally:
        try:
            agent.stop()
            agent.disconnect()
        except:
            pass
