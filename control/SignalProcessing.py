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
    def auto_correlation(signal:object, lags:int=10, plot:bool=False):
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
        data = signal.get_timseries(numpy=True)
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
    def cross_correlation(signal1:object, signal2:object, lags_percentage: int = 75, plot: bool = False):
        """
        The `cross_correlation` function calculates the cross-correlation between two signals, allowing for
        a specified percentage of lags and an optional plot of the cross-correlation.
        
        :param signal1: Signal object representing the first signal data
        :type signal1: object
        :param signal2: Signal2 is the second input signal for which you want to calculate the
        cross-correlation with signal1. This function `cross_correlation` takes two signals as input and
        calculates the cross-correlation between them. The `signal2` parameter represents the second signal
        object that you want to compare with `
        :type signal2: object
        :param lags_percentage: The `lags_percentage` parameter in the `cross_correlation` function
        determines what percentage of lags to consider when calculating the cross-correlation between two
        signals. By default, it is set to 75%, meaning that the function will use 75% of the lags available
        in the signals for, defaults to 75
        :type lags_percentage: int (optional)
        :param plot: The `plot` parameter in the `cross_correlation` function is a boolean parameter that
        determines whether a cross-correlation plot should be displayed or not. If `plot=True`, a
        cross-correlation plot will be generated showing the correlation between the two input signals. If
        `plot=False`, the function, defaults to False
        :type plot: bool (optional)
        :return: The function `cross_correlation` returns the central part of the cross-correlation between
        two signals after calculating and normalizing the cross-correlation values. The returned value is a
        numpy array representing the cross-correlation values within the specified lags range.
        """

        if lags_percentage>=100:
            raise ValueError('Lags cannot be greater than 100%')
        
        signals = SignalProcessing.align_timeseries([signal1, signal2], numpy=True)# get a numpy array of the two signals
        signals = signals[:, 1:]# get rid of the first column which is time
        
        # Dynamically determine the number of lags
        lags = int(signals.shape[0] * lags_percentage/100) # get the number of rows (samples) and find 75% of the lags

        if plot:
            plt.title("Cross-correlation Plot")
            plt.xlabel("Lags")
            plt.xcorr(signals[:, 0], signals[:, 1], maxlags=lags, normed=True)
            plt.grid(True)
            plt.show()
        else:
            # Calculating cross-correlation
            cross_corr = np.correlate(signals[:, 0] - np.mean(signals[:, 0]), signals[:, 1] - np.mean(signals[:, 1]), mode='full')
            # Normalizing the cross-correlation
            cross_corr = cross_corr / (np.std(signals[:, 0]) * np.std(signals[:, 1]) * len(signals[:, 1]))
            # Returning the central part of the cross-correlation
            mid = len(cross_corr) // 2
            return cross_corr[mid - lags: mid + lags + 1]

    @staticmethod
    def align_timeseries(data:list, earliest_time=None, numpy=False):
        """
        The `align_timeseries` function aligns and resamples a list of time series data with different
        starting and ending points and sample rates, returning either a combined pandas DataFrame or a numpy
        array based on the specified parameters.
        
        :param data: The `align_timeseries` function you provided seems to align a list of time series data
        with different starting and ending points and sample rates. It converts the data into pandas
        DataFrames, aligns them based on the most recent first entry and the final entry, resamples them to
        a common sampling frequency
        :type data: list
        :param earliest_time: The `earliest_time` parameter in the `align_timeseries` function is used to
        specify a specific starting time for the aligned time series data. If provided, the function will
        align the time series data starting from this specified time. If not provided (defaulting to
        `None`), the function
        :param numpy: The `numpy` parameter in the `align_timeseries` function determines whether the output
        should be returned as a NumPy array (`numpy=True`) or as a pandas DataFrame (`numpy=False`). If
        `numpy=True`, the function will convert the combined DataFrame into a NumPy array before returning
        it, defaults to False (optional)
        :return: The `align_timeseries` function returns either a combined pandas DataFrame or a numpy
        array, depending on the value of the `numpy` parameter. If `numpy` is set to `True`, the function
        returns the combined DataFrame converted to a numpy array. Otherwise, it returns the combined pandas
        DataFrame.
        """
        #TODO: make a method that aligns a list of timeseries data that has different:
        #TODO: starting and end points - end points will be almost the same
        #TODO: sample rates
        #Is it better to have these as pandas dfs or a list of numpy arrays?

        dataframes_list = [element.get_timeseries() for element in data] # now we get a list of python dataframes
        timestep_list = [element.get_timestep() for element in data] # get the sampling time for all 
        min_timestep = min(timestep_list) # get the smallest timestep to resample from
        
        sample_time = f'{min_timestep}S'

        #find the most recent first entry within the time series
        first_entries = [df.iloc[0] for df in dataframes_list]
        most_recent_first_entry = max(first_entries, key=lambda x: x['time'])

        last_entries = [df.iloc[-1] for df in dataframes_list]
        final_entry = max(last_entries, key=lambda x: x['time'])

        aligned_dataframes = [df[df.index >= most_recent_first_entry.name] for df in dataframes_list]# aligned to the start
        trimmed_dataframes = [df[df.index <= final_entry.name] for df in aligned_dataframes]# cut off at the end

        # Ensure the 'time' column is a datetime index
        for i in range(len(trimmed_dataframes)):
            trimmed_dataframes[i]['time'] = pd.to_datetime(trimmed_dataframes[i]['time'])
            trimmed_dataframes[i].set_index('time', inplace=True)

        resampled_dataframes = [df.resample(sample_time).interpolate() for df in trimmed_dataframes]# resampled with the same sampling frequency

        combined_df = pd.concat(resampled_dataframes, axis=1, join='inner') # turn into one dataframe 

        if numpy:
            combined_df.reset_index(inplace=True)# make the time index a column that isn't an index
            return combined_df.to_numpy()
        
        else:
            return combined_df

    @staticmethod
    def stationarity():
        #dickyfuller test, needed to check for for whether sysID methods are going to be successful. 
        #TODO: implement a method to check for stationarity
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