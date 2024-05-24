import unittest
import numpy as np
import pandas as pd

from data_management.DatabaseManager import DatabaseManager
from control.SignalProcessing import SignalProcessing
from peripherals.Sensor import Sensor

from dotenv import dotenv_values

class TestSensor(unittest.TestCase):

    def setUp(self):
        config = dotenv_values(".env")
        auth = config.get("HASS_IO_AUTH_TOKEN")
        url = config.get("HASS_IO_HOSTNAME")
        yaml_file = config.get("YAML_NAME")

        db_name = config.get("DATABASE_NAME")
        db_host = config.get("DATABASE_HOST")
        db_port = config.get("DATABASE_PORT")
        db_user = config.get("DATABASE_USER")
        db_password = config.get("DATABASE_PASSWORD")

        credentials_dict = {
            'db_name':db_name,
            'db_host':db_host,
            'db_port':db_port,
            'db_user':db_user,
            'db_password':db_password
        }

        dbmanager = DatabaseManager(credentials=credentials_dict)
        np.random.seed(0)
        self.sample_signal = np.sin(np.linspace(0, 2 * np.pi, 100)) + 0.5 * np.random.randn(100)
    
    # def test_real(self):
    #     pass

    # def test_virtual(self):
    #     pass

    # def test_dataframe_real_virtual(self):
    #     #compare the dataframes between real and virtual sensors
    #     pass

if __name__ == '__main__':
    unittest.main()