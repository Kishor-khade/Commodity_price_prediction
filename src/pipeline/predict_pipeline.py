import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_obj


class PredictPipeline_Bike:
    def __init__(self):
        pass
        
    def predict(self,features):
        try:
            model_path = 'artifacts/Bike/model.pkl'
            preprocessor_path = 'artifacts/Bike/preprocessor.pkl'
            model = load_obj(file_path=model_path)
            preprocessor = load_obj(file_path=preprocessor_path)        
            data_scaled = preprocessor.transform(features)
            pred = model.predict(data_scaled)
            return pred
        except Exception as e:
            raise CustomException(e,sys)

class BikeCustomData:
    def __init__(self, year:int, kms_driven:int,
                 cc_type:str, fuel_type:str, 
                 ownership:str, company:str, place:str):
        self.year = year
        self.kms_driven = kms_driven
        self.cc_type = cc_type
        self.fuel_type = fuel_type
        self.ownership = ownership
        self.company = company
        self.place = place
    
    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "company":[self.company],
                "cc_type":[self.cc_type],
                "year":[self.year],
                "kms_driven":[self.kms_driven],
                "fuel_type":[self.fuel_type],
                "ownership":[self.ownership],
                "place":[self.place]
            }
            return pd.DataFrame(custom_data_input_dict)
        
        except Exception as e:
            raise CustomException(e,sys)
        

class PredictPipeline_Car:
    def __init__(self) -> None:
        pass
    
    def predict(self, features):
        try:
            model_path = 'artifacts/Cars/model.pkl'
            preprocessor_path = 'artifacts/Cars/preprocessor.pkl'
            model = load_obj(file_path=model_path)
            preprocessor = load_obj(file_path=preprocessor_path)        
            data_scaled = preprocessor.transform(features)
            pred = model.predict(data_scaled)
            return pred
        except Exception as e:
            raise CustomException(e,sys)


class CarCustomData:
    def __init__(self, year:int, kms_driven:int, passing:str,
                 transmission:str, fuel_type:str, model:str,
                 ownership:str, company:str, area:str):
        self.company = company
        self.model = model
        self.year = year
        self.kms_driven = kms_driven
        self.transmission = transmission
        self.fuel_type = fuel_type
        self.ownership = ownership
        self.passing = passing
        self.area = area
    
    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'Company': [self.company],
                'Model': [self.model],
                'Year': [self.year],
                'Kms_Driven': [self.kms_driven],
                'Fuel_Type': [self.fuel_type],
                'Transmission': [self.transmission],
                'ownership': [self.ownership],
                'Passing': [self.passing],
                'Area': [self.area]
            }
            return pd.DataFrame(custom_data_input_dict)
        
        except Exception as e:
            raise CustomException(e,sys)
        