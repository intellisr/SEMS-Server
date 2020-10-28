import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#import warnings
import seaborn as sns
from matplotlib.dates import WeekdayLocator
import matplotlib.dates as mdates
#from pmdarima.model_selection import train_test_split
#from sklearn.metrics import accuracy_score
#import libraries

#read csv file unit wise electricity paramaters (global active power and data parameters only taken)
ax = pd.read_csv("SEMS2Xdays_data.csv", header=0 , index_col=['datetime'],parse_dates=['datetime'],usecols=['datetime','Global_active_power']).plot(title='Weekly Seasonality', figsize=(18,8))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
# set formatter
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%Y'))
# set font and rotation for date tick labels
plt.gcf().autofmt_xdate()

plt.show()


#train, test = train_test_split(ts_dataframe, train_size=20)
   
