"""
A class to store data about specific sensors, and potentially create virtual sensors
"""
import math
import random
import re
import datetime


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from data_management.SensorDataManager import SensorDataManager
from data_management.DatabaseManager import DatabaseManager
from peripherals.Peripheral import Peripheral


class Sensor(Peripheral):
    def __init__(self, dbmanager=None, identifier=None, virtual=False, **attributes):
        
        self.virtual = virtual
        self.identifier = identifier
        
        
        # If the sensor is real
        if identifier:
            if not re.match(r'^sensor\.', identifier):
                raise ValueError("Identifier does not indicate a sensor")
        
            self.df = dbmanager.get_timeseries(identifier)# time is index on the real sensors already
            self.timeseries = self.df.reset_index()[['time','state']]
            self.timeseries['state']=pd.to_numeric(self.timeseries["state"], errors='coerce').values
            self.timeseries = self.timeseries.dropna()
            self.initialise_attributes_from_df()
            self.x = np.array(self.timeseries.index)#should be date
            self.y = np.array(self.timeseries["state"])#should be value
        
        elif virtual:
            self.generate_virtual_data(randomise=True)

    ### Virtual Sensor Methods
    #TODO: Create Virtual Sensors

    def initialise_virtual_df(self):
        # Convert self.x to datetime
        self.x = pd.to_datetime(self.x)
        
        # Create a DataFrame with 'time' as the index
        self.df = pd.DataFrame({
            'state': self.y,
            'time': self.x
        })

        # Perform same operations as with the real sensor
        self.timeseries = self.df.reset_index()[['time', 'state']]
        self.timeseries['state'] = pd.to_numeric(self.timeseries['state'], errors='coerce')
        # Update self.x and self.y
        self.x = np.array(self.timeseries.index)
        self.y = np.array(self.timeseries['state'])



    def generate_virtual_data(self, sample_rate=None, amplitude=None, frequency=None, phase=None, noise_level=None, randomise:bool=False):
        # add capability for white noise
        random.seed(0)

        if randomise:
            sample_rate = sample_rate if sample_rate is not None else 60 + np.random.randint(-59, 6000)  # seconds with randomness
            amplitude = amplitude if amplitude is not None else 1.0 + np.random.uniform(-0.1, 0.1)
            frequency = frequency if frequency is not None else (1 / 86400) * (1 + np.random.uniform(-0.1, 0.1))  # daily frequency with 10% variation
            phase = phase if phase is not None else np.random.uniform(-np.pi/4, np.pi/4)
            noise_level = noise_level if noise_level is not None else 0.1 + np.random.uniform(-0.05, 0.05)

        else:
            #params
            sample_rate = sample_rate if sample_rate is not None else 60
            amplitude = amplitude if amplitude is not None else 1
            frequency = frequency if frequency is not None else 1 / 86400
            phase = phase if phase is not None else 0
            noise_level = noise_level if noise_level is not None else 0.1

        # Calculate the number of samples
        duration = 14  # 2 weeks
        num_samples = int(duration * 24 * 60 * 60 / sample_rate)
        
        # Generate timestamps starting from two weeks from now
        start_time = datetime.datetime.now() + datetime.timedelta(weeks=2)
        timestamps = pd.date_range(start=start_time, periods=num_samples, freq=pd.DateOffset(seconds=sample_rate))
        
        # Generate the sinusoidal data
        t = np.arange(num_samples) * sample_rate
        sinusoidal_data = amplitude * np.sin(2 * np.pi * frequency * t + phase)
        
        # Add noise to the data
        noise = noise_level * np.random.randn(num_samples)
        data_with_noise = sinusoidal_data + noise
        
        # Create a DataFrame
        self.x = timestamps
        self.y = data_with_noise
        self.initialise_virtual_df()
        

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

    def get_timestep(self) -> float:
        # Ensure the index is a datetime index
        
        if self.virtual:
            self.df.set_index('time', inplace=True)
            
        
        time_diffs = self.df.index.to_series().diff() # get the difference between sample times
        rounded_interval = time_diffs.mode()[0]# find most common time interval
        common_interval_seconds = round(rounded_interval.total_seconds()) # find the most common and round
        return common_interval_seconds

    def update_attributes(self, attributes):
            for key, value in attributes.items():
                setattr(self, key, value)

    def get_attributes(self):
        # return the attributes gathered from the database
        return NotImplementedError
    
    def get_timeseries(self, numpy=False):
        """
        The function `get_timeseries` returns the timeseries data either as a list or as numpy arrays based
        on the `numpy` parameter.
        
        :param numpy: It looks like the `numpy` parameter is used to determine whether the function should
        return the timeseries data as a numpy array or not. If `numpy` is set to `False`, the function will
        return the timeseries data as it is. If `numpy` is set to `True`,, defaults to False (optional)
        :return: The code is returning the timeseries data if the `numpy` parameter is set to `False`. If
        `numpy` is set to `True`, the code seems to be incomplete as it does not specify what should be
        returned when `numpy` is `True`. It appears that there is a missing return statement or logic to
        handle the case when `numpy` is `True`.
        """
        
        if not numpy:
            return self.timeseries #returns the dataframe
        
        else:
            return self.y# returns a 1d numpy array of the sensor values

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
