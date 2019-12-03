import numpy as np
import pandas as pd
import matplotlib.pyplot as plt





def main():
    dfsteam = pd.read_csv("steam.csv")
    dfsteam["multiplayer"] = False
    for i in range(len(dfsteam)):
        if "Multi-player" in dfsteam.iloc[i].categories.split(";"):
            dfsteam.at[i,"multiplayer"] = True
    
    multi = pd.Series()
    
    for row in dfsteam.index: 
        for col in dfsteam.columns:
            if col == 'multiplayer':
                if dfsteam.loc[row,col] == True:
                    dfsteam.loc[row,col] = 1
                elif dfsteam.loc[row,col] == False:
                    dfsteam.loc[row,col] = 0
    single = 0
    multi = 0
    series = dfsteam.loc[:, "multiplayer"]
    
    for i in range(len(series)):
        if series.iloc[i] == 1:
            multi += 1
        elif series.iloc[i] == 0 :
            single += 1
    print (str(multi) +"," + str(single))
    counts = [single,multi]
    objects = ('multiplayer','singleplayer')
    y_pos = np.arange(len(objects))
    plt.bar(y_pos,counts, align = 'center', color = 'red')
    plt.xticks(y_pos, objects)
    plt.ylabel('Total Amout of Games')
    plt.title("Multiplayer","Singleplayer")
    
    plt.show()
    
    dfsteam["owners"]= dfsteam["owners"].apply(means)
    selfpub = dfsteam[dfsteam["developer"]==dfsteam["publisher"]].sample(n = 50, random_state = 3)
    selfpub.sort_values("owners",inplace = True)
    thirdparty = dfsteam[dfsteam["developer"]!=dfsteam["publisher"]].sample(n = 50, random_state = 2)
    thirdparty.sort_values("owners",inplace = True)
#    
    
    
    plt.scatter(thirdparty.price, thirdparty.owners, label="third party published")
    plt.scatter(selfpub.price,selfpub.owners, label="self published")
    plt.legend()
    (m,b) = np.polyfit(thirdparty.price,thirdparty.owners , 1)
    yp = np.polyval([m,b],thirdparty.price)
    plt.plot(thirdparty.price, yp, linestyle = "--")
    (m,b) = np.polyfit(selfpub.price,selfpub.owners , 1)
    yp = np.polyval([m,b],selfpub.price)
    plt.plot(selfpub.price, yp, linestyle = "--")
    plt.ylabel('Owners')
    plt.xlabel('Price')
    plt.title("Self Pubilshed and Third Party")
    plt.show()
    
    avg_playtime = dfsteam[dfsteam["average_playtime"] > 0].sample(n = 50, random_state = 5)
    
    plt.scatter(avg_playtime.average_playtime, avg_playtime.achievements)
    (m,b) = np.polyfit(avg_playtime.average_playtime, avg_playtime.achievements , 1)
    yp = np.polyval([m,b],avg_playtime.average_playtime)
    plt.plot(avg_playtime.average_playtime, yp, linestyle = "--")
    plt.ylabel('Achievements')
    plt.xlabel('Average Playtime')
    plt.title("Achievements vs Average Playtime")
    plt.show()

    
    
    
    
    
                    
        
            
                   
    

                
                
                
        
            
def means(string):
    return (int(string.split("-")[0])+int(string.split("-")[1]))/ 2.0
main()
