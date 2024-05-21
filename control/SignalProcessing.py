import pandas as pd

import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
from scipy import signal
from scipy.signal import butter, lfilter, filtfilt

import pywt

class SignalProcessing:

    @staticmethod
    def __butter_lowpass(cutoff, fs, order):
        return butter(order,cutoff, fs=fs, btype='low', analog=False)

    @staticmethod
    def signaltonoise(a, axis=0, ddof=0, detrend=False):
        if detrend:
            a = SignalProcessing.detrend(a)
        a = np.asanyarray(a)
        m = a.mean(axis)
        sd = a.std(axis=axis, ddof=ddof)
        return np.where(sd == 0, 0, m/sd)

    #TODO: band pass

    #TODO: high pass

    @staticmethod
    def butter_lowpass_filter(data:np.array,  cutoff, timestep:int=1, order:int=5, plot:bool=False):
        data = SignalProcessing.detrend(data)
        fs = 1/timestep #sample frequency
        b, a = SignalProcessing.__butter_lowpass(cutoff, fs, order=order)
        y = filtfilt(b, a, data) # to avoid lag you must flip the output and pass it through the filter again.
        n = len(data)
        T = int(n/fs)
        t = np.linspace(0, T, n, endpoint=False)
        if plot:
            plt.plot(t, data, 'b-', label='data')
            plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
        else:
            return y
    
    @staticmethod
    def psd(data:np.array):
        #TODO: implement power spectral density
        pass

    @staticmethod
    def auto_correlation(data:np.array):
        #TODO: implement auto correlation function
        pass

    @staticmethod
    def cross_correlation(data:np.array):
        #TODO: implement cross correlation function
        pass


    @staticmethod
    def moving_average(self, df) -> pd.DataFrame:
        pass

    @staticmethod
    def detrend(y, plot:bool = False):
        if plot:
            #TODO: implement plotting the detrend vs the standard signal
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

        
        else:
            # Return the DataFrame with frequency and amplitude for further analysis if needed
            return pd.DataFrame({'Frequency': freq, 'Amplitude': FFT_abs})
            
    

    @staticmethod
    def filter_data(frequency_low:float, frequency_high:float, plot:bool=False) -> pd.DataFrame:
        pass

    @staticmethod
    def __plot():
        #plot a given output
        pass