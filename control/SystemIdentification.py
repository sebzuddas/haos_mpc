import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from control.SignalProcessing import SignalProcessing as dsp

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize

from sysidentpy.model_structure_selection import FROLS
from sysidentpy.basis_function._basis_function import Polynomial
from sysidentpy.metrics import root_relative_squared_error
from sysidentpy.utils.generate_data import get_siso_data
from sysidentpy.utils.display_results import results
from sysidentpy.utils.plotting import plot_residues_correlation, plot_results
from sysidentpy.residues.residues_correlation import (compute_residues_autocorrelation,compute_cross_correlation)

import pysindy as ps


class SystemIdentification:
    def __init__(self, input_sensors:list, output_sensors:list, data_train_percentage=80) -> None:
        """
        A class to perform system identification. 
        Needs two separate dataframes passed in, separate input_datas and output_datas
        """

        #TODO: need to take note of what is inputs and outputs, ie what variable is what
        #TODO: need to normalise all data
        #TODO: need to realign the inputs and outputs. 
        #TODO: need to split into training and testing
        #TODO: need to test whether its possible to do sysid from dsp (stationarity)
        #TODO: analyse the residulas, which should resemble white noise.
        #TODO: need to check the autocorrelation function of the residuals to ensure no significant correlation remains.
        
        # Convert input and output DataFrames to NumPy arrays
        self.input_data = input_data.values
        self.output_data = output_data.values.flatten()  # Ensure it's a 1D array
        self.output_data = self.output_data.reshape(-1, 1)# to make it work with model.fit
        self.data_train_percentage:int = data_train_percentage

        self.model = None
        self.num_inputs = self.input_data.shape[1]
        self.num_output_data = output_data.shape[1]#should be 1 according to sysidentpy

        #get x percent of the timeseries data and place into a training set. 
        self.training_input_data = input_data.sample(frac=data_train_percentage/100, random_state=42)
        self.training_output_data = output_data.sample(frac=data_train_percentage/100, random_state=42)

        # get the remaining timeseries data for a testing set. 
        self.training_input_data, self.testing_input_data, self.training_output_data, self.testing_output_data = train_test_split(
            self.input_data, self.output_data, train_size=data_train_percentage / 100, random_state=42)

        try:
            if self.input_data.shape[0] != self.output_data.shape[0]:# test that both sets of data have the same number of rows
                raise IndexError
            self.time_step = self.input_data.shape[0] # assign the number of rows to the time steps for the data if both inputs and outputs match
        except IndexError:
                print(f'input_datas:{input_data.index} and output_datas :{output_data.index} have different amounts of datapoints.')

    def fit_model(self):

        basis_function = Polynomial(degree=2)

        model = FROLS(
            order_selection=True,
            n_info_values=3,
            extended_least_squares=False,
            ylag=2,
            xlag=2,
            info_criteria="aic",
            estimator="least_squares",
            basis_function=basis_function,
        )

        model.fit(X=self.training_input_data, y=self.training_output_data)
        yhat = model.predict(X=self.testing_input_data, y=self.testing_output_data)
        rrse = root_relative_squared_error(self.testing_output_data, yhat)
        print(rrse)

        self.results = pd.DataFrame(
            results(
                model.final_model,
                model.theta,
                model.err,
                model.n_terms,
                err_precision=8,
                dtype="sci",
            ),
            columns=[
                "Regressors", 
                "Parameters", 
                "ERR"],
            )
        
        print(self.results)


    def fit_model_pysindy(self):
        # Example indicators, replace with relevant data if needed
        indicator_1 = np.ones_like(self.training_input_data) ## v2
        indicator_2 = np.ones_like(self.training_output_data)## v2

        # Candidate Models/basis functions
        # Instantiate the model using a polynomial library
        poly_order = 1  # Adjust based on your problem
        feature_library = ps.PolynomialLibrary(degree=poly_order, include_interaction=True)

        lag = 1

        # Combine indicators and lagged data## v2
        X_indicators = np.column_stack([np.roll(indicator_1, i) for i in range(1)])
        X_input = np.column_stack([np.roll(self.training_input_data, i) for i in range(lag + 1)])
        X_output = np.column_stack([np.roll(self.training_output_data, i) for i in range(lag + 1)])

        # Combine all features
        X = np.hstack([X_indicators, X_input[:, -1:], X_output[:, -1:]])## v2

        # # stack lagged data
        # X = np.column_stack([np.roll(self.training_input_data, i) for i in range(lag+1)] + 
        #                     [np.roll(self.training_output_data, i) for i in range(lag+1)])

        # Dynamically generate feature names based on the matrix structure#v2
        feature_names_indicators = [f"indicator_{i + 1}" for i in range(X_indicators.shape[1])]
        feature_names_input = [f"input_lag_{i}" for i in range(lag + 1)]
        feature_names_output = [f"output_lag_{i}" for i in range(lag + 1)]
        feature_names = feature_names_indicators + feature_names_input + feature_names_output


        #remove rows due to shifting
        X = X[lag:, :]
        self.training_output_data = self.training_output_data[lag:]

        optimizer = ps.STLSQ(threshold=0.21)#where threshold is Lambda

        differentiation_method = ps.FiniteDifference()#decide on the differentiation method to be used. 

        model = ps.SINDy(
            feature_names=feature_names,
            optimizer=optimizer, 
            feature_library=feature_library, 
            differentiation_method=differentiation_method, 
            use_cross_validation=True
            )#, feature_library=feature_library

        model.fit(X, t=1)

        print(X)

        model.print()
        print('test')



    def predict(self, input_data_data):
        pass

    def evaluate(self, predictions):
        pass

    def get_model(self):
        return self.model