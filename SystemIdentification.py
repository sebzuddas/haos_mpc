from sysidentpy.utils.generate_data import get_siso_data
from sysidentpy.model_structure_selection import FROLS
from sysidentpy.metrics import mean_squared_error


class SystemIdentification:
    def __init__(self, input, output) -> None:
        
        self.input = input
        self.output = output
        self.model = None

    def fit_model(self, model):
        pass

    def predict(self, input_data):
        pass

    def evaluate(self, predictions):
        pass

    


    
    
