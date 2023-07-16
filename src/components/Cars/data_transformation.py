import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler,OrdinalEncoder
import category_encoders as ce

from src.exception import CustomException
from src.logger import logging
from src.utils import save_obj



@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','Cars', "preprocessor.pkl")

class DataTransformation:
    def __init__(self) -> None:
        self.data_transformation_config = DataTransformationConfig()
        
    def get_data_transformer_obj(self):
        try:
            numerical_cols =  ['Year', 'Kms_Driven']
            less_category_cols = ['Company','Transmission','ownership','Fuel_Type']
            huge_category__cols = ['Area','Model','Passing']
            
            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy='median')),
                    ("scaler",StandardScaler())
                ]
            )
            logging.info("numerical columns encoding completed")
            ohe_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            
            te_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ('target_encoder',ce.TargetEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            
            oe_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy='most_frequent')),
                    ('ordinal_encoder', OrdinalEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            
            logging.info("Categorical columns encoding completed")
            
            
            logging.info(f"Numerical features : {numerical_cols}")
            logging.info(f"Categorical features foe One Hot Encoding: {less_category_cols}")
            logging.info(f"Categorical features for Target guided Encoding: {huge_category__cols}")
            # logging.info(f"Categorical features for Ordinal Encoding: ['Passing']")
            
            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline', num_pipeline, numerical_cols),
                    ('ohe_pipeline', ohe_pipeline, less_category_cols),
                    ('te_pipeline',te_pipeline, huge_category__cols),
                    # ('or_encoding',oe_pipeline,['Passing']),
                ]
            )
            
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
        
    def initiate_data_transformer(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("read train and test data completed")
            
            logging.info("Obtaining Preprocessing object")
            preprocessing_obj = self.get_data_transformer_obj()
            target_col_name = 'Price'

            input_feature_train_df=train_df.drop(columns=[target_col_name],axis=1)
            target_feature_train_df=train_df[target_col_name]

            input_feature_test_df=test_df.drop(columns=[target_col_name],axis=1)
            target_feature_test_df=test_df[target_col_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr = preprocessing_obj.fit_transform(X=input_feature_train_df,y=target_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logging.info('Done preprocessing')
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_obj(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )

        except Exception as e:
            raise CustomException(e,sys)