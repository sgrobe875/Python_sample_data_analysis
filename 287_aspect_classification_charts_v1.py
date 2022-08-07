### MODIFIED FILE FROM LAST SEMESTER TO WRITE FILES USING LARGER DATA SET ###

### modified: aspect_classification_charts_v1.py


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 13 16:23:56 2021

@author: sarahgrobe
"""


# imports
import json
import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
import numpy as np





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





def find_max_aspect(counts, aspects):
    '''returns the name of the most commonly mentioned product aspect for a given review'''
    max_tally = 0
    for aspect in aspects:
        if counts[aspect] > max_tally:
            max_tally = counts[aspect]
            max_aspect = aspect
    
    
    if max_tally == 0:
        max_aspect = 'none'
    
    return max_aspect





def avg(numList):
    '''Accepts a list of numbers and returns the average'''
    try:
        return sum(numList)/len(numList)
    
    # this will occur if the aspect is not present
    except ZeroDivisionError:
        return 0









# load in file 
reviews = gz_json_loader(filename = "../data/sorted_data_one-hundred-thousand.json")


# initialize classification word lists for each aspect
price = ['pric', 'cost', 'dollar', 'expens', 'rip-off', 'worth', 'valu','ripoff','afford','paid','ripped-off']

durability = ['broke', 'durab', 'resistant', 'indestruct', 'shoddy', 'outlast', 'cheap','tough','dent',
              'degrad','sturdy']
 
aes = ['pretty','ugly','color','appearance','design', 'shiny', 'siz','comfy', 'small', 'large', 'big',
       'gorgeous','hideous']

performance = ['fast', 'slow', 'effective', 'function', 'work', 'lag','defect','versatil','distort','scam',
               'pos','safe','efficien','speed','faulty','reliab','flaw']

ease = ['easy', 'install', 'installation','usab','readab','usab','portab','effort']


# may or may not want to include a service category; if so, uncomment line below and add service to aspects dictionary
# service = ['rude', 'supervisor','seller','company','packag','polic','warrant', 'respon', 'representative','receipt']


# dictionary which uses name of aspect to point to the list of classification words
aspects = {'price':price, 'durability':durability, 'aesthetics':aes, 'performance': performance, 'ease of use': ease}

# dictionary to hold counts of each aspect, across all data
counts = {}





# determine most common aspect for each review

# start by looping through categories
for cat in reviews:
    revs = reviews[cat]
    
    # loop through each month
    for month in revs:
        rev = revs[month]
        
        # loop through each review in that month
        for r in rev:
            counts = {}
            text = r['reviewText']
            
            # loop through each aspect's classification words and tally their appearances
            for aspect in aspects:
                aspectWords = aspects[aspect]
                
                tally = 0
                
                for word in aspectWords:
                    if word in text:
                        tally += 1
                
                counts[aspect] = tally
            
            # record the most common aspect using function; append to the review
            r['aspect'] = find_max_aspect(counts, aspects)





# graph compound sentiment by aspect across all categories

# initalize sentiment analyzer
analyzer = SentimentIntensityAnalyzer ()

# start by creating dictionary with avg compound sentiment per aspect
sentiment_Aspect = {}
for aspect in aspects:
    sentiment_Aspect[aspect] = []
    

# piggybacking on this, count the number of reviews for each aspect
count_Aspect = {}
for aspect in aspects:
    count_Aspect[aspect] = 0



numSkipped = 0

# loop through all reviews, record compound sentiment to a list by aspect
for cat in reviews:
    revs = reviews[cat]
    
    for month in revs:
        rev = revs[month]
        
        for r in rev:
            asp = r['aspect']
            
            result = analyzer.polarity_scores(r['reviewText'])
            
            # this accounts for those with 'none' (which hopefully will eventually be zero, idk)
            try:
                sentiment_Aspect[asp].append(result['compound'])
                # increment aspect count
                c = count_Aspect[asp]
                count_Aspect[asp] = c + 1
                
            except KeyError:
                numSkipped += 1
                
                
print("Reviews not categorized:", numSkipped)


    
# loop through all apsects and average the lists made above    
for aspect in aspects:
    sentList = sentiment_Aspect[aspect]
    sentiment_Aspect[aspect] = avg(sentList)
    


with open('../data/sentiment_by_aspect_one-hundred-thousand.json', 'w') as outfile:
    json.dump(sentiment_Aspect, outfile)


with open('../data/count_by_aspect_one-hundred-thousand.json', 'w') as outfile:
    json.dump(count_Aspect, outfile)




aspectList = []

for aspect in count_Aspect:
    aspectList.append(aspect)



# create nested dictionaries of format {category: {aspect: avg. compound} } 
sentiment_Category_Aspect = {}

# nested dict of format {category: {aspect: count} }
count_Category_Aspect = {}

for cat in reviews:
    revs = reviews[cat]
    aspect_count = {}
    
    asp_sent = {}
    for aspect in aspectList:
        asp_sent[aspect] = []
        aspect_count[aspect] = 0
    
    for month in revs:
        rev = revs[month]
        
        for r in rev:
            asp = r['aspect']
            result = analyzer.polarity_scores(r['reviewText'])

            try:
                asp_sent[asp].append(result['compound'])
                c = aspect_count[asp]
                aspect_count[asp] = c + 1
                
            except KeyError:
                pass
            
    for aspect in asp_sent:
        sentList = asp_sent[aspect]
        asp_sent[aspect] = avg(sentList)
        
    sentiment_Category_Aspect[cat] = asp_sent
    count_Category_Aspect[cat] = aspect_count
    
 

with open('../data/count_by_aspect_by_category_one-hundred-thousand.json', 'w') as outfile:
    json.dump(count_Category_Aspect, outfile)






### create barplot
categories = []

for cat in reviews:
    categories.append(cat)


for cat in sentiment_Category_Aspect:
    asp_dict = sentiment_Category_Aspect[cat]
    
    aspectList = []
    y = []
    
    for aspect in asp_dict:
        aspectList.append(aspect)
        y.append(asp_dict[aspect])
                

with open('../data/sentiment_by_aspect_by_category_one-hundred-thousand.json', 'w') as outfile:
    json.dump(sentiment_Category_Aspect, outfile)




### create barplot
categories = []

for cat in reviews:
    categories.append(cat)


for cat in count_Category_Aspect:
    asp_dict = count_Category_Aspect[cat]
    
    aspectList = []
    y = []
    
    for aspect in asp_dict:
        aspectList.append(aspect)
        y.append(asp_dict[aspect])
                


#with open('charts/count_by_aspect_by_category_one-hundred-thousand.txt', 'w') as outfile:
#    json.dump(count_Category_Aspect, outfile)



























