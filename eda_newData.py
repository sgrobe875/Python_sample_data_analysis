#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 21:31:33 2022

@author: sarahgrobe
"""



# Initial EDA on the Amazon review data set


import json
import matplotlib.pyplot as plt
import numpy as np
import datetime



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

    print("Loading in data . . .\n")

    f = open(filename, 'r')
    reviews = json.loads(f.read())
    
    return reviews



sentiment_Category = gz_json_loader(filename = "../data/sent_New_Cats.json")
sentiment_Month = gz_json_loader(filename = "../data/sentiment_month_one-hundred-thousand.json")
sentiment_Cat_Time = gz_json_loader(filename = "../data/sent_NewCats_Time.json")



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
    
# at this point, monthsSorted = sorted months in string form; monthsSorted2 = sorted months in datetime form

# x = monthsSorted

# loop through all months to get avg compound, add to the list called y
y = []
for month in monthsSorted:
    y.append(sentiment_Month[month]['compound'])

# plot
plt.xlabel("Time (months)")
plt.ylabel("Compound sentiment")
plt.title("Compound review sentiment over time")

plt.plot(monthsSorted2, y, label=cat)
plt.tight_layout() 

plt.show()



# x = monthsSorted


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

    
    # plot results
    #plt.xlabel("Time (months)")
    plt.xlabel("Time")
    plt.ylabel("Compound sentiment")
    title = "Compound review sentiment over time for " + cat
    plt.title(title)
    
    #plt.xticks(rotation = 45)
    plt.ylim([-1.1, 1.1])
    
    plt.plot(x, y, label=cat)
    plt.tight_layout() 
    
    newYears = [datetime.datetime.strptime('1998-01', "%Y-%m"), datetime.datetime.strptime('1999-01', "%Y-%m"),
                datetime.datetime.strptime('2000-01', "%Y-%m"), datetime.datetime.strptime('2001-01', "%Y-%m"),
                datetime.datetime.strptime('2002-01', "%Y-%m"), datetime.datetime.strptime('2003-01', "%Y-%m"),
                datetime.datetime.strptime('2004-01', "%Y-%m"), datetime.datetime.strptime('2005-01', "%Y-%m"),
                datetime.datetime.strptime('2006-01', "%Y-%m"), datetime.datetime.strptime('2007-01', "%Y-%m"),
                datetime.datetime.strptime('2008-01', "%Y-%m"), datetime.datetime.strptime('2009-01', "%Y-%m"),
                datetime.datetime.strptime('2010-01', "%Y-%m"), datetime.datetime.strptime('2011-01', "%Y-%m"),
                datetime.datetime.strptime('2012-01', "%Y-%m"), datetime.datetime.strptime('2013-01', "%Y-%m"),
                datetime.datetime.strptime('2014-01', "%Y-%m"), datetime.datetime.strptime('2015-01', "%Y-%m")]
    
    newYears = [datetime.datetime.strptime('2008-01', "%Y-%m"), datetime.datetime.strptime('2009-01', "%Y-%m"),
                datetime.datetime.strptime('2010-01', "%Y-%m"), datetime.datetime.strptime('2011-01', "%Y-%m"),
                datetime.datetime.strptime('2012-01', "%Y-%m"), datetime.datetime.strptime('2013-01', "%Y-%m"),
                datetime.datetime.strptime('2014-01', "%Y-%m")]
    
    for year in newYears:
        plt.axvline(x=year, color = 'red', linestyle = 'dashed')
    
    plt.show()




## Volume of reviews data

reviews = gz_json_loader(filename = "../data/reviews_New_Cats.json")

sentiment_Month = {}

# obtain a list of all unique months in the dataset using the set data structure
catMonthCount = {}
months = set()
for cat in reviews:
    revs = reviews[cat]
    catMonthCount[cat] = {}
    for month in revs:
        months.add(month)
        catMonthCount[cat][month] = 0
# convert the set to a list
months = list(months)

# loop through all unique months
#volumeByMonth = []
monthCount = {}


for month in months:
    monthCount[month] = 0
    catMonthCount
    
    # loop through all months in all categories
    for cat in reviews:
        revs = reviews[cat]
        #catRevs = {}
        #catRevs[cat] = 0
        #numRevs = 0
        
        # a given month may not be accounted for in a given category, so use try/except 
        try:
            # loop through all reviews in a given month
            rev = revs[month]
            for r in rev:
                # add the review sentiment to a list
                monthCount[month] = monthCount[month] + 1
                catMonthCount[cat][month] = catMonthCount[cat][month] + 1
                #numRevs += 1
        # if the month is not there, do nothing        
        except KeyError:
            pass
        
        
    # add these results to a dictionary where the key is the month
    #volumeByMonth.append(monthCount)
    #monthCount.clear()
    





# set limits
minMonth = datetime.datetime.strptime('1998-01', "%Y-%m")
maxMonth = datetime.datetime.strptime('2014-01', "%Y-%m")


width = 0.4
figbar, axbar = plt.subplots()
m = []
y.clear()

for month in monthsSorted2:
    if month < minMonth or month > maxMonth:
        pass
    else:
        month = datetime.datetime.strftime(month, "%Y %m")
        try:
            monthCount[month]
            m.append(month)
            y.append(monthCount[month])
        except KeyError:
            pass
    
    
x = np.arange(len(m))


mLabels = []
for i in range(len(m)):
    if i%24 == 0:
        mLabels.append("Jan " + m[i][0:4])
    else:
        mLabels.append("")
        

rects1 = axbar.bar(x - width/2, y, width, label='Count')

axbar.set_ylabel('Number of Reviews')
#axbar.set_ylim([0,0.8])
axbar.set_title('Total Number of Reviews per Month')
#axbar.set_xticks(np.arange(min(x), max(x), 6.0))
#axbar.set_xticks(x)

distance_between_ticks = 12
reduced_xticks = x[np.arange(0, len(x), distance_between_ticks)]

axbar.set_xticks(x)

axbar.set_xticklabels(mLabels)
plt.xlabel("Time")

plt.xticks(rotation = 45)
 
figbar.tight_layout()
 
plt.show()







# set limits
minMonth = datetime.datetime.strptime('2008-01', "%Y-%m")
maxMonth = datetime.datetime.strptime('2012-01', "%Y-%m")


width = 0.5
figbar, axbar = plt.subplots()
m = []
y.clear()

for month in monthsSorted2:
    if month < minMonth or month > maxMonth:
        pass
    else:
        month = datetime.datetime.strftime(month, "%Y %m")
        try:
            monthCount[month]
            m.append(month)
            y.append(monthCount[month])
        except KeyError:
            pass
    
    
x = np.arange(len(m))


mLabels = []
for i in range(len(m)):
    if i%12 == 0:
        mLabels.append("Jan " + m[i][0:4])
    else:
        mLabels.append("")
        

rects1 = axbar.bar(x - width/2, y, width, label='Count')

axbar.set_ylabel('Number of Reviews')
#axbar.set_ylim([0,0.8])
axbar.set_title('Total Number of Reviews per Month')
axbar.set_xticks(x)
axbar.set_xticklabels(mLabels)
plt.xlabel("Time")

plt.xticks(rotation = 45)
 
figbar.tight_layout()
 
plt.show()




# set limits
minMonth = datetime.datetime.strptime('2012-01', "%Y-%m")
maxMonth = datetime.datetime.strptime('2014-01', "%Y-%m")


width = 0.4
figbar, axbar = plt.subplots()
m = []
y.clear()

for month in monthsSorted2:
    if month < minMonth or month > maxMonth:
        pass
    else:
        month = datetime.datetime.strftime(month, "%Y %m")
        try:
            monthCount[month]
            m.append(month)
            y.append(monthCount[month])
        except KeyError:
            pass
    
    
x = np.arange(len(m))


mLabels = []
for i in range(len(m)):
    if i%12 == 0:
        mLabels.append("Jan " + m[i][0:4])
    else:
        mLabels.append("")
        

rects1 = axbar.bar(x - width/2, y, width, label='Count')

axbar.set_ylabel('Number of Reviews')
#axbar.set_ylim([0,0.8])
axbar.set_title('Total Number of Reviews per Month')
axbar.set_xticks(x)
axbar.set_xticklabels(mLabels)
plt.xlabel("Time")

plt.xticks(rotation = 45)
 
figbar.tight_layout()
 
plt.show()





# set limits
minMonth = datetime.datetime.strptime('2008-01', "%Y-%m")
maxMonth = datetime.datetime.strptime('2014-01', "%Y-%m")


width = 0.4
figbar, axbar = plt.subplots()
m = []
y.clear()

for month in monthsSorted2:
    if month < minMonth or month > maxMonth:
        pass
    else:
        month = datetime.datetime.strftime(month, "%Y %m")
        try:
            monthCount[month]
            m.append(month)
            y.append(monthCount[month])
        except KeyError:
            pass
    
    
x = np.arange(len(m))


mLabels = []
for i in range(len(m)):
    if i%12 == 0:
        mLabels.append("Jan " + m[i][0:4])
    else:
        mLabels.append("")
        

rects1 = axbar.bar(x - width/2, y, width, label='Count')

axbar.set_ylabel('Number of Reviews')
#axbar.set_ylim([0,0.8])
axbar.set_title('Total Number of Reviews per Month')
axbar.set_xticks(x)
axbar.set_xticklabels(mLabels)
plt.xlabel("Time")

plt.xticks(rotation = 45)
 
figbar.tight_layout()
 
plt.show()









minMonth = datetime.datetime.strptime('2008-01', "%Y-%m")
maxMonth = datetime.datetime.strptime('2014-01', "%Y-%m")



# same thing as above but now for each category

for cat in reviews:
    width = 0.4
    figbar, axbar = plt.subplots()
    m = []
    y.clear()
    
    for month in monthsSorted2:
        if month < minMonth or month > maxMonth:
            pass
        else:
            month = datetime.datetime.strftime(month, "%Y %m")
            try:
                catMonthCount[cat][month]
                m.append(month)
                y.append(catMonthCount[cat][month])
            except KeyError:
                m.append(month)
                y.append(0)
                #pass
        
        
    x = np.arange(len(m))
    
    
    mLabels = []
    for i in range(len(m)):
        if i%12 == 0:
            mLabels.append("Jan " + m[i][0:4])
        else:
            mLabels.append("")
            
    
    rects1 = axbar.bar(x - width/2, y, width, label='Count')
    
    axbar.set_ylabel('Number of Reviews')
    #axbar.set_ylim([0,0.8])
    title = "Compound review sentiment over time for " + cat
    axbar.set_title(title)
    axbar.set_xticks(x)
    axbar.set_xticklabels(mLabels)
    
    plt.xlabel("Time")
    
    plt.xticks(rotation = 45)
     
    figbar.tight_layout()
     
    plt.show()




# write catMonthCount to file to use later
with open('../data/catMonthCount_one-hundred-thousand_reduced_cats.json', 'w') as fout:
    fout.write(json.dumps(catMonthCount)) 
fout.close()

















