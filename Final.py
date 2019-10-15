import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
	df = pd.read_csv("steam.csv", nrows=50)
	

main()



#df.drop(df[df.median_playtime > 500].index)
# df.plot(kind='scatter',x='price',y='average_playtime')
# plt.show()



def ownersToInteger():
	ownersMinMax = df.iloc[x]["owners"].split("-")
	ownersMinMax[0] = int(ownersMinMax[0])
	ownersMinMax[1] = int(ownersMinMax[1])
	ownersMean = (ownersMinMax[0] +  ownersMinMax[1]) / 2
	print(ownersMean)
	df.ix[x, 'owners'] = ownersMean
	print(df.iloc[1])