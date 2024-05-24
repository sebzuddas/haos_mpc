import unittest
import numpy as np
import pandas as pd

from control.SignalProcessing import SignalProcessing
from peripherals.Sensor import Sensor

# Unit Tests
class TestSignalProcessing(unittest.TestCase):

    def setUp(self):
        np.random.seed(0)
        self.sample_signal = np.sin(np.linspace(0, 2 * np.pi, 100)) + 0.5 * np.random.randn(100)
    
    def test_detrend(self):
        detrended_signal = SignalProcessing.detrend(self.sample_signal)
        self.assertIsInstance(detrended_signal, np.ndarray)
        self.assertEqual(detrended_signal.shape, self.sample_signal.shape)
        self.assertAlmostEqual(np.mean(detrended_signal), 0, places=5)

    def test_fourier_transform(self):
        result = SignalProcessing.fourier_transform(self.sample_signal, plot=False)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertIn('Frequency', result.columns)
        self.assertIn('Amplitude', result.columns)
        self.assertTrue((result['Amplitude'] >= 0).all())
        self.assertTrue((result['Frequency'] >= 0).all())

    def test_cross_correlation(self):
        # Sanity check with synthetic data
        # Create two sine waves with a known phase shift
        t1 = np.arange(0, 1000, 30)  # time vector for data1
        t2 = np.arange(0, 1000, 1800)  # time vector for data2

        data1 = np.sin(2 * np.pi * t1 / 100)  # sine wave for data1
        data2 = np.sin(2 * np.pi * (t2 - 200) / 100)  # sine wave for data2 with a phase shift

        # Expected phase shift in terms of lag
        expected_lag = -200 // 30  # -200 is the phase shift in terms of the original timestep

        # Get the cross-correlation result
        cross_corr_result = SignalProcessing.cross_correlation(data1, 30, data2, 1800, lags=50, plot=False)

        # Check the type and shape of the result
        self.assertIsInstance(cross_corr_result, np.ndarray)
        self.assertEqual(cross_corr_result.shape, (2 * 50 + 1,))

        # Find the lag with the maximum correlation
        max_lag_index = np.argmax(cross_corr_result) - 50  # since lags range from -50 to 50

        # Check if the peak correlation lag is as expected
        self.assertEqual(max_lag_index, expected_lag)


if __name__ == '__main__':
    unittest.main()