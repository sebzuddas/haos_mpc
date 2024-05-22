"""
The signal processing class contains a number of static methods primarily for signal analysis and filtering out noise. 
"""

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd 
from scipy import signal
from scipy.signal import butter, lfilter, filtfilt, periodogram
from scipy.interpolate import interp1d

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
        """
        The function `butter_lowpass_filter` applies a Butterworth lowpass filter to input data with
        specified cutoff frequency, timestep, order, and optional plotting capability.
        
        :param data: The `data` parameter is expected to be a NumPy array containing the input data that you
        want to filter using a Butterworth low-pass filter
        :type data: np.array
        :param cutoff: The `cutoff` parameter in the `butter_lowpass_filter` method refers to the cutoff
        frequency of the low-pass filter. This frequency determines the point at which the filter starts
        attenuating the higher frequencies in the signal. It is usually specified in hertz (Hz) and helps in
        removing
        :param timestep: The `timestep` parameter in the `butter_lowpass_filter` method represents the time
        interval between each data point in the input array. It is used to calculate the sample frequency
        (`fs`) for the low-pass filter, defaults to 1
        :type timestep: int (optional)
        :param order: The `order` parameter in the `butter_lowpass_filter` method refers to the order of the
        Butterworth filter to be used for low-pass filtering the input data. In signal processing, the order
        of a filter determines how quickly it rolls off the frequency response curve after the cutoff
        frequency, defaults to 5
        :type order: int (optional)
        :param plot: The `plot` parameter in the `butter_lowpass_filter` method is a boolean flag that
        determines whether to plot the original data and the filtered data. If `plot` is set to `True`, the
        method will generate a plot showing the original data in blue and the filtered data in green,
        defaults to False
        :type plot: bool (optional)
        :return: If the `plot` parameter is set to `True`, the function will plot the original data and the
        filtered data using matplotlib. If the `plot` parameter is set to `False`, the function will return
        the filtered data array `y`.
        """
        data = SignalProcessing.detrend(data)
        fs = 1/timestep #sample frequency
        b, a = SignalProcessing.__butter_lowpass(cutoff, fs, order=order)
        y = filtfilt(b, a, data) # to avoid lag you must flip the output and pass it through the filter again. filtfilt does this for you
        n = len(data)
        T = int(n/fs)
        t = np.linspace(0, T, n, endpoint=False)
        if plot:
            plt.plot(t, data, 'b-', label='data')
            plt.plot(t, y, 'g-', linewidth=2, label='filtered data')
        else:
            return y
    
    @staticmethod
    def psd(data:np.array, timestep:int=1, plot:bool=False):
        """
        The function `psd` calculates the power spectral density (PSD) of a given data array and optionally
        plots the PSD.
        
        :param data: The `data` parameter is expected to be a NumPy array containing the input signal for
        which you want to calculate the Power Spectral Density (PSD). This function calculates the PSD of
        the input signal using the periodogram method
        :type data: np.array
        :param timestep: The `timestep` parameter in the `psd` function represents the time interval between
        consecutive samples in the data array. It is used to calculate the sample frequency (`fs`) for the
        periodogram calculation, defaults to 1
        :type timestep: int (optional)
        :param plot: The `plot` parameter in the `psd` function is a boolean parameter that determines
        whether a plot of the Power Spectral Density (PSD) should be displayed or not. If `plot=True`, the
        function will display a semilog plot of the PSD. If `plot=False`, the, defaults to False
        :type plot: bool (optional)
        :return: If the `plot` parameter is set to `True`, the function will display a semilog plot of the
        Power Spectral Density (PSD) and will not return anything. If the `plot` parameter is set to
        `False`, the function will return the frequency array `f` and the PSD array `Pxx_den`.
        """
        fs = 1/timestep #sample frequency
        f, Pxx_den = periodogram(x=data, fs=fs)
        
        if plot:
            plt.semilogy(f, Pxx_den)
            plt.xlabel('frequency [Hz]')
            plt.ylabel('PSD [V**2/Hz]')
            plt.show()
        else:
            return f, Pxx_den

    @staticmethod
    def auto_correlation(data:np.array, lags:int=10, plot:bool=False):
        """
        The function `auto_correlation` calculates and optionally plots the autocorrelation of a given data
        array up to a specified number of lags.
        
        :param data: The `data` parameter is expected to be a NumPy array containing the data for which you
        want to calculate the auto-correlation
        :type data: np.array
        :param lags: The `lags` parameter in the `auto_correlation` function specifies the number of lags to
        be considered when calculating the autocorrelation. It determines how many lagged values of the data
        will be used to compute the autocorrelation values, defaults to 10
        :type lags: int (optional)
        :param plot: The `plot` parameter in the `auto_correlation` function is a boolean parameter that
        determines whether an autocorrelation plot should be displayed or not. If `plot=True`, the function
        will generate and display the autocorrelation plot using the provided data and specified number of
        lags. If `, defaults to False
        :type plot: bool (optional)
        :return: The function `auto_correlation` is currently set to return a `NotImplementedError` when the
        `plot` parameter is set to `False`.
        """
        data = SignalProcessing.detrend(data)
        
        if plot:
            # Adding plot title.
            plt.title("Auto-correlation Plot")
            # Providing x-axis name.
            plt.xlabel("Lags") 
            # Plotting the Autocorrelation plot.
            plt.acorr(data, maxlags = lags, normed=True)
            # Displaying the plot.
            plt.grid(True)
            plt.show()
        
        else:
            #TODO: output the auto correlation as np array
            return NotImplementedError

    @staticmethod
    def cross_correlation(data1: np.array, data1_timestep: float, data2: np.array, data2_timestep: float, lags: int = None, plot: bool = False):
        # Ensure the input data arrays are non-empty
        if len(data1) == 0 or len(data2) == 0:
            raise ValueError("Input data arrays must be non-empty.")

        # Create time vectors based on the provided timesteps
        time_data1 = np.arange(0, len(data1) * data1_timestep, data1_timestep)
        time_data2 = np.arange(0, len(data2) * data2_timestep, data2_timestep)
        
        # Ensure time vectors cover the same range
        common_start_time = max(time_data1[0], time_data2[0])
        common_end_time = min(time_data1[-1], time_data2[-1])
        
        if common_start_time >= common_end_time:
            raise ValueError("No overlapping time range between data1 and data2.")

        # Create a common time vector with the smaller timestep for resampling
        common_timestep = min(data1_timestep, data2_timestep)
        common_time = np.arange(common_start_time, common_end_time, common_timestep)
        

        # Interpolate data1 and data2 to the common time vector
        interpolator_data1 = interp1d(time_data1, data1, kind='linear', fill_value="extrapolate")
        interpolator_data2 = interp1d(time_data2, data2, kind='linear', fill_value="extrapolate")

        resampled_data1 = interpolator_data1(common_time)
        resampled_data2 = interpolator_data2(common_time)

        # Dynamically determine the number of lags
        if lags is None:
            lags = min(len(resampled_data1), len(resampled_data2)) // 75  # Example: 10% of the shorter series

        if plot:
            if len(resampled_data1) == 0 or len(resampled_data2) == 0:
                raise ValueError("Resampled data arrays are empty.")
            plt.title("Cross-correlation Plot")
            plt.xlabel("Lags")
            plt.xcorr(resampled_data1, resampled_data2, maxlags=lags, normed=True)
            plt.grid(True)
            plt.show()
        else:
            if len(resampled_data1) == 0 or len(resampled_data2) == 0:
                raise ValueError("Resampled data arrays are empty.")
            # Calculating cross-correlation
            cross_corr = np.correlate(resampled_data1 - np.mean(resampled_data1), resampled_data2 - np.mean(resampled_data2), mode='full')
            # Normalizing the cross-correlation
            cross_corr = cross_corr / (np.std(resampled_data1) * np.std(resampled_data2) * len(resampled_data1))
            # Returning the central part of the cross-correlation
            mid = len(cross_corr) // 2
            return cross_corr[mid - lags: mid + lags + 1]


    @staticmethod
    def align_timeseries(data:list):
        #TODO: make a method that aligns a list of timeseries data that has different:
        #TODO: starting and end points
        #TODO: sample rates
        #Is it better to have these as pandas dfs or a list of numpy arrays?
        pass

    @staticmethod
    def moving_average(self, df) -> pd.DataFrame:
        return NotImplementedError

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