#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 11:18:57 2021

@author: sarahgrobe
"""

import json
import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
import numpy as np
import matplotlib.pyplot as plt
import datetime



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
    
    
def avg(numList):
    '''Accepts a list of numbers and returns the average'''
    return sum(numList)/len(numList)








# load in file 
reviews = gz_json_loader(filename = "../data/sorted_data_one-hundred-thousand.json")

# initalize sentiment analyzer
analyzer = SentimentIntensityAnalyzer ()




###### record sentiment analysis by category #############################################################
sentiment_Category = {}

# loop through all categories 
for cat in reviews:
    neg = []
    neu = []
    pos = []
    comp = []
    
    revs = reviews[cat]
    
    # loop through each month
    for month in revs:
        rev = revs[month]
        for r in rev:
        #rev = rev[0]
            result = analyzer.polarity_scores(r['reviewText'])
            
            # sanity checks:
            #print(rev['reviewText'])
            #print(result['neg'], result['neu'], result['pos'], result['compound'])
            #print()
            
            # add sentiment results to a list
            neg.append(result['neg'])
            neu.append(result['neu'])
            pos.append(result['pos'])
            comp.append(result['compound'])
            
    # sanity checks:  
    #print(cat)
    #print("Neg: %.5f      Neu: %.5f      Pos: %.5f      Compound: %.5f" % (avg(neg), avg(neu), avg(pos), avg(comp)))
    #print(avg(neg), avg(neu), avg(pos), avg(comp))
    #print()
    
    # save these results to a dictionary for further analysis
    sent = {'neg':avg(neg), 'neu': avg(neu), 'pos': avg(pos), 'compound': avg(comp)}
    
    # add these results to overall dictionary (by category)
    sentiment_Category[cat] = sent.copy()
    
    sent.clear()
    
        

###### record sentiment analysis by month ####################################################################
sentiment_Month = {}

# obtain a list of all unique months in the dataset using the set data structure
months = set()
for cat in reviews:
    revs = reviews[cat]
    for month in revs:
        months.add(month)
# convert the set to a list
months = list(months)

# loop through all unique months
for month in months:
    neg = []
    neu = []
    pos = []
    comp = []
    
    # loop through all months in all categories
    for cat in reviews:
        revs = reviews[cat]
        
        # a given month may not be accounted for in a given category, so use try/except 
        try:
            # loop through all reviews in a given month
            rev = revs[month]
            for r in rev:
                # add the review sentiment to a list
                result = analyzer.polarity_scores(r['reviewText'])
                neg.append(result['neg'])
                neu.append(result['neu'])
                pos.append(result['pos'])
                comp.append(result['compound'])
        # if the month is not there, do nothing        
        except KeyError:
            pass
        
    # record avg sentiment to a dictionary        
    sent = {'neg':avg(neg), 'neu': avg(neu), 'pos': avg(pos), 'compound': avg(comp)}
    
    # add these results to a dictionary where the key is the month
    sentiment_Month[month] = sent.copy()
    
    sent.clear()
    
    
    
    
    
###### record sentiment analysis by category ################################################################
sentiment_Cat_Time = {}
sent_time = {}

# =============================================================================
# # obtain a list of all unique months in the data set
# months = set()
# for cat in reviews:
#     revs = reviews[cat]
#     for month in revs:
#         months.add(month)
# months = list(months)
# =============================================================================

    
# loop through all months in all categories
for cat in reviews:
    revs = reviews[cat]
    
    for month in months:
        neg = []
        neu = []
        pos = []
        comp = []
        
    
        # a given month may not be accounted for in a given category, so use try/except 
        try:
            # add the review sentiment to a list
            rev = revs[month]
            for r in rev:
                result = analyzer.polarity_scores(r['reviewText'])
                neg.append(result['neg'])
                neu.append(result['neu'])
                pos.append(result['pos'])
                comp.append(result['compound'])
                
            # record avg sentiment to a dictionary        
            sent = {'neg':avg(neg), 'neu': avg(neu), 'pos': avg(pos), 'compound': avg(comp)}
    
            # add these results to a dictionary where the key is the month
            sent_time[month] = sent.copy()
            
            sent.clear()
                
        except KeyError:
            pass
    
    # add these to yet another dictionary, where the key is the category
    sentiment_Cat_Time[cat] = sent_time.copy()
    
    sent_time.clear()
        
        
###############################################################################################################        
        
        
# make some pretty plots!



# Below plot commented out because not very useful, but didn't want to delete it entirely

# barplot of positive and negative by category
# =============================================================================
# categories = []
# positive = []
# negative = []
# 
# for cat in reviews:
#     categories.append(cat)
#     positive.append(sentiment_Category[cat]['pos'])
#     negative.append(sentiment_Category[cat]['neg'])
#     
#     
# x = np.arange(len(categories))
# width = 0.35
# fig, ax = plt.subplots()
# 
# rects1 = ax.bar(x - width/2, positive, width, label='Positive')
# rects2 = ax.bar(x - width/2, negative, width, label='Negative')
# 
# ax.set_ylabel('Accuracy')
# ax.set_ylim([0,0.3])
# ax.set_title('Accuracy of Each Classifier by Training Database')
# ax.set_xticks(x)
# ax.set_xticklabels(categories)
# ax.legend()
#  
# #ax.bar_label(rects1, padding=3)
# #ax.bar_label(rects2, padding=3)
# 
# plt.xticks(rotation = 90)
# #plt.xticks(rotation = 45)
#  
# fig.tight_layout()
#  
# plt.show()
# =============================================================================



###### barplot of compound by category ###########################################################
categories = []
comp = []

# loop through all categories to get list of categories and list of avg. sentiment by category
for cat in reviews:
    categories.append(cat)
    comp.append(sentiment_Category[cat]['compound'])

    
# set up graph parameters    
x = np.arange(len(categories))
width = 0.4
fig, ax = plt.subplots()

rects1 = ax.bar(x - width/2, comp, width, label='Compound')

ax.set_ylabel('Compound Sentiment')
ax.set_ylim([0,0.8])
ax.set_title('Average Compound Sentiment by Category')
ax.set_xticks(x)
ax.set_xticklabels(categories)

plt.xticks(rotation = 90)
 
fig.tight_layout()
 
plt.show()

# compounds has a range of [-1,1], so we can see that in general reviews are pretty positive

        
     
        
        
###### line graph of compound sentiment over time (across all categories) #########################
monthsSorted = []

# convert months to datetime, store in a list
for month in months:
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

plt.plot(monthsSorted, y, label=cat)
plt.tight_layout() 

plt.show()



# save x and y data in plot above to a csv
file = open("../data/sentiment_over_time.csv", 'w')
for i in range(len(monthsSorted)):
    print(monthsSorted[i],",", y[i], sep='', file = file)
file.close()







###### create line graph for each category of compound over time #######################################


# x = monthsSorted

# loop through all categories
for cat in reviews:

    y = []   # avg compound sentiment for the corresponding category and month
    x = []   # sorted months found in that category
    
    m = sentiment_Cat_Time[cat]
    
    # loop through all months, in order
    for month in monthsSorted2:
        # find string version of that month
        monthString = month.strftime("%Y %m")
        try:
            # if exists, append to x and y lists
            y.append(m[monthString]['compound'])
            x.append(month)
        # if it does not exist, move on
        except KeyError:
            pass
    
    # plot results
    plt.xlabel("Time (months)")
    plt.ylabel("Compound sentiment")
    title = "Compound review sentiment over time for " + cat
    plt.title(title)
    
    plt.xticks(rotation = 45)
    plt.ylim([-1.1, 1.1])
    
    plt.plot(x, y, label=cat)
    plt.tight_layout() 
    
    plt.show()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        