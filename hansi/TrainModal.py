import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib

dataset=pd.read_csv('master.csv').values

dataset = dataset[~np.isnan(dataset).any(axis=1)]

data=dataset[:,0:16]
target=dataset[:,16]

from sklearn.model_selection import train_test_split
#dataset splitting function

train_data,test_data,train_target,test_target=train_test_split(data,target,test_size=0.3)

algorithm=SVC(kernel='rbf',gamma ='auto')
#loading the SVM algorithm into "algorithm"

#print(train_target)
algorithm.fit(train_data,train_target)
#training

result=algorithm.predict(test_data)
#testing

#print('Actual Target:',test_target)
#print('Predicted Target:',result)

acc=accuracy_score(test_target,result)

print('Accuracy:',int(acc*100),'%')

joblib.dump(algorithm,'Profile.sav')