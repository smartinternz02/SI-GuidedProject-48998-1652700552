# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 11:50:45 2022

@author: ShriyaPant
"""

import numpy as np
from flask import Flask, request, jsonify, render_template
import joblib
import json
import matplotlib
import matplotlib.pyplot as plt
import pandas
import os

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "detpdBejRqwEL5T2TfvHZV4p77aSx6lEvLqx0VVyFOnP"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
app = Flask(__name__)
#model = joblib.load("model.save")
trans=joblib.load('transform.save')





@app.route('/')
def predict():
    return render_template('manual_pred.html')

@app.route('/y_predict',methods=['POST','GET'])
def y_predict():
    
    x_test = [[float(x) for x in request.form.values()]]
    print('actual',x_test)
    x_test=trans.transform(x_test)
    print(x_test)
   # pred = model.predict(x_test)
    #print(pred)
    payload_scoring = {"input_data": [{"fields":[["f0","f1","f2","f3","f4","f5","f6"]],
    "values":[[1,2,3,2,1,4,5]]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/7045d37c-cc26-46c1-aa83-444c7eab4540/predictions?version=2022-06-05', json=payload_scoring,
     headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    pred=response_scoring.json()
    output=pred['predictions']
    print(output)
    outpt=pred['predictions'][0]['values'][0][0]
    print(outpt)

    return render_template('Manual_predict.html', prediction_text=('Permanent Magnet surface temperature: ',pred[0]))



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
