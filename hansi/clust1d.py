import pandas as pd
import kmeans1d
import numpy as np

dataset=pd.read_csv('units.csv')
data =np.array(dataset)
k = 3
clusters, centroids = kmeans1d.cluster(data, k)

#print(clusters)
print("Law : 0 <= x <",centroids[0])
print("Medium : ",centroids[0],"<= x <",centroids[1])
print("High : ",centroids[0]," <= x")


