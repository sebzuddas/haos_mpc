from Sensor import Sensor
from Actuator import Actuator
import re

def peripheral_factory(dbmanager, identifier):
    if re.match(r'^sensor\.', identifier):
        return Sensor(dbmanager=dbmanager, identifier=identifier)
    elif re.match(r'^switch\.', identifier):
        return Actuator(dbmanager=dbmanager, identifier=identifier)
    else:
        raise ValueError("Unknown device type")