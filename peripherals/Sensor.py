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
from peripherals.Peripheral import Peripheral


class Sensor(Peripheral):
    def __init__(self, dbmanager, identifier=None, virtual=False, **attributes):
        
        self.virtual = virtual
        self.identifier = identifier
        if not re.match(r'^sensor\.', identifier):
            raise ValueError("Identifier does not indicate a sensor")
        
        # If the sensor is real
        if identifier:
            self.df = dbmanager.get_timeseries(identifier)
            self.timeseries = self.df.reset_index()[['time','state']]
            self.initialise_attributes_from_df()
        
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
    def initialise_attributes_from_df(self):
            # Extract attributes from the first non-null row in the DataFrame
            first_valid_index = self.df['attributes'].first_valid_index()
            if first_valid_index is not None:
                attributes = self.df.loc[first_valid_index, 'attributes']
                self.update_attributes(attributes)


    ### Agnostic Methods
    
    def get_latest_state(self):
        """
        The function `get_latest_state` returns the latest entry in the timeseries data if it is not empty.
        :return: The `get_latest_state` method returns the latest state from the `timeseries` data if it is
        not empty. If the `timeseries` is empty, it returns `None`.
        """
        if not self.timeseries.empty:
            return self.timeseries.iloc[-1]
        return None        


    def update_attributes(self, attributes):
            for key, value in attributes.items():
                setattr(self, key, value)
    
    def get_timeseries(self):
        """
        The function `get_timeseries` returns a timeseries with any missing values removed.
        :return: The `timeseries` variable, which is the `self.timeseries` DataFrame with any missing values
        (NaNs) removed, is being returned.
        """
        timeseries = self.timeseries.dropna()
        return timeseries

    def get_state_at_time(self, time):
        pass

    def plot(self):
        pass

    #TODO: does this need to be an async function because it will need to be able to handle the websocket data?
    def update_series(self, time, state, location=None):
        new_entry = pd.DataFrame({'time': [time], 'state': [state], 'location': [location]})
        self.timeseries = pd.concat([self.timeseries, new_entry], ignore_index=True)

    def __str__(self):
        latest_state = self.get_latest_state()
        last_state_info = f"{latest_state['state']} at {latest_state.name}" if latest_state is not None else "No data"
        return f"Sensor({self.friendly_name}, class: {self.device_class}, measured in: {self.unit_of_measurement} Last recorded state: {last_state_info})"
