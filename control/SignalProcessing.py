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
    def detrend(y, plot:bool = False)-> pd.DataFrame:
        if plot:
            pass
        else:
            return signal.detrend(y)
    
    @staticmethod
    def fourier_transform(y, timestep: int = 1, plot: bool = False) -> pd.DataFrame:
        # Detrend the data
        y_detrend = SignalProcessing.detrend(y)

        # Perform FFT
        FFT = np.fft.fft(y_detrend)

        # Get frequency components
        n = len(y_detrend)
        freq = np.fft.fftfreq(n, d=timestep)

        # Normalize the FFT output
        FFT_abs = np.abs(FFT) / n

        # Only keep the positive frequencies
        mask = freq > 0
        freq = freq[mask]
        FFT_abs = FFT_abs[mask]

        if plot:
            plt.figure(figsize=(10, 6))
            plt.plot(freq, FFT_abs, color='black')
            plt.xlabel('Frequency (Hz)', fontsize=20)
            plt.ylabel('Amplitude', fontsize=20)
            plt.title('(Fast) Fourier Transform Method Algorithm', fontsize=20)
            plt.grid(True)
            plt.show()

        # Return the DataFrame with frequency and amplitude for further analysis if needed
        return pd.DataFrame({'Frequency': freq, 'Amplitude': FFT_abs})


    
    @staticmethod
    def filter_data(self, frequency_low:float, frequency_high:float, plot:bool=False) -> pd.DataFrame:
        pass

    @staticmethod
    def __plot(self):
        #plot a given output
        pass