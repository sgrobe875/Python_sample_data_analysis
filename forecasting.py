import json
import matplotlib.pyplot as plt
import numpy as np
import datetime
import gzip
import statsmodels.tsa.seasonal as sm
from statsmodels.graphics.tsaplots import plot_acf
import pandas as pd
import math
from statistics import variance as var

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import numpy as np
from sklearn import linear_model

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from statsmodels.tsa.api import SimpleExpSmoothing




### Reading in data, initializing data structures, etc. #############


debug = False



def gz_json_loader(filename):
    '''
    Parameters
    ----------
    filename : a gzipped json file to be loaded into a list of dictionaries (jsons)

    Returns
    -------
    reviews: a list of dictionaries contianing information from the json

    '''
    reviews = []      # list to hold review data

    print("Loading in " + filename + " . . .\n")

    f = open(filename, 'r')
    reviews = json.loads(f.read())
    
    return reviews



sentiment_Category = gz_json_loader(filename = "../data/sentiment_category_one-hundred-thousand.json")
sentiment_Month = gz_json_loader(filename = "../data/sentiment_month_one-hundred-thousand.json")
sentiment_Cat_Time = gz_json_loader(filename = "../data/sentiment_cat_time_one-hundred-thousand.json")

reviews = gz_json_loader(filename = "../data/sorted_data_one-hundred-thousand.json")

cat_Month_Count = gz_json_loader(filename = "../data/catMonthCount_one-hundred-thousand.json")


categories = []
comp = []

# loop through all categories to get list of categories and list of avg. sentiment by category
for cat in sentiment_Category:
    categories.append(cat)
    comp.append(sentiment_Category[cat])



monthsSorted = []

# convert months to datetime, store in a list
for month in sentiment_Month:
    month = datetime.datetime.strptime(month, "%Y %m")
    monthsSorted.append(month)

# sort dates so they are in chronological order
monthsSorted.sort()

# convert these sorted months back into their original string form ("YYYY MM")
monthsSorted2 = monthsSorted.copy()
monthsSorted.clear()
for month in monthsSorted2:
    month = month.strftime("%Y %m")
    monthsSorted.append(month)
    
    
    


#### Prediction ##############################################################



# set limits
minMonth = datetime.datetime.strptime('2008-01', "%Y-%m")
maxMonth = datetime.datetime.strptime('2014-01', "%Y-%m")


# loop through all categories
for cat in sentiment_Category:

    y = []   # avg compound sentiment for the corresponding category and month
    x = []   # sorted months found in that category
        
    
    m = sentiment_Cat_Time[cat]
    
    # loop through all months, in order
    for month in monthsSorted2:
        
        if month < minMonth or month > maxMonth:
            pass
        
        else:
            # find string version of that month
            monthString = month.strftime("%Y %m")
            try:
                # if exists, append to x and y lists
                y.append(m[monthString])
                x.append(month)
    
            # if it does not exist, move on
            except KeyError:
                pass
            except TypeError:
                pass
    
    yList = []
    for item in y:
        yList.append(item['compound'])


    
    # Hold out last 10% of data for testing
    cutoffVal = math.floor(len(x) * 0.9)
    xTrain = x[0:cutoffVal]
    yTrain = yList[0:cutoffVal]
    xTest = x[cutoffVal:]
    yTest = yList[cutoffVal:]
    
    d = {"Time": xTrain, "Sentiment" : yTrain}
    training = pd.DataFrame(d)
    
    d2 = {"Time": xTest, "Sentiment" : yTest}
    testing = pd.DataFrame(d2)
    

    
    model = SimpleExpSmoothing(training['Sentiment'], initialization_method="heuristic")
    fit = model.fit(smoothing_level=0.2, optimized=False)
    fcast1 = fit.forecast(xTest).rename(r"$\alpha=0.2$")
    
    #scores = cross_val_score(model, x, y, cv=cv)
    
    plt.figure(figsize=(12, 8))
    plt.plot(x, yList, color="black")
    #plt.plot(training['Time'], fit.fittedvalues, color="blue")
    plt.plot(x, fit.fittedvalues, color="blue")
    #(line1,) = plt.plot(fcast1, marker="o", color="blue")
    plt.show()
    

    
