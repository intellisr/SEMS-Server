import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import joblib

dataset=pd.read_csv('master.csv').values

dataset = dataset[~np.isnan(dataset).any(axis=1)]
data=dataset[:,0:17]
target=dataset[:,17]

#dataset splitting function
train_data,test_data,train_target,test_target=train_test_split(data,target,test_size=0.3)

algorithm=SVC(kernel='rbf',gamma ='auto')
#loading the SVM algorithm into "algorithm"

#print(train_target)
algorithm.fit(train_data,train_target)
#training

result=algorithm.predict(test_data)
#testing

acc=accuracy_score(test_target,result) #actual result,predicted result
#print(result)
print('Accuracy:',int(acc*100),'%')

joblib.dump(algorithm,'Profile.sav')