"""
A class to store data about specific sensors, and potentially create virtual sensors
"""
import math
import random
import re

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from data_management.SensorDataManager import SensorDataManager
from data_management.DatabaseManager import DatabaseManager



class Sensor:
    def __init__(self, dbmanager, identifier=None, virtual=False, **attributes):
        
        self.virtual = virtual
        self.identifier = identifier
        if not re.match(r'^sensor\.', identifier):
            raise ValueError("Identifier does not indicate a sensor")
        
        # If the sensor is real
        if identifier != None:
            self.df = dbmanager.get_sensor_timeseries(identifier)
        
        # if the sensor is virtual

    ### Virtual Sensor Methods
    #TODO: Create Virtual Sensors

    def initialize_empty_df(self):
        """
        now = datetime.now()
        dates = pd.date_range(end=now, periods=14, freq='D')
        self.timeseries = pd.DataFrame({
            'state': [None] * 14,
            'attributes': [{}] * 14,
            'location': [None] * 14
        }, index=dates)
        """        
        
        return NotImplemented

    def generate_virtual_data(self):
        """
        if self.virtual:
            #generate virtual data
            print('generating virtual data')
        else:
            print('generate forecasted data')
        """
        return NotImplemented

    ### Real Sensor




    ### Agnostic Methods
    
    def get_latest_state(self):
        if not self.timeseries.empty:
            return self.timeseries.iloc[-1]
        return None        


    
    def get_sensor_timeseries(self):

        pass

    def get_sensor_state(self):
        
        
        pass

    def plot(self):
        pass

    #TODO: does this need to be an async function because it will need to be able to handle the websocket data
    def update_series(self, time, state, location=None):
        new_entry = pd.DataFrame({'time': [time], 'state': [state], 'location': [location]})
        self.timeseries = pd.concat([self.timeseries, new_entry], ignore_index=True)

    def __str__(self):
        latest_state = self.get_latest_state()
        last_state_info = f"{latest_state['state']} at {latest_state.name}" if latest_state is not None else "No data"
        return f"Sensor({self.friendly_name}, {self.device_class}, Last recorded state: {last_state_info})"
