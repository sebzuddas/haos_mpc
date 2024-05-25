import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from control.SignalProcessing import SignalProcessing as dsp

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize
from sklearn.preprocessing import MinMaxScaler, StandardScaler

from sysidentpy.model_structure_selection import FROLS
from sysidentpy.basis_function._basis_function import Polynomial
from sysidentpy.metrics import root_relative_squared_error
from sysidentpy.utils.generate_data import get_siso_data
from sysidentpy.utils.display_results import results
from sysidentpy.utils.plotting import plot_residues_correlation, plot_results
from sysidentpy.residues.residues_correlation import (compute_residues_autocorrelation,compute_cross_correlation)

import pysindy as ps


class SystemIdentification:
    def __init__(self, input_sensors:list, output_sensors:list, data_train_percentage:int=80) -> None:
        """
        A class to perform system identification using PySINDy. Uses a list of sensor objects as inputs. 
        """

        #TODO: need to take note of what is inputs and outputs, ie what variable is what
        #TODO: need to normalise all data - Done
        #TODO: need to realign the inputs and outputs - Done
        #TODO: need to split into training and testing - Done
        #TODO: need to test whether its possible to do sysid from dsp (stationarity)
        #TODO: analyse the residulas, which should resemble white noise.
        #TODO: need to check the autocorrelation function of the residuals to ensure no significant correlation remains.

        np.random.seed(42)
        self.model = None
        self.MinMaxScaler = MinMaxScaler()

        self.combined_list = input_sensors + output_sensors#combine the list of inputs and output sensors

        self.aligned_data = dsp.align_timeseries(self.combined_list, numpy=True)
        self.aligned_data = self.aligned_data[:, 1:]#get rid of the time column
        self.aligned_data_normalized = self.MinMaxScaler.fit_transform(self.aligned_data)

        ### Get a sample of the data
        split_index = int(data_train_percentage / 100 * self.aligned_data.shape[0])

        # Split the data into training and testing sets
        self.train_data = self.aligned_data[:split_index]
        self.test_data = self.aligned_data[split_index:]


        # print(self.aligned_data)
        # print(self.train_data, self.test_data)


    # def fit_model(self):

    #     basis_function = Polynomial(degree=2)

    #     model = FROLS(
    #         order_selection=True,
    #         n_info_values=3,
    #         extended_least_squares=False,
    #         ylag=2,
    #         xlag=2,
    #         info_criteria="aic",
    #         estimator="least_squares",
    #         basis_function=basis_function,
    #     )

    #     model.fit(X=self.training_input_data, y=self.training_output_data)
    #     yhat = model.predict(X=self.testing_input_data, y=self.testing_output_data)
    #     rrse = root_relative_squared_error(self.testing_output_data, yhat)
    #     print(rrse)

    #     self.results = pd.DataFrame(
    #         results(
    #             model.final_model,
    #             model.theta,
    #             model.err,
    #             model.n_terms,
    #             err_precision=8,
    #             dtype="sci",
    #         ),
    #         columns=[
    #             "Regressors", 
    #             "Parameters", 
    #             "ERR"],
    #         )
        
    #     print(self.results)


    def fit_model_pysindy(self, basis_order_poly: int = 4, sparsity = 0.5):
            # Create basis functions
            poly_order = basis_order_poly  # Adjust based on your problem

            polynomial_library = ps.PolynomialLibrary(degree=poly_order, include_interaction=True)
            fourier_library = ps.FourierLibrary(n_frequencies=5)  # Example Fourier library

            feature_library = ps.GeneralizedLibrary([polynomial_library, fourier_library])
            lag = 1

            # Prepare lagged data using combined aligned_data
            X = np.column_stack([np.roll(self.train_data, i, axis=0) for i in range(lag + 1)])

            # Remove initial rows due to shifting
            X = X[lag:, :]
            # Ensure X is of type float to avoid TypeErrors
            X = X.astype(float)
            self.train_data = self.train_data[lag:]

            # Dynamically generate feature names based on the matrix structure
            feature_names = [f"feature_{i}" for i in range(X.shape[1])]

            optimizer = ps.STLSQ(threshold=sparsity)  # Adjust threshold as needed
            differentiation_method = ps.FiniteDifference()  # Decide on the differentiation method to be used

            self.model = ps.SINDy(
                feature_names=feature_names,
                optimizer=optimizer,
                feature_library=feature_library,
                differentiation_method=differentiation_method
                # use_cross_validation=True
            )

            self.model.fit(X, t=1)
            self.model.print()


    def predict(self, input_data_data):
        pass

    def evaluate(self, predictions):
        pass

    def get_model(self):
        return self.model