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
    def detrend(y)-> pd.DataFrame:
        return signal.detrend(y)
    
    @staticmethod
    def fourier_transform(y, plot:bool=False) -> pd.DataFrame:
        y_detrend = SignalProcessing.detrend(y)
        FFT =np.fft.fft(y_detrend)
        new_N=int(len(FFT)/2) 
        f_nat=1
        new_X = np.linspace(10**-12, f_nat/2, new_N, endpoint=True)
        new_Xph=1.0/(new_X)
        FFT_abs=np.abs(FFT)
        plt.plot(new_Xph,2*FFT_abs[0:int(len(FFT)/2.)]/len(new_Xph),color='black')
        plt.xlabel('Period ($h$)',fontsize=20)
        plt.ylabel('Amplitude',fontsize=20)
        plt.title('(Fast) Fourier Transform Method Algorithm',fontsize=20)
        plt.grid(True)
        if plot:
            plt.show()
        pass
    
    @staticmethod
    def filter_data(self, frequency_low:float, frequency_high:float, plot:bool=False) -> pd.DataFrame:
        pass

    @staticmethod
    def __plot(self):
        #plot a given output
        pass