import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#import warnings
#warnings.filterwarnings('ignore')
#import statsmodels.api as sm

# Load data
df=pd.read_csv('analyse.csv')
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df[:5] 
print(df.shape) 
print(df.head(5))

print("-------------------------------------Pearson----------------------------------------------------------")
print(df.corr(method ='pearson'))

print("-------------------------------------kendall----------------------------------------------------------")
print(df.corr(method ='kendall'))
