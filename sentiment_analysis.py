###### import libraries #####

import nltk, re, json, time, string, pandas as pd

from nltk import text
from nltk.tokenize import word_tokenize
from nltk.text import TextCollection
from nltk.probability import FreqDist
from nltk.util import ngrams

from watson_developer_cloud import AlchemyLanguageV1
import indicoio


###### import and set up data #######
""" Set API defaults """
alchemy_language = AlchemyLanguageV1(api_key='xxx')
indicoio.config.api_key = 'xxx'


""" Retrieve the data set """
train = pd.read_csv("NYC_comments_train.csv", header=0)
reviewsx = list(train.Review) #send dataframe column to list
classification = list(train.Classification)

"""get the files for positive and negative words, convert to lists"""
csv_read = pd.read_csv("negative-words.csv", header=0)
negative_words = list(csv_read.Negative)
csv_read = pd.read_csv("positive-words.csv", header=0)
positive_words = list(csv_read.Positive)
csv_read = pd.read_csv("stopwords.csv", header=0)
stop = list(csv_read.stopwords)

negation = ['no','not','never','n\'t','cannot']
intensify = ['very','really','extremely','absolutely','highly']

""" Create a corpus of text """
reviews=[]
for z in reviewsx:
    n=''.join(x for x in z if x in string.printable)
    o=' '.join(n.split())
    reviews.append(o)

reviewcollection = TextCollection(word_tokenize(r) for r in reviews) #package a list of tokenized reviews
reviewset = [word_tokenize(r) for r in reviews]

""" add the pos/neg lists to a coded dictionary """
subj_dict = {}
for w in negative_words:
    subj_dict[w] = 'NEG'

for w in positive_words:
    subj_dict[w] = 'POS'

rating_dict = {}
rating_dict['NEG']= -1
rating_dict['IRR']= 0
rating_dict['POS']= 1
rating_dict['negate']= 2
rating_dict['intense']= 2

######## Define functions ##########
""" pre-clean the review set """
def pre_clean(wordl):
    lst2 = []
        
    splitted = re.split(r"\.\s*", wordl)
    for s in splitted:
        if s != '':
            l=s.lower().replace('n\'t','not')
            lst2.append(l)
    return lst2


""" for each tokenized word, clean the word (no punctuation) and see if it appears in the dictionary,
then assign the code to it """
def clean_token(word1):
    w=word1
    #make lowercase, replace periods (i.e. Mr., Dr.), and replace the n't contractions
    if w not in stop and w.isalnum() and subj_dict.get(w) is not None:
        tag_id = subj_dict[w]
        tag = rating_dict[tag_id]
    elif w.isalnum() or w.isdigit():
        tag_id = 'IRR'
        tag = rating_dict[tag_id]
    else:
        w, tag_id, tag = None, None, None 
    return w, tag_id, tag

""" for each tokenized word, determine if a negation or intensifier word precedes within 2 words,
then assign a code"""
def modify_token(lst):
    list1 = [v.lower() for v in lst]
    list2 = [n for n in negation if n in list1]
    list3 = [n for n in intensify if n in list1]
    list4 = [n for n in list1 if n=='would']
    tagg_id = 'negate'
    taggg_id = 'intense'
    tagggg_id = 'recs'
    if len(list2)==1: tagg = 2
    elif len(list2)!=1: tagg = 0
    if len(list3)>0: taggg = 1
    elif len(list3)==0: taggg = 0
    if len(list4)>0: tagggg = 0
    elif len(list4)==0: tagggg = 1
    return tagg_id,tagg,taggg_id,taggg,tagggg_id,tagggg


""" retrieve the AlchemyAPI sentiment rating """
def retrieve_alchemy(tok):
    jsonreturn = json.dumps(alchemy_language.sentiment(text=tok), indent=2)
    jsnr = json.loads(jsonreturn).get('docSentiment')
    sentiment = jsnr['type']
    return sentiment

""" retrieve the Indico sentiment rating """
def retrieve_indico(tokz):
    indi = indicoio.sentiment_hq(tokz)
    if indi>0.5:
        isent = 'POS'
    elif indi<0.5:
        isent = 'NEG'
    else: isent = 'NEU'
    return isent

######## Assigning sentiment ##########
reviewcleaned = []
for j in reviewset:
    lvl1 = []
    for i in j:
        lst3 = pre_clean(i)
        for k in lst3:
            lvl1.append(k)
    reviewcleaned.append(lvl1)
        
APIsent = []
Indisent = []

for d in reviews:
    try:
        sent_ret = retrieve_alchemy(d)
        APIsent.append(sent_ret)
    except:
        sent_ret='error'
        APIsent.appent(sent_ret)
    try:
        time.sleep(0.2)        
        sent_ret2 = retrieve_indico(d)
        Indisent.append(sent_ret2)
    except:
        sent_ret2='error'
        Indisent.append(sent_ret2)


""" for each tokenized review, clean, then designate a code """
cleaned = []
trigrams = []

for j in reviewcleaned:
    trigrams.append(ngrams(j,3))
    counter=0
    lvl2 = []
    for i in j:
        wd, tag1_id, tag1 = clean_token(i)
        if 0<counter<2 and wd is not None:
            list3 = j[:counter]
            tag2_id,tag2,tag3_id,tag3,tag4_id,tag4 = modify_token(list3)
            tagged = [wd,tag1_id,tag1,tag2_id,tag2,tag3_id,tag3,tag4_id,tag4]
            lvl2.append(tagged)
        elif counter>1 and wd is not None:
            starti = counter-2
            list3 = j[starti:counter]
            tag2_id,tag2,tag3_id,tag3,tag4_id,tag4 = modify_token(list3)
            tagged = [wd,tag1_id,tag1,tag2_id,tag2,tag3_id,tag3,tag4_id,tag4]
            lvl2.append(tagged)
        counter = counter+1
    cleaned.append(lvl2)

""" for each cleaned and coded review, tally, then assign a rating of pos/neg/neu """
score=[]
tallied = []
ftally = []

for z in cleaned:
    tally = 0
    for (a,b,c,d,e,f,g,h,i) in z:
        if i == 1:
            if e ==2:
                if b=='NEG':
                    tally = tally+c+e
                elif b=='POS':
                    tally = tally+c-i
            elif e==0:
                if b=='NEG':
                    tally = tally+c-g
                elif b=='POS':
                    tally = tally+c-i
        if i ==0:
            if e ==2:
                if b=='NEG':
                    tally = tally+c+e
                elif b=='POS':
                    tally = tally+c-e
            elif e==0:
                if b=='NEG':
                    tally = tally+c-g
                elif b=='POS':
                    tally = tally+c+g
        else: tally = tally+c
    if tally>0:
        final ='POS'
        tallied.append(tally/len(z))
    elif tally<0:
        final ='NEG'
        tallied.append(tally/len(z))
    elif tally==0:
        final ='NEU'
        tallied.append(tally)
    score.append(final)
    ftally.append(tally)

""" add column to dataframe based on list """
train['New_Rating']=score
train['Tally']=ftally
train['Pct']=tallied
train['Sentiment1']=APIsent
train['Sentiment2']= Indisent


train.to_csv('revised_NYC_comments_train.csv')


""" text collection exploration """
"""
reviewcollection.concordance("very") #word concordance for every review
fdist1 = FreqDist(reviewcollection) #frequency distribution of text, indexed
fdist1.most_common(10) #most frequent 10 words
wdpairs = list(bigrams(reviewcollection)) #all pairs of words that occur together in the text
reviewcollection.collocations() #returns most frequent pairs
reviewcollection.findall(r"<very> <.*>") #find phrases in text with a specific pattern
"""
