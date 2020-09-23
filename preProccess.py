#convert data into csv
from numpy import nan
from numpy import isnan
from pandas import read_csv
from pandas import to_numeric

# fill missing values with a value at the same time one day ago
def fill_missing(values):
	one_day = 60 * 24
	for row in range(values.shape[0]):
		for col in range(values.shape[1]):
			if isnan(values[row, col]):
				values[row, col] = values[row - one_day, col]

def preProccess(fileName):
    fileName='SEMS1X'                
    dataset = read_csv(fileName +'data.txt', sep=';', header=0, low_memory=False, infer_datetime_format=True, parse_dates={'datetime':[0,1]}, index_col=['datetime'])
    # mark all missing values
    dataset.replace('?', nan, inplace=True)
    # make dataset numeric
    dataset = dataset.astype('float32')
    # fill missing
    fill_missing(dataset.values)
    # add a column for for the remainder of sub metering
    values = dataset.values
    dataset['sub_metering_4'] = (values[:,0] * 1000 / 60) - (values[:,4] + values[:,5] + values[:,6])                
    dataset.to_csv(fileName+'temp.csv')
    
    dataset2 = read_csv(fileName+'temp.csv', header=0, infer_datetime_format=True, parse_dates=['datetime'], index_col=['datetime'])
    # resample data to daily
    daily_groups = dataset2.resample('D')
    daily_data = daily_groups.sum()
    # save
    daily_data.to_csv(fileName +'days_data.csv')