from flask import Flask, render_template, redirect, url_for, request ,session,jsonify,json,request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import joblib

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
    return jsonify("Success")

#predict tenure time and  resignation factor
@app.route('/predict_Profile',methods=['GET','POST']) 
def predict_Profile():    

    if request.method == 'POST':
        data = request.get_json()
        val1=eval(data['a'])
        val2=eval(data['b'])
        val3=eval(data['c'])
        val4=eval(data['d'])
        val5=eval(data['e'])
        val6=eval(data['f'])
        val7=eval(data['g'])
        val8=eval(data['h'])
        val9=eval(data['i'])
        val10=eval(data['j'])
        val11=eval(data['k'])
        val12=eval(data['l'])
        val13=eval(data['m'])
        val14=eval(data['n'])
        val15=eval(data['o'])
        val16=eval(data['p'])
    
    algorithm=joblib.load('profile.sav')
    #loading the trained algorithm
    result=algorithm.predict([[val1,val2,val3,val4,val5,val6,val7,val8,val9,val10,val11,val12,val13,val14,val15,val16]])
    
    return jsonify(result[0])  
            
if __name__ == "__main__":
	app.run(debug=True, use_reloader=True)
   


