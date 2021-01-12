from flask import Flask, render_template, redirect, url_for, request ,session,jsonify,json,request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from functools import reduce
from operator import add 
import numpy as np
import joblib
import os
import json
import csv
import preProccess
import forcast
import arima

# Fetch the service account key JSON file contents
cred = credentials.Certificate('sems-app-firebase-adminsdk-5jtol-c2d41ac3dd.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sems-app.firebaseio.com/'
})

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route("/", methods=['POST','GET'])
def main():
    if request.method == 'POST':
       content = request.get_json()    
    ref = db.reference('Paired/'+ content["col10"])
    Uid = ref.get()
    ref2 = db.reference('Units/'+ Uid)
    ref2.update(content)
    iotData=str(content["col1"])+';'+str(content["col2"])+';'+str(content["col3"])+';'+str(content["col4"])+';'+str(content["col5"])+';'+str(content["col6"])+';'+str(content["col7"])+';'+str(content["col8"])+';'+str(content["col9"])+';'
    with open(''+content["col10"]+'data.txt', 'a') as f:
        json.dump(iotData, f, indent=2)
        f.write('\n') 
    return jsonify("Success")
    

@app.route('/predict_Profile',methods=['GET','POST']) 
def predict_Profile():    

    if request.method == 'POST':
        data = request.get_json()
        print(data)
        val1=data['solar']
        val2=data['male']
        val3=data['female']
        val4=data['child']
        val5=data['adult']
        val6=data['emp']
        val7=data['income']
        val8=data['district']
        val9=data['size']
        val10=data['aircon']
        val11=data['fan']
        val12=data['micro']
        val13=data['tv']
        val14=data['refig']
        val15=data['iron']
        val16=data['geys']
        val17=data['wash']
    
    algorithm=joblib.load('Profile.sav')
    result=algorithm.predict([[0,2,2,0,0,3,2,2,2,1,2,0,1,1,1,1,1]])
    #result=algorithm.predict([[val1,val2,val3,val4,val5,val6,val7,val8,val9,val10,val11,val12,val13,val14,val15,val16,val17]])
    return jsonify(result[0])

@app.route('/forcastGAP',methods=['GET','POST']) 
def forcastGAP():
    if request.method == 'POST':
         data = request.get_json()
         fileName=data['fname']
         weeks=data['weeks']
    fileName="SEMS2X"
    weeks=4              
    preProccess.preProccess(fileName)
    data=forcast.predictActivePower(fileName,weeks)
    result=data.tolist()
    return jsonify(result)

@app.route('/anamaly',methods=['GET','POST']) 
def anamaly():
    if request.method == 'POST':
         data = request.get_json()
         fileName=data['fname']
    fileName="SEMS2X"                   
    arima.findAnomaly(fileName)
    return jsonify("success")

@app.route("/imgs/<path:path>")
def images(path):
    return '<img src=' + url_for('static',filename=path+'plot.png') + '>'
           
                
if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True, use_reloader=True)
   


