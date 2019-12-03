import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.parser import parse


""" 
	I focused my data manipulation on stratifying the data by developer, and making
	plots that show the similarities and differences between the various development
	companies over time

	Additionally, I did not hard-code any values for the developer names, thus the user 
	can change the developers list below to investigate various 
	combinations of developers they are interested in (as many developers as desired)
"""

#Change this to inspect different sets of developers from the dataset
developers = ["Ubisoft", "Electronic Arts", "BioWare", "Pandemic Studios", "Firaxis Games" ]


"""
---------------------------------------------------------------
		Company Stratified Sales over Time (scatterplot)
---------------------------------------------------------------
"""

def seperate_company_playtime_data(df):
	devSeries = []
	for dev in developers:
		devSeries.append(extract_company_playtime_data(df, dev))
	return devSeries

def extract_company_playtime_data(df, company):
	dfValve = df[df.developer == company]
	playtime = dfValve.average_playtime
	playtime.astype('int32')
	release = dfValve.release_date.apply(reformatDate)
	series = pd.Series(index=release, data=playtime.values)
	series.sort_index(inplace=True)
	return series

def plot_stratified_game_playtime(developerSeries):
	for i in range(len(developerSeries)):
		dev = developerSeries[i]
		plt.scatter(dev.index, dev.values, label=developers[i])
		(m, b) = np.polyfit(dev.index, dev.values, 1)
		yp = np.polyval([m, b], dev.index)
		plt.plot(dev.index, yp, linestyle="--")

	ax = plt.gca()
	ax.get_yaxis().get_major_formatter().set_scientific(False)
	ax.get_xaxis().get_major_formatter().set_scientific(False)
	plt.legend()
	ax.set_ylabel("Mean Playtime (Hours)").set_fontsize(20)
	ax.set_xlabel("Year").set_fontsize(20)
	plt.title("Mean Playtime vs Time").set_fontsize(20)
	plt.show()


"""
---------------------------------------------------------------
		Company Stratified Revenue over Time (scatterplot)
---------------------------------------------------------------
"""

def seperate_company_revenue_data(df):
	devSeries = []
	for dev in developers:
		devSeries.append(extract_company_revenue_data(df, dev))
	return devSeries

def extract_company_revenue_data(df, company):
	dfValve = df[df.developer == company]
	dfValve["meanUsers"] = dfValve.owners.apply(meanFromRange)
	dfValve["meanRevenue"] = dfValve["meanUsers"] * dfValve["price"]
	price = dfValve["meanRevenue"]
	release = dfValve.release_date.apply(reformatDate)
	series = pd.Series(index=release, data=price.values)
	series.sort_index(inplace=True)
	return series

def plot_stratified_game_revenue(developerSeries):
	for i in range(len(developerSeries)):
		dev = developerSeries[i]
		plt.scatter(dev.index, dev.values, label=developers[i])
		(m, b) = np.polyfit(dev.index, dev.values, 1)
		yp = np.polyval([m, b], dev.index)
		plt.plot(dev.index, yp, linestyle="--")
	ax = plt.gca()
	ax.get_yaxis().get_major_formatter().set_scientific(False)
	ax.get_xaxis().get_major_formatter().set_scientific(False)
	ax.set_ylabel("$ Revenue (Total Sales * Price)").set_fontsize(20)
	ax.set_xlabel("Year").set_fontsize(20)
	plt.legend()
	plt.title("Game revenue vs Time").set_fontsize(20)
	plt.show()

"""
--------------------------------------------------------------------
					Market Share (Stacked Bar Chart)
--------------------------------------------------------------------

	Calculates a ratio of summed game ownership for each 5 year period
	for each game company selected, creates a stacked bar chart 
	representing relative market share in each 5 year period

"""

"""
	Iterates the data extraction method for each company specified by the user
"""
def seperate_company_market_share(df):
	devSeries = []
	for dev in developers:
		devSeries.append(extract_company_binned_ownership(df, dev))
	return devSeries

"""
	extracts the necessary data from a single company
"""
def extract_company_binned_ownership(df, company):
	#seperate by company
	dfValve = pd.DataFrame(data=df[df.developer == company])
	dfValve["owners"] = dfValve["owners"].apply(meanFromRange)
	dfValve["bin"] = dfValve["release_date"].apply(getBin)
	
	#bin into 5 year chunks
	bin06 =dfValve[dfValve["bin"] == '2006']
	bin08 =dfValve[dfValve["bin"] == '2008']
	bin10 =dfValve[dfValve["bin"] == '2010']
	bin12 =dfValve[dfValve["bin"] == '2012']
	bin14 =dfValve[dfValve["bin"] == '2014']

	#get summed ownership data per bin
	ownership06 = bin06["owners"].sum()
	ownership08 = bin08["owners"].sum()		
	ownership10 = bin10["owners"].sum()
	ownership12 = bin12["owners"].sum()
	ownership14 = bin14["owners"].sum()

	#make list of date stratified ownership data
	ownership = [ownership06, ownership08, ownership10, ownership12, ownership14]
	return ownership

"""
	Plots the ratio of relative market share for each 5 year bin of time
"""
def plot_stratified_market_share(binStratifiedCompanySales):

	index = np.arange(5)    
	bar_width = 0.4
	bars = [0] * len(binStratifiedCompanySales[0])
	for developerIndex in range(len(developers)):
		if developerIndex == 0:
			plt.bar(index, binStratifiedCompanySales[developerIndex], width = bar_width, label = developers[developerIndex])
		else:
			plt.bar(index, binStratifiedCompanySales[developerIndex], width = bar_width, bottom=bars, label = developers[developerIndex])
		bars = [x + y for x, y in zip(bars, binStratifiedCompanySales[developerIndex][:8])]

	ax = plt.gca()
	plt.xticks(np.arange(5), ('2004-2006', '2006-2008', '2008-2010', '2010-2012', '2012-2014', '2014-2016'))
	ax.set_ylabel("Number of Games Sold").set_fontsize(20)
	ax.set_xlabel("Year Range").set_fontsize(20)
	plt.legend()
	plt.title("Game Sales per 2 Year Cycle").set_fontsize(20)
	plt.show()


"""
-------------------------------------------------------------------
						Helper Functions
-------------------------------------------------------------------
"""

def load_csv():
	df = pd.read_csv("steam.csv")
	return df

def calculateTotalBinSales(devSeries):
	out = []
	for i in range(5):
		total = 0
		for developer in devSeries:
			total += int(developer[i])
		out.append(total)
	return out

def getBin(dateStr):
	dt = datetime.strptime(dateStr, '%Y-%m-%d')
	year = dt.year
	if (year < 2000):
		return '2000'
	elif (year < 2002):
		return '2002'
	elif (year < 2004):
		return '2004'
	elif (year < 2006):
		return '2006'
	elif (year < 2008):
		return '2008'
	elif (year < 2010):
		return '2010'
	elif (year < 2012):
		return '2012'
	else:
		return '2014'

def getYear(dateStr):
	dt = datetime.strptime(dateStr, '%Y-%m-%d')
	year = str(dt.year)[:4].zfill(2)
	return year

def reformatDate(dateStr):
	dt = datetime.strptime(dateStr, '%Y-%m-%d')
	year = str(dt.year)[:4].zfill(2)
	month = str(int(dt.month / 0.12))[:2].zfill(2)
	day = str(int(dt.day / 0.31))[:2].zfill(2)
	return int(year + month + day)

def meanFromRange(string):
	return (int(string.split("-")[0]) + int(string.split("-")[1])) / 2.0


"""
-------------------------------------------------------------------
								Main
-------------------------------------------------------------------
"""
def main():
	df = load_csv()

	# Average Playtime Scatterplot
	company_stratified_game_playtime = seperate_company_playtime_data(df)
	plot_stratified_game_playtime(company_stratified_game_playtime)


	#Revenue scatterplot
	company_stratified_game_revenue = seperate_company_revenue_data(df)
	plot_stratified_game_revenue(company_stratified_game_revenue)


	#Market Share scatterplot
	company_stratified_market_share = seperate_company_market_share(df)
	plot_stratified_market_share(company_stratified_market_share)


main()