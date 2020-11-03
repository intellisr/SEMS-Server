from flask import Flask, render_template, redirect, url_for, request ,session,jsonify,json,request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from tinydb import TinyDB, Query
from functools import reduce
from operator import add 
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
    #dayCount(content["col1"],Uid)   
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
    #loading the trained algorithm
    result=algorithm.predict([[val1,val2,val3,val4,val5,val6,val7,val8,val9,val10,val11,val12,val13,val14,val15,val16,val17]])
    print(result[0])
    return jsonify(result[0])

@app.route('/forcastGAP',methods=['GET','POST']) 
def forcastGAP():
    if request.method == 'POST':
         data = request.get_json()
         fileName=data['fname']
         weeks=data['weeks']
         user=data['user']
    fileName="SEMS2X"
    #user="V7r2O2fsqVYsNH0z8ydPItaGBSf1"
    weeks=4
    # ref = db.reference('forcastStatus/'+ user)
    # ref.set(0)                
    preProccess.preProccess(fileName)
    data=forcast.predictActivePower(fileName,weeks)
    result=data.tolist()
    # ref = db.reference('forcast/'+ user)
    # ref.set(result)   
    # ref = db.reference('forcastStatus/'+ user)
    # ref.set(1) 
    return jsonify(result)

@app.route('/anamaly',methods=['GET','POST']) 
def anamaly():
    if request.method == 'POST':
         data = request.get_json()
         fileName=data['fname']
         user=data['user'] 
    fileName="SEMS2X"
    user="V7r2O2fsqVYsNH0z8ydPItaGBSf1"                   
    anomaly_value,anomaly_date=arima.findAnomaly(fileName)
    resultSet=json.dumps(anomaly_value)
    return jsonify(resultSet)

@app.route("/imgs/<path:path>")
def images(path):
    return '<img src=' + url_for('static',filename=path+'plot.png') + '>'       

def dayCount(date,user):
    tdb = TinyDB('db.json')
    Home = Query()
    Temp=tdb.search(Home.user == user)
    if(Temp == []):
        tdb.insert({'user':user , 'date': date ,'days' : 0 })
        ref3 = db.reference('dailyUnits/'+ user)
        ref3.set(date) 
    else:
        Temp=Temp[0]
        if(str(Temp['date']) != str(date)):
            days= Temp['date'] + 1
            tdb.update({'user':user , 'date': date ,'days' : days })
            ref3 = db.reference('dailyUnits/'+ user)
            ref3.set(days)            

                
if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True, use_reloader=True)
   


