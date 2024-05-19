import pandas as pd

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
from scipy import signal
import pywt

class SignalProcessing:
    def __init__(self) -> None:
        pass

    def moving_average(self, df) -> pd.DataFrame:
        pass

    def detrend(self, df)-> pd.DataFrame:
        return signal.detrend()

    def fourier_transform(self) -> pd.DataFrame:
        pass

    def filter_data(self, frequency_low:float, frequency_high:float) -> pd.DataFrame:
        pass