from flask import Flask, render_template, redirect, url_for, request ,session,jsonify,json,request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from tinydb import TinyDB, Query

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
    dailyAlgo(content["col1"],content["col10"],content["col7"],content["col8"],content["col9"])   
    return jsonify("Success")

def dailyAlgo(date,user,unit1,unit2,unit3):
    db = TinyDB('db.json')
    Home = Query()
    Temp=db.search(Home.user == user)
    if(Temp == None):
        db.insert({'user':user , 'date': date ,'unit1':unit1 ,'unit2':unit2 , 'unit3':unit3 })
    else:
        if(Temp.date == date):
            unit1Temp =  Temp.unit1 + unit1
            unit2Temp =  Temp.unit2 + unit2
            unit3Temp =  Temp.unit3 + unit3
            db.insert({'user':user , 'date': date ,'unit1':unit1Temp ,'unit2':unit2Temp , 'unit3':unit3Temp })
        else:
            ref = db.reference('dailyUnits/'+ user)
            ref.set({'user':Temp.user , 'date': Temp.date ,'unit1':Temp.unit1 ,'unit2':Temp.unit2 , 'unit3':Temp.unit3 })
            db.insert({'user':user , 'date': date ,'unit1':unit1 ,'unit2':unit2 , 'unit3':unit3 })    
            
if __name__ == "__main__":
	app.run(debug=True, use_reloader=True)
   


