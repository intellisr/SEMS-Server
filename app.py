from flask import Flask, render_template, redirect, url_for, request ,session,jsonify,json,request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from tinydb import TinyDB, Query
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
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
    dayCount(content["col1"],Uid)   
    return jsonify("Success")

@app.route("/report", methods=['POST','GET'])
def report():
    ref = db.reference('Paired/')
    Uid = ref.get()
    data_parsed = json.loads(Uid)
    header = data_parsed[0].keys()
    csv_writer.writerow(header)
    

@app.route('/predict_Profile',methods=['GET','POST']) 
def predict_Profile():    

    if request.method == 'POST':
        data = request.get_json()
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
        val12=data['oven']
        val13=data['micro']
        val14=data['refig']
        val15=data['car']
        val16=data['geys']
    
    algorithm=joblib.load('Profile.sav')
    #loading the trained algorithm
    result=algorithm.predict([[val1,val2,val3,val4,val5,val6,val7,val8,val9,val10,val11,val12,val13,val14,val15,val16]])
    print(result[0])
    return jsonify(result[0])

@app.route('/forcastGAP',methods=['GET','POST']) 
def forcastGAP():
    if request.method == 'POST':
         data = request.get_json()
         fileName=data['fname']
         weeks=data['weeks']           
    fileName="SEMS2X"
    weeks=3    
    preProccess.preProccess(fileName)
    data=forcast.predictActivePower(fileName,weeks)
    result=data.tolist()
    print(result)
    return jsonify(result)

@app.route('/anamaly',methods=['GET','POST']) 
def anamaly():
    if request.method == 'POST':
         data = request.get_json()
         fileName=data['fname']           
    fileName="SEMS2X"    
    anomaly_value,anomaly_date=arima.findAnomaly(fileName)
    bucket = storage.bucket(name="gs://sems-app.appspot.com")
    blob = bucket.blob(os.path.basename("/SEMS-Server/"+fileName+'plot.png'))
    #blob.upload_from_filename(fileName+'plot.png')
    result=[anomaly_value,anomaly_date]
    print(result)
    return jsonify(result)   

def dayCount(date,user):
    tdb = TinyDB('db.json')
    Home = Query()
    Temp=tdb.search(Home.user == user)
    #dateFormat=datetime.strptime(date, '%m/%d/%Y')
    #strdate=dateFormat.strftime('%Y-%m-%d')
    if(Temp == []):
        tdb.insert({'user':user , 'date': date })
        ref3 = db.reference('dailyUnits/'+ user)
        ref3.set(date) 
    else:
        Temp=Temp[0]
        if(str(Temp['date']) != str(date)):
            tdb.update({'user':user , 'date': date })
            ref3 = db.reference('dailyUnits/'+ user)
            ref3.set(date)            

                
if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True, use_reloader=True)
   


