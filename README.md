# Python_sample_data_analysis

My submission for my Data Science II graduate course final project, to help show my abilities to conduct data analysis within Python. Note that some 
pieces of code were drawn from group work in a prior course, and that the data set is omitted due to size.

## Relevant prior wor
This project will be picking up where my group project from Data Science I last semester left off. I will really only be building off of those files which 
were included in the data cleaning and sentiment analysis process, meaning that
the vast majority of the files created during the course of that project will not be referenced for this particular project. I also want to note that the
data set is not included 
within the zip file due to its size (roughly 83 million reviews).

Any filename beginning with "287" indicates that this was drawn from the group project in a prior semester (the course being STAT 287). Further information on some of these files is given below. Any filename which does not have this prefix was written by myself for the individual project.

### report_REDVIPER.pdf
This file is our final written report for the group project from a prior semester, and is referenced in the literature review (reference 4). This paper provides useful background on 
the data set itself, including how the subset was achieved and how the sentiment analysis was conducted. As such, it will be a useful reference for this 
project for the introduction and/or methods section when I am introducing and describing the data.

The following files from the group project were also referenced for this project, and were ones that I wrote during the group project:

### sentiment_analysis_v2.py

This file conducts the initial sentiment analysis on the data, creates some EDA plots for average compound sentiment, and saves that data to a file. This 
saved data is then used in subsequent Python scripts, including sentiment_over_time_graphs_v1.py.

### sentiment_over_time_graphs_v1.py

This files uses the CSV files created above to plot the compound sentiment across all products, as well as separately for each product category. 
This basic framework for looping through to create the graphs was the starting point for this project’s EDA, and was modified to create more meaningful 
visualizations for the scope of this project.
