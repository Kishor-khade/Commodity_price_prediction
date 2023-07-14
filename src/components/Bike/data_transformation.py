import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
import category_encoders as ce

from src.exception import CustomException
from src.logger import logging
from src.utils import save_obj


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts','Bike', "preprocessor.pkl")
    
class DataTransformation:
    def __init__(self) -> None:
        self.data_transformation_config = DataTransformationConfig()
        
    def get_data_transformer_obj(self):
        try:
            numerical_cols =  ['year', 'kms_driven']
            less_category_cols = ['cc_type', 'fuel_type', 'ownership']
            huge_category__cols = ['company','place']
            
            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy='median')),
                    ("scaler",StandardScaler())
                ]
            )
            logging.info("numerical columns encoding completed")
            
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            
            target_encoding = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ('target_encoder',ce.TargetEncoder())
                ]
            )
            
            logging.info("Categorical columns encoding completed")
            
            
            logging.info(f"Numerical features : {numerical_cols}")
            logging.info(f"Categorical features with small number of categories: {less_category_cols}")
            logging.info(f"Categorical features with high number of categories: {huge_category__cols}")
            
            preprocessor = ColumnTransformer(
                [
                    ('num_pipeline', num_pipeline, numerical_cols),
                    ('cat_pipeline', cat_pipeline, less_category_cols),
                    ('target_encode_pipeline',target_encoding, huge_category__cols)
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
            target_col_name = 'price'
            numerical_columns = ['year', 'kms_driven']

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