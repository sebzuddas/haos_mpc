
import re
from peripherals.Peripheral import Peripheral

class Actuator(Peripheral):
    def __init__(self, dbmanager, identifier=None, virtual=False, **attributes) -> None:
        self.virtual = virtual
        self.identifier = identifier
        if not re.match(r'^switch\.', identifier):
            raise ValueError("Identifier does not indicate an actuator or switch")
        
        # If the actuator is real
        if identifier:
            self.df = dbmanager.get_timeseries(identifier)
            self.timeseries = self.df.reset_index()[['time','state']]
            self.initialise_attributes_from_df()

    def initialise_attributes_from_df(self):
        # Extract attributes from the first non-null row in the DataFrame
        first_valid_index = self.df['attributes'].first_valid_index()
        if first_valid_index is not None:
            attributes = self.df.loc[first_valid_index, 'attributes']
            self.update_attributes(attributes)
    def update_attributes(self, attributes):
        for key, value in attributes.items():
            setattr(self, key, value)

    def get_latest_state(self):
        """
        The function `get_latest_state` returns the latest entry in the timeseries data if it is not empty.
        :return: The `get_latest_state` method returns the latest state from the `timeseries` data if it is
        not empty. If the `timeseries` is empty, it returns `None`.
        """
        if not self.timeseries.empty:
            return self.timeseries.iloc[-1]
        return None

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

    def __str__(self):
        latest_state = self.get_latest_state()
        last_state_info = f"{latest_state['state']} at {latest_state.name}" if latest_state is not None else "No data"
        return f"Actuator({self.friendly_name}, class: {self.device_class}, measured in: {self.unit_of_measurement} Last recorded state: {last_state_info})"