import pickle
import numpy as np
import pandas as pd

from src.pipeline.Bike.predict_pipeline import BikeCustomData,PredictPipeline_Bike

from flask import Flask,request,render_template

from sklearn.preprocessing import StandardScaler

application = Flask(__name__)

app = application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictbikedata',methods=['GET','POST'])
def predict_bike_data():
    if request.method == 'GET':
        return render_template('Bike/home.html')
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
        print(pred_df)
        
        predict_pipeline = PredictPipeline_Bike()
        result = predict_pipeline.predict(pred_df)
        result = result[0]/1000
        result_text = f" You can sell / buy the bike at approx {int(result)}000 RS."
        return render_template('Bike/home.html',result=result_text)


@app.route('/predictcardata',methods=['GET','POST'])
def predict_car_data():
    pass
    
if __name__=='__main__':
    app.run(host="0.0.0.0", debug=True)