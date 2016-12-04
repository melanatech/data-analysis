README:

**Needs update**

These files are meant to demonstrate my journey of analyzing unstructured text data. I use Python 3.5 to scrape a website of doctor reviews, clean the reviews systematically, retrieve a sentiment rating using external APIs, and create my own algorithm for assigning sentiment.

There are 4 input files:
*negative-words.csv - a list of negative words
*positive-words.csv - a list of positive words
*stopwords.csv - a list of irrelevant words
*NYC_comments_train - a pre-coded set of reviews with sentiment

There are 4 python scripts:
*ratemds_scrape.py - my first foray into scraping a single web page
*ratemds.scrap2.py - an iterative approach to scraping hundreds of web pages on a site in order to build a dataset
*sentiment_analysis.py - taking a set of coded reviews and assigning sentiment codes to each
*crosstab.py - comparing different modes of sentiment analysis with the original codes
