import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from sysidentpy.model_structure_selection import FROLS
from sysidentpy.basis_function._basis_function import Polynomial
from sysidentpy.metrics import root_relative_squared_error
from sysidentpy.utils.generate_data import get_siso_data
from sysidentpy.utils.display_results import results
from sysidentpy.utils.plotting import plot_residues_correlation, plot_results
from sysidentpy.residues.residues_correlation import (compute_residues_autocorrelation,compute_cross_correlation)


class SystemIdentification:
    def __init__(self, input_data:pd.DataFrame, output_data:pd.DataFrame, data_train_percentage=80) -> None:
        """
        A class to perform system identification. 
        Needs two separate dataframes passed in, separate input_datas and output_datas
        """
        
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



    def predict(self, input_data_data):
        pass

    def evaluate(self, predictions):
        pass

    def get_model(self):
        return self.model