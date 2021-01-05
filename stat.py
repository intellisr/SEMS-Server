from pandas import read_csv
from matplotlib import pyplot
series =read_csv("household_power_consumption_days_data.csv", header=0 , index_col=['datetime'],parse_dates=['datetime'],usecols=['datetime','Global_active_power'])
X = series.values
split = round(len(X) / 2)
X1, X2 = X[0:split], X[split:]
mean1, mean2 = X1.mean(), X2.mean()
var1, var2 = X1.var(), X2.var()
print('mean1=%f, mean2=%f' % (mean1, mean2))
print('variance1=%f, variance2=%f' % (var1, var2))
series.hist()
pyplot.show()