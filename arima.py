import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
import seaborn as sns
import pmdarima as pm
from pmdarima.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
#import libraries


#read csv file unit wise electricity paramaters (global active power and data parameters only taken)

def MAPE(y_orig, y_pred):
    diff = y_orig - y_pred
    MAPE = np.mean((abs(y_orig - y_pred)/y_orig)  * 100.)
    return MAPE
#find the MEAN AVERAGE PERCENTAGE error

def findAnomaly(dataFile):
    dataFile = "SEMS2X"
    ts_dataframe = pd.read_csv(dataFile+"days_data.csv", header=0 , index_col=['datetime'],parse_dates=['datetime'],usecols=['datetime','Global_active_power'])
    ts_dataframe = ts_dataframe[1:60]

    # Now, Anomaly Detection By Confidence Interval Method
    train, test = train_test_split(ts_dataframe, train_size=55)
    #split data into test data and train data
    model = pm.auto_arima(train, seasonal=True, m=12)
    model.fit(train)


    #using auto arima function set monthly seasonal ARIMA Model
    forecast = model.predict(test.shape[0]) 
    #forecast data
    mape = MAPE(test.values.reshape(1,-1)[0], forecast)
    acc=int(100 - mape)
    print('ARIMA Model Accuracy:',acc,'%')
    #call mape function

    date = pd.date_range(start ='2006-12-16', periods = len(forecast) , freq ='MS') 
    #graph eka hadanna data set karagannawa

    # upper bound using MAPE
    predicted_ub = forecast + (mape * 0.01 * forecast)

    test_actuals = test.values.reshape(1,-1)[0]
    anomaly_value = []
    anomaly_date = []
    for i in range(len(test_actuals)):
        if (abs(test_actuals[i]) > abs(predicted_ub[i])):
            anomaly_value.append(test_actuals[i])
            anomaly_date.append(date[i])
    #if anomaly detected fill data into array using append       
    print(anomaly_value,anomaly_date)

    #upper bound and lower bound using MAPE
    predicted_ub = forecast + (mape * 0.01 * forecast)
    predicted_lb = forecast - (mape * 0.01 * forecast)
    plt.fill_between(date, predicted_lb, predicted_ub, alpha = 0.3, color = 'red')
    plt.plot(date, test.values.reshape(1,-1)[0], color = 'black')
    plt.plot(anomaly_date, anomaly_value, 'r*')
    plt.legend(['Actual Test', 'Anomaly Detected','Prediction Band'])
    plt.xlabel('datetime')
    plt.xticks(rotation=45)
    plt.ylabel('Global_active_power')
    plt.savefig(dataFile+'plot.png')
    #graph print

    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('sems-app-firebase-adminsdk-5jtol-c2d41ac3dd.json')
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://sems-app.firebaseio.com/'
    })

    bucket = storage.bucket()
    blob = bucket.blob(dataFile+'plot.png')
    blob.upload_from_filename(
        "/img/",
        content_type='image/png',)

    return anomaly_value,anomaly_date    
