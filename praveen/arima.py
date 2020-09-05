import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
import seaborn as sns
import pmdarima as pm
from pmdarima.model_selection import train_test_split
#warnings.filterwarnings("ignore")

ts_dataframe = pd.read_csv('sems100000xdataDays.csv', header=0 , index_col=['datetime'],parse_dates=['datetime'],usecols=['datetime','Global_active_power'])
#ts_dataframe = pd.read_csv('sems100000xdata.csv', header=0 , parse_dates=['datetime'], index_col=['datetime'],usecols=['datetime','Global_active_power'])
ts_dataframe = ts_dataframe[1:60]

def MAPE(y_orig, y_pred):
    diff = y_orig - y_pred
    MAPE = np.mean((abs(y_orig - y_pred)/y_orig)  * 100.)
    return MAPE

# Now, Anomaly Detection By Confidence Interval Method
# Using a simple Seasonal ARIMA model to highlight the idea
train, test = train_test_split(ts_dataframe, train_size=55)
#model = pm.auto_arima(train, trace=True, error_action='ignore', suppress_warnings=True)
model = pm.auto_arima(train, seasonal=True, m=12)
model.fit(train)
forecast = model.predict(test.shape[0]) 
mape = MAPE(test.values.reshape(1,-1)[0], forecast)


date = pd.date_range(start ='2006-12-16', periods = len(forecast) , freq ='MS') 

# upper bound and lower bound using MAPE
predicted_ub = forecast + (mape * 0.01 * forecast)

test_actuals = test.values.reshape(1,-1)[0]
anomaly_value = []
anomaly_date = []
for i in range(len(test_actuals)):
    if (abs(test_actuals[i]) > abs(predicted_ub[i])):
        anomaly_value.append(test_actuals[i])
        anomaly_date.append(date[i])
        
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
plt.show()