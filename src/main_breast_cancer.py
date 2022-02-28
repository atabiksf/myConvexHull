import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from sklearn import datasets
from myConvexHull import myConvexHull 

data = datasets.load_breast_cancer() 
#create a DataFrame 
df = pd.DataFrame(data.data, columns=data.feature_names) 
df['Target'] = pd.DataFrame(data.target) 
print(df.shape)
df.head()

#visualisasi hasil ConvexHull
plt.figure(figsize = (10, 6))
colors = ['b','r']
plt.title('Mean Texture vs Mean Radius')
plt.xlabel(data.feature_names[0])
plt.ylabel(data.feature_names[1])
for i in range(len(data.target_names)):
    bucket = df[df['Target'] == i]
    bucket = bucket.iloc[:,[0,1]].values
    plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i])
    hullUpper, hullBottom = myConvexHull(bucket)
    idx = 0
    while idx < len(hullUpper)-1:
        p1 = hullUpper[idx]
        p2 = hullUpper[idx+1]
        plt.plot([p1[0],p2[0]],[p1[1],p2[1]],colors[i])
        idx += 1
    idx = 0
    while idx < len(hullBottom)-1:
        p1 = hullBottom[idx]
        p2 = hullBottom[idx+1]
        plt.plot([p1[0],p2[0]],[p1[1],p2[1]],colors[i])
        idx += 1
plt.legend()
plt.show()