import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
	df = pd.read_csv("C:\\Users\\ogree\\repos\\ista-131-final\\steam.csv")

	# df.drop(df[df.median_playtime > 500].index)
	df.plot(kind='scatter', x='price', y='average_playtime')
	plt.show()

main()