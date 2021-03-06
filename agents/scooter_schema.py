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


from oef.schema import DataModel, AttributeSchema, Location


PRICE_PER_KM = AttributeSchema("price_per_km", int, True, "Provides the price per kilometer.")

PRICE_KWH = AttributeSchema("price_kilowatt_hour", int, True, "Provides the price kilowatt hour.")

CHARGER_BONUS = AttributeSchema("charger_bonus", int, False, "Provides bonus cash back for charging here.")
CHARGER_LOCATION = AttributeSchema("charger_location", Location, True, "The location of the charger ")
CHARGER_AVAILABLE = AttributeSchema("charger_available", bool, True, "Provides the availability of the charger ")
CHARGER_OWNER = AttributeSchema("charger_owner", str, False, "Provides  charger's owner, "
                                                            "it could be person id or name name")


JOURNEY_MODEL = DataModel("journey", [PRICE_PER_KM], "All possible scooter data.")

CHARGING_MODEL = DataModel("charging",
                               [PRICE_KWH, CHARGER_LOCATION, CHARGER_AVAILABLE, CHARGER_OWNER, CHARGER_BONUS],
                               "All possible chargers data.")
