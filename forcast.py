# univariate multi-step lstm
from math import sqrt
from numpy import split
from numpy import array
from pandas import read_csv
from sklearn.metrics import mean_squared_error
from matplotlib import pyplot
from tensorflow.keras.models import Sequential,load_model
from tensorflow.keras.layers import Dense, Flatten, LSTM
import joblib

# split a univariate dataset into train/test sets
def split_dataset(data):
	# split into standard weeks
	train = data[0:]
	# restructure into windows of weekly data
	train = array(split(train, len(train)/7))

	return train

# convert history into inputs and outputs
def to_supervised(train, n_input, n_out=7):
	# flatten data
	data = train.reshape((train.shape[0]*train.shape[1], train.shape[2]))
	X, y = list(), list()
	in_start = 0
	# step over the entire history one time step at a time
	for _ in range(len(data)):
		# define the end of the input sequence
		in_end = in_start + n_input
		out_end = in_end + n_out
		# ensure we have enough data for this instance
		if out_end <= len(data):
			x_input = data[in_start:in_end, 0]
			x_input = x_input.reshape((len(x_input), 1))
			X.append(x_input)
			y.append(data[in_end:out_end, 0])
		# move along one time step
		in_start += 1
	return array(X), array(y)

def build_model(train, n_input):
	# prepare data
	train_x, train_y = to_supervised(train, n_input)
	# define parameters
	verbose, epochs, batch_size = 1, 70, 16
	n_timesteps, n_features, n_outputs = train_x.shape[1], train_x.shape[2], train_y.shape[1]
	# define model
	model = Sequential()
	model.add(LSTM(200, activation='relu', input_shape=(n_timesteps, n_features)))
	model.add(Dense(100, activation='relu'))
	model.add(Dense(n_outputs))
	model.compile(loss='mse', optimizer='adam',metrics=['acc'])
	# fit network
	model.fit(train_x, train_y, epochs=epochs, batch_size=batch_size, verbose=verbose)
	model.save('sems.h5') 
	return model

# make a forecast
def forecast(model, history, n_input):
	# flatten data
	data = array(history)
	data = data.reshape((data.shape[0]*data.shape[1], data.shape[2]))
	# retrieve last observations for input data
	input_x = data[-n_input:, 0]
	# reshape into [1, n_input, 1]
	input_x = input_x.reshape((1, len(input_x), 1))
	# forecast the next week
	yhat = model.predict(input_x, verbose=1)
	# we only want the vector forecast
	yhat = yhat[0]
	return yhat

# evaluate a single model
def get_n_weeks(train, n_input ,n_weeks):
	# fit model
	model = build_model(train, n_input)
	#model = load_model('sems.h5')
	# history is a list of weekly data
	history = [x for x in train]
	# walk-forward validation over each week
	predictions = list()
	for i in range(n_weeks):
		# predict the week
		yhat_sequence = forecast(model, history, n_input)
		# store the predictions
		predictions.append(yhat_sequence)
		# get real observation and add to history for predicting the next week
		history.append(train[i, :])
	# evaluate predictions days for each week
	predictions = array(predictions)	
	return predictions	

def predictActivePower(dataFile,weeks):
	# load the new file
	dataset = read_csv(dataFile+"days_data.csv", header=0, infer_datetime_format=True, parse_dates=['datetime'], index_col=['datetime'])
	# split into train Weely
	train = split_dataset(dataset.values)
	# prepare data
	n_input = 7
	#train the model
	#model = build_model( train, n_input)
	result=get_n_weeks(train, n_input ,weeks)
	week1=sum(result[0])
	week2=sum(result[1])
	week3=sum(result[2])
	week4=sum(result[3])
	month=week1+week2+week3+week4 
	print("week1 : "+str(week1))
	print("week2 : "+str(week2))
	print("week3 : "+str(week3))
	print("week4 : "+str(week4))
	print("Next Month : "+str(month))

	return result

