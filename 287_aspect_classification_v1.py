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

service = ['rude', 'supervisor','seller','company','packag','polic','warrant', 'respon', 'representative','receipt']


# dictionary which uses name of aspect to point to the list of classification words
aspects = {'price':price, 'durability':durability, 'aesthetics':aes, 'performance': performance, 'ease of use': ease, 'service': service}

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
    




### create barplot from above data
aspectList = []
y = []

for aspect in sentiment_Aspect:
    aspectList.append(aspect)
    y.append(sentiment_Aspect[aspect])
            
x = np.arange(len(aspectList))
width = 0.4
fig, ax = plt.subplots()


rects1 = ax.bar(x - width/2, y, width, label='Compound')

ax.set_ylabel('Compound Sentiment')
ax.set_ylim([0,0.8])
ax.set_title('Average Compound Sentiment by Product Aspect')
ax.set_xticks(x)
ax.set_xticklabels(aspectList)
 
plt.xticks(rotation = 45)
  
fig.tight_layout()
  
plt.show()




### create barplot from above data
aspectList = []
y = []

for aspect in count_Aspect:
    aspectList.append(aspect)
    y.append(count_Aspect[aspect])
            
x = np.arange(len(aspectList))
width = 0.4
fig, ax = plt.subplots()


rects1 = ax.bar(x - width/2, y, width, label='Count')

ax.set_ylabel('Count')
ax.set_ylim([0, max(y) + max(y)*0.1])
ax.set_title('Number of Reviews by Product Aspect (all categories)')
ax.set_xticks(x)
ax.set_xticklabels(aspectList)

ax.bar_label(rects1, padding=3)
 
plt.xticks(rotation = 45)
  
fig.tight_layout()
  
plt.show()




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
                
    x = np.arange(len(aspectList))
    width = 0.4
    fig, ax = plt.subplots()
    
    
    rects1 = ax.bar(x - width/2, y, width, label='Compound')
    
    ax.set_ylabel('Compound Sentiment')
    ax.set_ylim([-1.1,1.1])
    
    title = 'Average Compound Sentiment by Product Aspect for ' + cat
    
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(aspectList)
    ax.axhline(0, color='black')
     
    plt.xticks(rotation = 45)
      
    fig.tight_layout()
      
    plt.show()




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
                
    x = np.arange(len(aspectList))
    width = 0.4
    fig, ax = plt.subplots()
    
    
    rects1 = ax.bar(x - width/2, y, width, label='Count')
    
    ax.set_ylabel('Count')
    ax.set_ylim([0,max(y) + max(y)*0.1])     # adds 10% buffer
    
    title = 'Count by Product Aspect for ' + cat
    
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(aspectList)
     
    plt.xticks(rotation = 45)
    
    ax.bar_label(rects1, padding=3)
      
    fig.tight_layout()
      
    plt.show()



























