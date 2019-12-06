import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


def read_in(csv):
    df= pd.read_csv(csv,header=0)
    return df

def owners_mean(df):
    owners=df['owners']
    L=[]
    for item in owners:
        L.append(item)
    for i in range(0,len(L)):
        L[i] = L[i].split('-')
        L[i] = (int(L[i][0]) + int(L[i][1]))/2
    s=pd.Series(L,dtype=int)
    s.astype(int)
    df['owners']=s
    

def avnp(df):
    df.plot(kind='scatter',x='achievements', y='owners',c='red',s=.5)
    axes=plt.gca()
    axes.set_xlim([0,1000])
    axes.set_ylim([0,10000000])
    ytl=[0,2000000,4000000,6000000,8000000,10000000]
    axes.set_yticklabels(ytl)
    axes.set_ylabel("Owners", fontsize=20)
    axes.set_xlabel("Achievements", fontsize=20)
    plt.show()


def total_reviews(df):
    s=pd.Series()
    d={}
    for row in df.iterrows():
        if row[1]['publisher'] not in d:
            d[row[1]['publisher']]=row[1]['positive_ratings']+row[1]['negative_ratings']
        else:
            d[row[1]['publisher']]+=row[1]['positive_ratings']+row[1]['negative_ratings']

    for key in d:
        s.set_value(key,d[key])
        
    s=s.nlargest(n=10)
    s.plot.bar()
    axes=plt.gca()
    axes.set_ylabel("Ratings", fontsize=20)
    axes.set_xlabel("Publishers", fontsize=20)
    
    plt.show()


def price_play(df):
    df.plot(kind='scatter',x='price', y='median_playtime',c='green',s=1)
    axes=plt.gca()
    axes.set_ylabel("Average Playtime", fontsize=20)
    axes.set_xlabel("Price in USD", fontsize=20)
    axes.set_xlim([0,100])
    axes.set_ylim([0,1000])
    plt.show()
    

    

