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
    
    
    
    
    
#### Begin Decomposition #######################################

# https://towardsdatascience.com/time-series-decomposition-in-python-8acac385a5b2




#### Number of reviews


# Note that many product categories have an upward trend in volume of reviews due to
# the overall upward trend in volume of reviews; so, this is not super interesting 
# and should be should be removed in order to analyze seasonality

# set limits
minMonth = datetime.datetime.strptime('2008-01', "%Y-%m")
maxMonth = datetime.datetime.strptime('2014-01', "%Y-%m")


if not debug:
    
    
    
    
    for cat in cat_Month_Count:
        x = []
        y = []
        
        for month in monthsSorted2:
            if month < minMonth or month > maxMonth:
                pass
            else:
                month = datetime.datetime.strftime(month, "%Y %m")
                try:
                    y.append(cat_Month_Count[cat][month])
                    x.append(month)
                    
                except KeyError:
                    pass
    
            
        d = {"Months": x, "Number of Reviews" : y}
        df = pd.DataFrame(d)
        
        
        try:
            result = sm.seasonal_decompose(df["Number of Reviews"], model='additive', period=12)
            
            fig, (ax1,ax2,ax3) = plt.subplots(3,1, figsize=(15,8))
            result.trend.plot(ax=ax1,ylabel = "trend")
            #result.seasonal.plot(ax=ax2,ylabel = "seasonality")
            #result.resid.plot(ax=ax3,ylabel = "residual")
            plt.title("Number of reviews " + cat)
        
        
            plt.xlabel("Time")

            
            plt.xticks(rotation = 45)
            
            mLabels = []
            for i in range(len(x)): 
                if i%12 == 0:
                    mLabels.append("Jan " + x[i][0:4])
                else:
                    mLabels.append("")
            
            #fig, ax = plt.subplots()
            
            x2 = np.arange(len(x))
            distance_between_ticks = 12
            reduced_xticks = x2[np.arange(0, len(x2), distance_between_ticks)]
            
            ax1.set_xticks(x2)
            
            #ax.set_title(title)
            ax1.set_ylabel("Number of Reviews")
            
            ax1.set_xticklabels(mLabels)
            plt.xlabel("Time")
            
            plt.xticks(rotation = 45)
        
        
            plt.show()
            
            p = result.seasonal
        
            
            # width = 0.5
            # figbar, axbar = plt.subplots()
            # m = []
            # y.clear()
            
            # for month in monthsSorted2:
            #     if month < minMonth or month > maxMonth:
            #         pass
            #     else:
            #         month = datetime.datetime.strftime(month, "%Y %m")
            #         try:
            #             monthCount[month]
            #             m.append(month)
            #             y.append(monthCount[month])
            #         except KeyError:
            #             pass
            
            
            plt.xlabel("Time")
            #plt.ylabel("Compound sentiment")
            title = "Number of Reviews over time for " + cat
            #plt.title(title)
            
            plt.xticks(rotation = 45)
            
            mLabels = []
            for i in range(len(x)): 
                if i%12 == 0:
                    mLabels.append("Jan " + x[i][0:4])
                else:
                    mLabels.append("")
            
            fig, ax = plt.subplots()
            
            x2 = np.arange(len(x))
            distance_between_ticks = 12
            reduced_xticks = x2[np.arange(0, len(x2), distance_between_ticks)]
            
            ax.set_xticks(x2)
            
            ax.set_title(title)
            ax.set_ylabel("Number of Reviews")
            
            ax.set_xticklabels(mLabels)
            plt.xlabel("Time")
            
            plt.xticks(rotation = 45)
            
            plt.plot(x, p)
            #fig.tight_layout()
            
            # newYears = [datetime.datetime.strftime('2008-01', "%Y-%m"), datetime.datetime.strftime('2009-01', "%Y-%m"),
            #             datetime.datetime.strftime('2010-01', "%Y-%m"), datetime.datetime.strftime('2011-01', "%Y-%m"),
            #             datetime.datetime.strftime('2012-01', "%Y-%m"), datetime.datetime.strftime('2013-01', "%Y-%m"),
            #             datetime.datetime.strftime('2014-01', "%Y-%m")]
            
            newYears = ['2008 01', '2009 01', '2010 01', '2011 01', '2012 01', '2013 01', '2014 01']
            
            for year in newYears:
                for date in x:
                    if year == date:
                        plt.axvline(x = date, color = 'red', linestyle = 'dashed')
                        
                    
    
            plt.show()
        
        except ValueError:
            print(cat + " plot skipped, too few cycles", sep = '')
    
    
    
    
    
    for cat in cat_Month_Count:
        x = []
        y = []
        
        for month in monthsSorted2:
            if month < minMonth or month > maxMonth:
                pass
            else:
                month = datetime.datetime.strftime(month, "%Y %m")
                try:
                    y.append(float(cat_Month_Count[cat][month]))
                    x.append(month)
                    
                except KeyError:
                    pass
                
        #y = np.array(y)
        try:
            plt.acorr(y, maxlags = 12)
            title = "Autocorrelation for Number of Reviews for " + cat
            plt.title(title)
            plt.xlabel("Lags")
            plt.show()
            
            
            fig, ax = plt.subplots()
            title = "Autocorrelation for Number of Reviews for " + cat + " (Plot 2)"
            ax.set_title(title)
            plt.xlabel("Lags")
            y = np.array(y)
            plot_acf(y, bartlett_confint = False, ax = ax, title = title)
    
            plt.show()
            
        except ValueError:
            print(cat + " plot skipped, too few cycles", sep = '')
    
    
    
    
    
    
    
    # remove trend for Amazon_Instant_Video, Beauty, Office_Products, Cell_Phones and plot again
    
    
    # remove trend from above categories and try again
    
    needsDetrending = ["Amazon_Instant_Video", "Beauty", "Office_Products", 
                       "Cell_Phones_and_Accessories", "Health_and_Personal_Care",
                       "Grocery_and_Gourmet_Food", "Clothing_Shoes_and_Jewelry",
                       "Tools_and_Home_Improvement","Sports_and_Outdoors", 
                       "Toys_and_Games","Books","Baby","Electronics","Video_Games"]
    
    for cat in needsDetrending:
        
        x = []
        y = []
        
        for month in monthsSorted2:
            if month < minMonth or month > maxMonth:
                pass
            else:
                month = datetime.datetime.strftime(month, "%Y %m")
                try:
                    y.append(float(cat_Month_Count[cat][month]))
                    x.append(month)
                    
                except KeyError:
                    pass
        
        ###############
        
        fig_trend, ax_trend = plt.subplots()
        
        data = pd.DataFrame({"time" : x, "original" : y})
        
        data["detrended"] = data["original"].diff()
        ax_trend = data.plot()
        ax_trend.legend(ncol=5, 
                  loc='lower center',
                  #bbox_to_anchor=(0.5, 1.0),
                  bbox_transform=plt.gcf().transFigure)
        
        title = "Number of Reviews over Time for " + cat
        ax_trend.set_title(title)
        mLabels = []
        for i in range(len(x)): 
            if i%12 == 0:
                mLabels.append("Jan " + x[i][0:4])
            else:
                mLabels.append("")
                
        x2 = np.arange(len(x))
        distance_between_ticks = 12
        reduced_xticks = x2[np.arange(0, len(x2), distance_between_ticks)]
        
        ax_trend.set_xticks(x2)
        
        ax_trend.set_title(title)
        ax_trend.set_ylabel("Number of Reviews")
        
        ax_trend.set_xticklabels(mLabels)
        plt.xlabel("Time")
        
        plt.xticks(rotation = 45)
        plt.title(title)
        plt.show()
        
        ###################
        
        data["detrended"].iloc[0] = 0
        plt.acorr(data["detrended"], maxlags = 12)
        title = "Autocorrelation for Number of Reviews for " + cat + "\n(detrended)"
        plt.title(title)
        plt.xlabel("Lags")
        plt.show()
        
        #####
        
        fig, ax = plt.subplots()
        title = "Autocorrelation for Number of Reviews for " + cat + " (Plot 2)" + "\n(detrended)"
        ax.set_title(title)
        plt.xlabel("Lags")
        plot_acf(data["detrended"], bartlett_confint = False, ax = ax, title = title)
    
        plt.show()
    
    





#### Compound sentiment

# Now, the existence (or not) of trends is actually interesting/should be considered

for cat in sentiment_Cat_Time:
    x = []
    y = []
    
    for month in monthsSorted2:
        if month < minMonth or month > maxMonth:
            pass
        else:
            month = datetime.datetime.strftime(month, "%Y %m")
            try:
                y.append(sentiment_Cat_Time[cat][month]['compound'])
                x.append(month)
                
            except KeyError:
                pass

        
    d = {"Months": x, "Compound Sentiment" : y}
    df = pd.DataFrame(d)
    
    
    try:
        result = sm.seasonal_decompose(df["Compound Sentiment"], model='additive', period=12)
        
        fig, ax1 = plt.subplots()
        result.trend.plot(ax=ax1,ylabel = "trend")

        plt.title("Compound Sentiment Trend for " + cat)
        
        
        plt.xlabel("Time")
        #plt.ylabel("Compound sentiment")
        #title = "Compound sentiment over time for " + cat
        #plt.title(title)
        
        plt.xticks(rotation = 45)
        
        mLabels = []
        for i in range(len(x)): 
            if i%12 == 0:
                mLabels.append("Jan " + x[i][0:4])
            else:
                mLabels.append("")
        
        #fig, ax = plt.subplots()
        
        x2 = np.arange(len(x))
        distance_between_ticks = 12
        reduced_xticks = x2[np.arange(0, len(x2), distance_between_ticks)]
        
        ax1.set_xticks(x2)
        
        #ax.set_title(title)
        ax1.set_ylabel("Compound sentiment")
        
        ax1.set_xticklabels(mLabels)
        plt.xlabel("Time")
        
        plt.xticks(rotation = 45)
    
        
        plt.show()
        
        
        
        
        p = result.seasonal
    
        
        # width = 0.5
        # figbar, axbar = plt.subplots()
        # m = []
        # y.clear()
        
        # for month in monthsSorted2:
        #     if month < minMonth or month > maxMonth:
        #         pass
        #     else:
        #         month = datetime.datetime.strftime(month, "%Y %m")
        #         try:
        #             monthCount[month]
        #             m.append(month)
        #             y.append(monthCount[month])
        #         except KeyError:
        #             pass
        
        
        plt.xlabel("Time")
        #plt.ylabel("Compound sentiment")
        title = "Compound sentiment over time for " + cat
        #plt.title(title)
        
        plt.xticks(rotation = 45)
        
        mLabels = []
        for i in range(len(x)): 
            if i%12 == 0:
                mLabels.append("Jan " + x[i][0:4])
            else:
                mLabels.append("")
        
        fig, ax = plt.subplots()
        
        x2 = np.arange(len(x))
        distance_between_ticks = 12
        reduced_xticks = x2[np.arange(0, len(x2), distance_between_ticks)]
        
        ax.set_xticks(x2)
        
        ax.set_title(title)
        ax.set_ylabel("Compound sentiment")
        
        ax.set_xticklabels(mLabels)
        plt.xlabel("Time")
        
        plt.xticks(rotation = 45)
        
        plt.plot(x, p)
        #fig.tight_layout()
        
        # newYears = [datetime.datetime.strftime('2008-01', "%Y-%m"), datetime.datetime.strftime('2009-01', "%Y-%m"),
        #             datetime.datetime.strftime('2010-01', "%Y-%m"), datetime.datetime.strftime('2011-01', "%Y-%m"),
        #             datetime.datetime.strftime('2012-01', "%Y-%m"), datetime.datetime.strftime('2013-01', "%Y-%m"),
        #             datetime.datetime.strftime('2014-01', "%Y-%m")]
        
        newYears = ['2008 01', '2009 01', '2010 01', '2011 01', '2012 01', '2013 01', '2014 01']
        
        for year in newYears:
            for date in x:
                if year == date:
                    plt.axvline(x = date, color = 'red', linestyle = 'dashed')
                    
                

        plt.show()
    
    except ValueError:
        print(cat + " plot skipped, too few cycles", sep = '')





for cat in sentiment_Cat_Time:
    x = []
    y = []
    
    for month in monthsSorted2:
        if month < minMonth or month > maxMonth:
            pass
        else:
            month = datetime.datetime.strftime(month, "%Y %m")
            try:
                y.append(float(sentiment_Cat_Time[cat][month]['compound']))
                x.append(month)
                
            except KeyError:
                pass
            
    #y = np.array(y)
    try:
        plt.acorr(y, maxlags = 12)
        title = "Autocorrelation for Compound Sentiment for " + cat
        plt.title(title)
        plt.xlabel("Lags")
        plt.show()
        
        
        fig, ax = plt.subplots()
        title = "Autocorrelation for Compound Sentiment for " + cat + " (Plot 2)"
        ax.set_title(title)
        plt.xlabel("Lags")
        y = np.array(y)
        plot_acf(y, bartlett_confint = False, ax = ax, title = title)

        plt.show()
        
    except ValueError:
        print(cat + " plot skipped, too few cycles", sep = '')


# Electronics, Sports, Tools, Health, Automotive have potential trends that should be analyzed
    
    
needsDetrending = ["Health_and_Personal_Care", "Tools_and_Home_Improvement",
                   "Electronics", "Sports_and_Outdoors", "Automotive", "Patio_Lawn_and_Garden"]

for cat in needsDetrending:
    
    x = []
    y = []
    
    for month in monthsSorted2:
        if month < minMonth or month > maxMonth:
            pass
        else:
            month = datetime.datetime.strftime(month, "%Y %m")
            try:
                y.append(float(sentiment_Cat_Time[cat][month]['compound']))
                x.append(month)
                
            except KeyError:
                pass
    
    ###############
    
    fig_trend, ax_trend = plt.subplots()
    
    data = pd.DataFrame({"time" : x, "original" : y})
    
    data["detrended"] = data["original"].diff()
    ax_trend = data.plot()
    ax_trend.legend(ncol=5, 
              loc='lower center',
              #bbox_to_anchor=(0.5, 1.0),
              bbox_transform=plt.gcf().transFigure)
    
    title = "Compound sentiment over Time for " + cat
    ax_trend.set_title(title)
    mLabels = []
    for i in range(len(x)): 
        if i%12 == 0:
            mLabels.append("Jan " + x[i][0:4])
        else:
            mLabels.append("")
            
    x2 = np.arange(len(x))
    distance_between_ticks = 12
    reduced_xticks = x2[np.arange(0, len(x2), distance_between_ticks)]
    
    ax_trend.set_xticks(x2)
    
    ax_trend.set_title(title)
    ax_trend.set_ylabel("Compound sentiment")
    
    ax_trend.set_xticklabels(mLabels)
    plt.xlabel("Time")
    
    plt.xticks(rotation = 45)
    plt.title(title)
    plt.show()
    
    ###################
    
    data["detrended"].iloc[0] = 0
    plt.acorr(data["detrended"], maxlags = 12)
    title = "Autocorrelation for compound sentiment for " + cat + "\n(detrended)"
    plt.title(title)
    plt.xlabel("Lags")
    plt.show()
    
    #####
    
    fig, ax = plt.subplots()
    title = "Autocorrelation for compound sentiment for " + cat + " (Plot 2)" + "\n(detrended)"
    ax.set_title(title)
    plt.xlabel("Lags")
    plot_acf(data["detrended"], bartlett_confint = False, ax = ax, title = title)

    plt.show()
    
    
    
    
    
#### Ranking Trends    #######################################################################
    

# calculate F statistics
Ftrends = {}
FtrendsList = []
Fseasons = {}
FseasonsList = []

for cat in cat_Month_Count:
        x = []
        y = []
        
        for month in monthsSorted2:
            if month < minMonth or month > maxMonth:
                pass
            else:
                month = datetime.datetime.strftime(month, "%Y %m")
                try:
                    y.append(cat_Month_Count[cat][month])
                    x.append(month)
                    
                except KeyError:
                    pass
    
            
        d = {"Months": x, "Number of Reviews" : y}
        df = pd.DataFrame(d)
        
        
        try:
            # trend:
            result = sm.seasonal_decompose(df["Number of Reviews"], model='additive', period=12)
            remainderSeries = result.resid
            trendSeries = result.trend
            # remove the nans
            remainder = []
            trend = []
            for num in remainderSeries:
                if math.isnan(num):
                    pass
                else:
                    remainder.append(num)
                    
            for num in trendSeries:
                if math.isnan(num):
                    pass
                else:
                    trend.append(num)
                    
            # var(T + R) = var(T) + var(R) + 2 * cov(R,T)
            covariance = np.cov(trend,remainder)[0,1]
            value = var(remainder) / (var(trend) + var(remainder) + 2 * covariance)
            Ftrend = max(0, 1 - value)
            FtrendsList.append(Ftrend)
            Ftrends[Ftrend] = cat
            
        except ValueError:
            print(cat + " plot skipped, too few cycles", sep = '')
            
            
        try:
            # seasonality:
            seasonSeries = result.seasonal
            # remove the nans
            season = []
            # remove first and last six of seasonality to match remainder
            for num in seasonSeries:
                season.append(num)
                
            season = season[6:-6]

            # var(T + R) = var(T) + var(R) + 2 * cov(R,T)
            covariance = np.cov(season,remainder)[0,1]
            value = var(remainder) / (var(season) + var(remainder) + 2 * covariance)
            Fseason = max(0, 1 - value)
            FseasonsList.append(Fseason)
            Fseasons[Fseason] = cat
            
        except ValueError:
            print(cat + " plot skipped, too few cycles", sep = '')
    
    
    
    
# sort above figures to get results
print()
print("Strongest trends:")
FtrendsList.sort(reverse=True)
for i in range(10):
    Fval = FtrendsList[i]
    FvalString = str(Fval)
    print(FvalString + "    " + Ftrends[Fval])

print()
print("Weakest trends:")
FtrendsList.sort()
for i in range(10):
    Fval = FtrendsList[i]
    FvalString = str(Fval)
    print(FvalString + "    " + Ftrends[Fval])
    
    
    
print()
print("Strongest seasonalities:")
FseasonsList.sort(reverse=True)
for i in range(11):
    Fval = FseasonsList[i]
    FvalString = str(Fval)
    print(FvalString + "    " + Fseasons[Fval])
    
print()
print("Weakest seasonalities:")
FseasonsList.sort()
for i in range(10):
    Fval = FseasonsList[i]
    FvalString = str(Fval)
    print(FvalString + "    " + Fseasons[Fval])
    
    
    
    
    
    
    
    
    
    
    
    
    