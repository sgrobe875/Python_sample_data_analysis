# Reworking the data set to obtain better sample sizes for further analysis


import json
import matplotlib.pyplot as plt
import numpy as np
import datetime
import gzip



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



sentiment_Category = gz_json_loader(filename = "../data/sentiment_category_one-hundred-thousand.json")
sentiment_Month = gz_json_loader(filename = "../data/sentiment_month_one-hundred-thousand.json")
sentiment_Cat_Time = gz_json_loader(filename = "../data/sentiment_cat_time_one-hundred-thousand.json")

reviews = gz_json_loader(filename = "../data/sorted_data_one-hundred-thousand.json")


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
    
    
    
    
# group into similar categories to reduce total number of categories/increase 
# number of observations per category

# new categories: Music, Recreation, Home_and_Garden, Electronics, Media, Clothing_and_Accessories, Miscellaneous

newCat = {"Cell_Phones_and_Accessories" : "Electronics",
            "Pet_Supplies" : "Home_and_Garden",
            "Kindle_Store" : "Media",
            "Apps_for_Android" : "Media",
            "Automotive" : "Miscellaneous",
            "Home_and_Kitchen" : "Home_and_Garden",
            "Baby" : "Home_and_Garden",
            "Grocery_and_Gourmet_Food" : "Home_and_Garden",
            "Clothing_Shoes_and_Jewelry" : "Clothing_and_Accessories",
            "Books" : "Media", # maybe recreation?
            "Toys_and_Games" : "Recreation",
            "Musical_Instruments" : "Recreation", 
            "Movies_and_TV" : "Media", 
            "Electronics" : "Electronics", 
            "Tools_and_Home_Improvement" : "Home_and_Garden",
            "Patio_Lawn_and_Garden" : "Home_and_Garden",
            "Digital_Music" : "Music",
            "Video_Games" : "Electronics",
            "Beauty" : "Clothing_and_Accessories", 
            "Office_Products" : "Miscellaneous",
            "Health_and_Personal_Care" : "Miscellaneous",
            "Sports_and_Outdoors" : "Recreation", 
            "CDs_and_Vinyl" : "Music",
            "Amazon_Instant_Video" : "Media" }


# assign reviews to new categories
reviews_New_Cats = {"Music" : {},
                    "Recreation" : {},
                    "Home_and_Garden" : {},
                    "Electronics" : {},
                    "Media" : {},
                    "Clothing_and_Accessories" : {},
                    "Miscellaneous" : {} }



### Reassign categories for reviews ####################################################


# loop through all categories in reviews
for cat in reviews:
    # find the corresponding new category name
    newCatName = newCat[cat]
        
    # loop through each month of reviews for that category
    for month in reviews[cat]:
        # if month is not present, initialize it with an empty list; then append review
        try: 
            reviews_New_Cats[newCatName][month]
        except KeyError:
            reviews_New_Cats[newCatName][month] = []
        for rev in reviews[cat][month]:
            reviews_New_Cats[newCatName][month].append(rev)
    
    
    
# Sanity check: get counts to evaluate sample sizes, compare to original data structure
new_Cats_Counts = {"Music" : 0,
                    "Recreation" : 0,
                    "Home_and_Garden" : 0,
                    "Electronics" : 0,
                    "Media" : 0,
                    "Clothing_and_Accessories" : 0,
                    "Miscellaneous" : 0 }


for cat in reviews_New_Cats:
    for month in reviews_New_Cats[cat]:
        new_Cats_Counts[cat] = new_Cats_Counts[cat] + len(reviews_New_Cats[cat][month])

            
            

totalCount = 0
for cat in reviews_New_Cats:
    print("%30s: %5d" % (cat, new_Cats_Counts[cat]))
    totalCount += new_Cats_Counts[cat]

print("---------------------------------------")
print("%30s: %5d" % ("Total Reviews", totalCount))
    
print("\n\n")
    

    
    
    
old_Cats_Counts = {"Cell_Phones_and_Accessories" : 0,
            "Pet_Supplies" : 0,
            "Kindle_Store" : 0,
            "Apps_for_Android" : 0,
            "Automotive" : 0,
            "Home_and_Kitchen" : 0,
            "Baby" : 0,
            "Grocery_and_Gourmet_Food" : 0,
            "Clothing_Shoes_and_Jewelry" : 0,
            "Books" : 0, 
            "Toys_and_Games" : 0,
            "Musical_Instruments" : 0, 
            "Movies_and_TV" : 0, 
            "Electronics" : 0, 
            "Tools_and_Home_Improvement" : 0,
            "Patio_Lawn_and_Garden" : 0,
            "Digital_Music" : 0,
            "Video_Games" : 0,
            "Beauty" : 0, 
            "Office_Products" : 0,
            "Health_and_Personal_Care" : 0,
            "Sports_and_Outdoors" : 0, 
            "CDs_and_Vinyl" : 0,
            "Amazon_Instant_Video" : 0 }
    
    
    
    
    
for cat in reviews:
    for month in reviews[cat]:
        for rev in reviews[cat][month]:
            old_Cats_Counts[cat] = old_Cats_Counts[cat] + 1
        
        
        #old_Cats_Counts[cat] = old_Cats_Counts[cat] + len(reviews[cat][month])

            
            

totalCount = 0
for cat in reviews:
    print("%30s: %5d" % (cat, old_Cats_Counts[cat]))
    totalCount += old_Cats_Counts[cat]

print("---------------------------------------")
print("%30s: %5d" % ("Total Reviews", totalCount))
    
print("\n\n")
    
    
    
    
    
### Reassign categories for sentiment_Category ####################################################


sent_New_Cats = {"Music" : [],
                    "Recreation" : [],
                    "Home_and_Garden" : [],
                    "Electronics" : [],
                    "Media" : [],
                    "Clothing_and_Accessories" : [],
                    "Miscellaneous" : [] }


# loop through all categories in sentiment_Category
for cat in sentiment_Category:
    # find the corresponding new category name
    newCatName = newCat[cat]
    sent_New_Cats[newCatName].append(sentiment_Category[cat])

        
        
for cat in sent_New_Cats:
    avg = sum(sent_New_Cats[cat]) / len(sent_New_Cats[cat])
    sent_New_Cats[cat] = avg
    
    
# Sanity check: print out results, ensure that they look correct
for cat in sent_New_Cats:
    print("%30s: %.5f" % (cat, sent_New_Cats[cat]))

    
print("\n\n")
    




# Reassignment not necessary for sentiment_Month since category not included in this data structure!


### Reassign categories for sentiment_Cat_Time ####################################################


# this process is very similar to reassignment of reviews above:
    
    
sent_NewCats_Time = {"Music" : {},
                    "Recreation" : {},
                    "Home_and_Garden" : {},
                    "Electronics" : {},
                    "Media" : {},
                    "Clothing_and_Accessories" : {},
                    "Miscellaneous" : {} }
    


# loop through all categories in reviews
for cat in sentiment_Cat_Time:
    # find the corresponding new category name
    newCatName = newCat[cat]
        
    # loop through each month of reviews for that category
    for month in sentiment_Cat_Time[cat]:
        # if month is not present, initialize it with an empty list; then append review
        try: 
            sent_NewCats_Time[newCatName][month]
        except KeyError:
            sent_NewCats_Time[newCatName][month] = []
        sent_NewCats_Time[newCatName][month].append(sentiment_Cat_Time[cat][month]['compound'])
        
        
        
for cat in sent_NewCats_Time:
    for month in sent_NewCats_Time[cat]:
        avg = sum(sent_NewCats_Time[cat][month]) / len(sent_NewCats_Time[cat][month])
        sent_NewCats_Time[cat][month] = avg
        
    
    
# Sanity check: get counts to evaluate sample sizes, compare to original data structure
new_Cats_Counts = {"Music" : 0,
                    "Recreation" : 0,
                    "Home_and_Garden" : 0,
                    "Electronics" : 0,
                    "Media" : 0,
                    "Clothing_and_Accessories" : 0,
                    "Miscellaneous" : 0 }


for cat in sent_NewCats_Time:
    for month in sent_NewCats_Time[cat]:
        new_Cats_Counts[cat] += 1

            
            
# Sanity check 
totalCount = 0
for cat in sent_NewCats_Time:
    print("%30s: %5d" % (cat, new_Cats_Counts[cat]))
    totalCount += new_Cats_Counts[cat]

print("---------------------------------------")
print("%30s: %5d" % ("Total Months", totalCount))
    
print("\n\n")
    






### Final step: Write all these data structures to JSONs to be used in other files

# name files with the same name as the data structure


# reviews_New_Cats
with open('../data/reviews_New_Cats.json', 'w') as fout:
    fout.write(json.dumps(reviews_New_Cats)) 
fout.close()



# sent_New_Cats
with open('../data/sent_New_Cats.json', 'w') as fout:
    fout.write(json.dumps(sent_New_Cats)) 
fout.close()



# sent_NewCats_Time
with open('../data/sent_NewCats_Time.json', 'w') as fout:
    fout.write(json.dumps(sent_NewCats_Time)) 
fout.close()







    
    
    
    
    
    