import pandas as pd

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
from scipy import signal
import pywt

class SignalProcessing:

    @staticmethod
    def moving_average(self, df) -> pd.DataFrame:
        pass

    @staticmethod
    def detrend(self, df)-> pd.DataFrame:
        #TODO: finish the detrend method
        return signal.detrend()
    
    @staticmethod
    def fourier_transform(self, plot:bool=False) -> pd.DataFrame:
        pass
    
    @staticmethod
    def filter_data(self, frequency_low:float, frequency_high:float, plot:bool=False) -> pd.DataFrame:
        pass

    @staticmethod
    def __plot(self):
        #plot a given output
        pass