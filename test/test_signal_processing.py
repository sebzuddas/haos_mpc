import unittest
import numpy as np
import pandas as pd

from control.SignalProcessing import SignalProcessing

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

if __name__ == '__main__':
    unittest.main()