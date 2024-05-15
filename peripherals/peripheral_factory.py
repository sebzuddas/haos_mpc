from Sensor import Sensor
from Actuator import Actuator
import re

def peripheral_factory(identifier):
    if re.match(r'^sensor\.', identifier):
        return Sensor(identifier)
    elif re.match(r'^switch\.', identifier):
        return Actuator(identifier)
    else:
        raise ValueError("Unknown device type")