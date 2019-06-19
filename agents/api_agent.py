import time

from oef.agents import OEFAgent
from oef.messages import PROPOSE_TYPES
from oef.query import *
from oef.schema import Description

from agents.scooter_schema import *


class ApiAgent(OEFAgent):
    chargerList: List[Description]

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
        for i, p in enumerate(proposals):
            print("[{0}]: Proposal {1}: {2}".format(self.public_key, i, p.values))
            self.chargerList.append(p)

        # TODO: save proposals to global var
        print("[{0}]: Decline Propose.".format(self.public_key))
        self.send_decline(msg_id, dialogue_id, origin, msg_id + 1)


if __name__ == "__main__":
    # create and connect the agent
    agent = ApiAgent("ApiAgent", oef_addr="127.0.0.1", oef_port=10000)
    agent.connect()

    time.sleep(2)

    # query = Query([Constraint(PRICE_PER_KM.name, Eq(1))],
    #               JOURNEY_MODEL

    query = Query([Constraint(PRICE_KWH.name, Lt(56)), Constraint(CHARGER_AVAILABLE.name, Eq(True))])

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
