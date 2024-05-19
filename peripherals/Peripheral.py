from abc import ABC, abstractmethod

class Peripheral(ABC):

    @abstractmethod
    def initialise_attributes_from_df(self):
        pass

    @abstractmethod
    def update_attributes(self, attributes):
        pass

    @abstractmethod
    def get_latest_state(self):
        pass

    @abstractmethod
    def get_timeseries(self):
        pass

    @abstractmethod
    def get_state_at_time(self, time):
        pass

    @abstractmethod
    def plot(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
