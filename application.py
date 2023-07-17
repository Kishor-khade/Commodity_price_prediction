import pickle
import numpy as np
import pandas as pd

from src.pipeline.predict_pipeline import (
    BikeCustomData,
    PredictPipeline_Bike,
    CarCustomData,
    PredictPipeline_Car)

from flask import Flask,request,render_template

from sklearn.preprocessing import StandardScaler

application = Flask(__name__)

app = application

## Route for a home page

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/predictbikedata',methods=['GET','POST'])
def predict_bike_data():
    if request.method == 'GET':
        return render_template('Bike/index.html')
    else:
        data = BikeCustomData(
            year = int(request.form.get('year')),
            kms_driven = int(request.form.get('kms_driven')),
            company = request.form.get('company'),
            ownership = request.form.get('ownership'),
            fuel_type = request.form.get('fuel_type'),
            place = request.form.get('place'),
            cc_type = request.form.get('cc_type'),
        )
        pred_df = data.get_data_as_dataframe()
        # print(pred_df)
        
        predict_pipeline = PredictPipeline_Bike()
        result = predict_pipeline.predict(pred_df)
        result = result[0]/1000
        result_text = f" You can sell / buy the bike at approx Rs.{int(result)}000."
        return render_template('result.html',result=result_text)


@app.route('/predictcardata',methods=['GET','POST'])
def predict_car_data():
    if request.method == 'GET':
        return render_template('Cars/index.html')
    else:
        data = CarCustomData(
            company = request.form.get('company'),
            model = request.form.get('model'),
            fuel_type = request.form.get('fuel_type'),
            transmission=request.form.get('transmission'),
            ownership = request.form.get('ownership'),
            kms_driven = int(request.form.get('kms_driven')),
            year = int(request.form.get('year')),
            area = request.form.get('area'),
            passing = request.form.get('passing'),
        )
        
        pred_df = data.get_data_as_dataframe()
        # print(pred_df)
        
        predict_pipeline = PredictPipeline_Car()
        result = predict_pipeline.predict(pred_df)
        result = result[0]/1000
        result_text = f" You can sell / buy the Car at approx Rs.{int(result)}000 "
        return render_template('result.html',result=result_text)
    

if __name__=='__main__':
    app.run(host="0.0.0.0")
