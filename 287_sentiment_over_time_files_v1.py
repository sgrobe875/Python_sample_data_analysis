### MODIFIED FILE FROM LAST SEMESTER TO WRITE FILES USING LARGER DATA SET ###

### modified: sentiment_over_time_files_v1.py


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


    
sentiment_aspect_category = gz_json_loader(filename = "../data/sentiment_by_aspect_by_category_one-hundred-thousand.json")
for cat in sentiment_aspect_category:
    l = []
    for aspect in sentiment_aspect_category[cat]:
        l.append(sentiment_aspect_category[cat][aspect])
    sentiment_Category[cat] = avg(l)
    
    
with open('../data/sentiment_category_one-hundred-thousand.json', 'w') as outfile:
    json.dump(sentiment_Category, outfile)
outfile.close()


    
        

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
                comp.append(result['compound'])
        # if the month is not there, do nothing        
        except KeyError:
            pass
        
    # record avg sentiment to a dictionary        
    sent = {'compound': avg(comp)}
    
    # add these results to a dictionary where the key is the month
    sentiment_Month[month] = sent.copy()
    
    sent.clear()
    
    
with open('../data/sentiment_month_one-hundred-thousand.json', 'w') as outfile:
    json.dump(sentiment_Month, outfile)
outfile.close()
    


    
    
    
    
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
        comp = []
        
    
        # a given month may not be accounted for in a given category, so use try/except 
        try:
            # add the review sentiment to a list
            rev = revs[month]
            for r in rev:
                result = analyzer.polarity_scores(r['reviewText'])
                comp.append(result['compound'])
                
            # record avg sentiment to a dictionary        
            sent = {'compound': avg(comp)}
    
            # add these results to a dictionary where the key is the month
            sent_time[month] = sent.copy()
            
            sent.clear()
                
        except KeyError:
            pass
    
    # add these to yet another dictionary, where the key is the category
    sentiment_Cat_Time[cat] = sent_time.copy()
    
    sent_time.clear()
    
file = '../data/sentiment_cat_time_one-hundred-thousand.json'
with open(file, 'w') as outfile:
    json.dump(sentiment_Cat_Time, outfile)
outfile.close()
    
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        