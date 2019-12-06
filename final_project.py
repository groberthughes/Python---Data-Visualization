import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections
import operator

# Percent positive ratings vs. Price of game
# Developers vs. Average playtime
# Steamspy_tags vs. playtime

#
def extract_ratings_vs_price(df):
	positive = df["positive_ratings"]
	negative = df["negative_ratings"]
	price = df["price"]
	ratings_vs_price = dict()
	for i in range(len(positive)):
		pos_count = positive[i]
		neg_count = negative[i]
		if ((pos_count + neg_count) >= 10000): # If there are 10000 or more ratings on the game
			if float(price[i]) in ratings_vs_price.keys():
				ratings_vs_price[float(price[i])].append(pos_count / (pos_count + neg_count))
			else:
				ratings_vs_price[float(price[i])] = [pos_count / (pos_count + neg_count)]
	ratings_vs_price = collections.OrderedDict(sorted(ratings_vs_price.items()))
	for key in ratings_vs_price.keys():
		average = 0
		for rating in ratings_vs_price[key]:
			average += rating
		average /= len(ratings_vs_price[key])
		ratings_vs_price[key] = average
	return pd.DataFrame([ratings_vs_price.values()], columns = ratings_vs_price.keys())

#
def plot_ratings_vs_price(ratings_vs_price):
	ratings_vs_price.iloc[0].plot(color = "blue", label = "Average rating of games at x price")
	ax = plt.gca()
	ax.set_xlabel("Price of game (USD)")
	ax.set_ylabel("Average of ratings")
	plt.legend()
	plt.show()

#
def extract_dev_vs_playtime(df):
	positive = df["positive_ratings"]
	negative = df["negative_ratings"]
	devs = df["developer"]
	playtime = df["average_playtime"]
	devs_vs_playtime = dict()
	for i in range(len(devs)):
		pos_count = positive[i]
		neg_count = negative[i]
		dev = devs[i]
		time = playtime[i]
		if ((pos_count + neg_count) >= 10000): # If there are 10000 or more ratings on the game
			if dev in devs_vs_playtime.keys():
				devs_vs_playtime[dev].append(float(time))
			else:
				devs_vs_playtime[dev] = [float(time)]
	for key in devs_vs_playtime.keys():
		average = 0
		for av in devs_vs_playtime[key]:
			average += av
		average /= len(devs_vs_playtime[key])
		devs_vs_playtime[key] = average
	devs_vs_playtime = sorted(devs_vs_playtime.items(), key = operator.itemgetter(1))
	top_ten = devs_vs_playtime[-10::]
	ten = dict()
	index = []
	for pair in top_ten:
		ten[pair[0]] = pair[1]
		index.append(pair[0][0:4].upper())
	return pd.DataFrame(ten, index = ["10 Developers With Highest Average Playtime Across All Games"])

#
def plot_dev_vs_playtime(dev_vs_playtime):
	dev_vs_playtime.plot(kind = "bar", rot = 0)
	ax = plt.gca()
	ax.set_ylabel("Average Playtime")
	plt.show()

#
def extract_tags_vs_playtime(df):
	positive = df["positive_ratings"]
	negative = df["negative_ratings"]
	steam_tags = df["steamspy_tags"]
	playtime = df["average_playtime"]
	tags_vs_playtime = dict()
	for i in range(len(steam_tags)):
		pos_count = positive[i]
		neg_count = negative[i]
		tags = steam_tags[i]
		time = playtime[i]
		if ((pos_count + neg_count) >= 10000): # If there are 10000 or more ratings on the game
			for tag in tags.split(";"):
				if tag in tags_vs_playtime.keys():
					tags_vs_playtime[tag].append(float(time))
				else:
					tags_vs_playtime[tag] = [float(time)]
	for key in tags_vs_playtime.keys():
		average = 0
		for av in tags_vs_playtime[key]:
			average += av
		average /= len(tags_vs_playtime[key])
		tags_vs_playtime[key] = (average, len(tags_vs_playtime[key]))
	tags_vs_playtime = sorted(tags_vs_playtime.items(), key = operator.itemgetter(1))
	index = -1
	tags = []
	game_counts = []
	for i in range(10):
		tags.append(tags_vs_playtime[index][0])
		game_counts.append(tags_vs_playtime[index][1])
		index -= 1
	frame = pd.DataFrame(game_counts, index = tags, columns = ["Time", "Number"])
	return frame

#
def plot_tags_vs_playtime(tags_vs_playtime):
	ax = plt.gca()
	for tag in tags_vs_playtime.index:
		ax.scatter(tags_vs_playtime.loc[tag].Number, tags_vs_playtime.loc[tag].Time, label = tag)
	(a, b) = np.polyfit(tags_vs_playtime.Number, tags_vs_playtime.Time, 1)
	yp = np.polyval([a, b], tags_vs_playtime.Number)
	plt.plot(tags_vs_playtime.Number, yp, linestyle = "--")
	ax.legend()
	ax.set_xlabel("Number of games with Tag")
	ax.set_ylabel("Average Playtime")
	plt.show()

#
def main():
	df = pd.read_csv("C:\\Users\\ogree\\repos\\ista-131-final\\steam.csv")
	plot_ratings_vs_price(extract_ratings_vs_price(df))
	plot_dev_vs_playtime(extract_dev_vs_playtime(df))
	plot_tags_vs_playtime(extract_tags_vs_playtime(df))

main()