import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
# Load data
df=pd.read_csv('master.csv')
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df[:5] 
print(df.shape) 
print(df.head(5))

print("-------------------------------------spearman----------------------------------------------------------")
spcore=df.corr(method ='spearman')
print(df.corr(method ='spearman'))
ax = sb.heatmap(spcore, 
            xticklabels=spcore.columns,
            yticklabels=spcore.columns,
            cmap='RdBu_r',
            annot=True,
            linewidth=0.5)

plt.show(ax)            

print("-------------------------------------kendall----------------------------------------------------------")
print(df.corr(method ='kendall'))
