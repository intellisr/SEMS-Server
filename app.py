from flask import Flask, render_template, redirect, url_for, request ,session,jsonify,json,request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from tinydb import TinyDB, Query
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os

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
    iotData=str(content["col1"])+';'+str(content["col2"])+';'+str(content["col3"])+';'+str(content["col4"])+';'+str(content["col5"])+';'+str(content["col6"])+';'+str(content["col7"])+';'+str(content["col8"])+';'+str(content["col9"])+';'+str(content["col10"])+';'
    with open(''+content["col10"]+'data.txt', 'a') as f:
        json.dump(iotData, f, indent=2)
        f.write('\n')
    dailyAlgo(content["col1"],Uid,content["col7"],content["col8"],content["col9"])   
    return jsonify("Success")

def dailyAlgo(date,user,unit1,unit2,unit3):
    tdb = TinyDB('db.json')
    Home = Query()
    Temp=tdb.search(Home.user == user)
    dateFormat=datetime.strptime(date, '%m/%d/%Y')
    strdate=dateFormat.strftime('%Y-%m-%d')
    if(Temp == []):
        tdb.insert({'user':user , 'date': date ,'unit1':unit1 ,'unit2':unit2 , 'unit3':unit3 })
    else:
        Temp=Temp[0]
        print(Temp['date'])
        print(date)
        print("====================")
        if(str(Temp['date']) == str(date)):
            unit1Temp =  Temp['unit1'] + unit1
            unit2Temp =  Temp['unit2'] + unit2
            unit3Temp =  Temp['unit3'] + unit3
            tdb.update({'user':user , 'date': date ,'unit1':unit1Temp ,'unit2':unit2Temp , 'unit3':unit3Temp })
        else:
            ref3 = db.reference('dailyUnits/'+ user + '/' +strdate)
            ref3.set({'unit1':Temp['unit1'],'unit2':Temp['unit2'] , 'unit3':Temp['unit3']})
            tdb.update({'user':user , 'date': date ,'unit1':unit1 ,'unit2':unit2 , 'unit3':unit3 })
            print(strdate)

@app.route('/checkUnits') 
def checkUnits():
    #autoCorelate()
    ref4 = db.reference('dailyUnits/bxh0A3EyQobgNEsITN8oWxuODTw2')
    daily = ref4.get()
    for data in daily:
        days=daily[data]
        print(days)
    return jsonify("Success")

def autoCorelate():
    x = np.array([30,34,32,35,35,39,30,34,32,35,45,59,60,74,72,75,75,79])
    n = x.size
    norm = (x - np.mean(x))
    result = np.correlate(norm, norm, mode='same')
    acorr = result[n//2 + 1:] / (x.var() * np.arange(n-1, n//2, -1))
    lag = np.abs(acorr).argmax() + 1    
    r = acorr[lag-1]
    print(lag)
    #print(r)        
    # if np.abs(r) > 0.5:
    #   print('Appears to be autocorrelated with r = {}, lag = {}'. format(r, lag))
    # else: 
    #   print('Appears to be not autocorrelated')
    

            
if __name__ == "__main__":
	app.run(debug=True, use_reloader=True)
   


