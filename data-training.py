from numpy import nan
from numpy import isnan
from pandas import read_csv
from pandas import to_numeric
 

def fill_missing(values):
	one_day = 60 * 24
	for row in range(values.shape[0]):
		for col in range(values.shape[1]):
			if isnan(values[row, col]):
				values[row, col] = values[row - one_day, col]
 

dataset = read_csv('household_power_consumption.txt', sep=';', header=0, low_memory=False, infer_datetime_format=True, parse_dates={'datetime':[0,1]}, index_col=['datetime'])

dataset.replace('?', nan, inplace=True)

dataset = dataset.astype('float32')

fill_missing(dataset.values)

dataset['sub_metering_4'] = (values[:,0] * 1000 / 60) - (values[:,4] + values[:,5] + values[:,6])

dataset.to_csv('household_power_consumption.csv')