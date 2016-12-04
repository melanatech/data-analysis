import time, itertools, pandas as pd



""" Import data and create a corpus of text """
today = time.strftime("%Y%m%d")
filename = "performance"+today+".txt"

train = pd.read_csv("revised_NYC_comments_trainx.csv", header=0, encoding = 'ISO-8859-1')


""" Define functions to create report """
def printout(z,y,x,w,v,u,t,s,r,q):
    line1 = '\n*****************************'+'\nModel1 -'+q+'\n*****************************'+'\n'
    line3 = 'Positive precision: '+"%.2f" % z+'; Positive recall: '+"%.2f" % y+'; Likelihood Ratio: '+"%.2f" % x+'; Informedness: '+"%.2f" % s+'\nNegative precision: '+"%.2f" % w+'; Negative recall: '+"%.2f" % v+'; Likelihood Ratio: '+"%.2f" % u+'; Informedness: '+"%.2f" % r+'\nOverall POS/NEG Accuracy: '+"%.2f" % t+'\n'
    return line1, line3

def model_performance(model,l,m,n):
    a,b,c,d,e='POS','NEG',l,m,n
    TP_pos = len(train[(train['Classification']==a) & (train[model]==c)])
    pos_P = TP_pos/len(train[(train[model]==c)])
    pos_R = TP_pos/len(train[(train['Classification']==a)])
    pos_FPR = len(train[(train[model]==c) & (train['Classification']!=a)])/len(train[(train['Classification']!=a)])
    pos_SPC = len(train[(train[model]!=c) & (train['Classification']!=a)])/len(train[(train['Classification']!=a)])
    pos_PLR = pos_R/pos_FPR
    pos_J = (pos_R+pos_SPC)-1
    TP_neg = len(train[(train['Classification']==b) & (train[model]==d)])
    neg_P = TP_neg/len(train[(train[model]==d)])
    neg_R = TP_neg/len(train[(train['Classification']==b)])
    neg_FPR = len(train[(train[model]==d) & (train['Classification']!=b)])/len(train[(train['Classification']!=b)])
    neg_SPC = len(train[(train[model]!=d) & (train['Classification']!=b)])/len(train[(train['Classification']!=b)])
    neg_PLR = neg_R/neg_FPR
    neg_J = (neg_R+neg_SPC)-1
    accuracy = (TP_pos+TP_neg)/len(train[(train['Classification']!='NEU')])
    #call the printout function to set up output file
    printed1, printed3 = printout(pos_P,pos_R,pos_PLR,neg_P,neg_R,neg_PLR,accuracy,pos_J,neg_J,e)
    return printed1, printed3

def create_output(h,i):
    outfile = open(filename,'a')
    outfile.write(h)
    outfile.write(i)
    outfile.close()

""" Create and print report """
pd.set_option('expand_frame_repr', False)

mod,c1,d1,e1 = train.columns.values[4],'POS','NEG','Self-coded'
printline1, printline2 = model_performance(mod,c1,d1,e1)
print(printline1)
print(pd.crosstab(train.Classification, train.New_Rating, margins=True),'\n')
print(printline2)
create_output(printline1, printline2)

mod,c1,d1,e1 = train.columns.values[7],'positive','negative','Alchemy'
printline1, printline2 = model_performance(mod,c1,d1,e1)
print(printline1)
print(pd.crosstab(train.Classification, train.Sentiment1, margins=True),'\n')
print(printline2)
create_output(printline1, printline2)

mod,c1,d1,e1 = train.columns.values[8],'POS','NEG','Indico'
printline1, printline2 = model_performance(mod,c1,d1,e1)
print(printline1)
print(pd.crosstab(train.Classification, train.Sentiment2, margins=True),'\n')
print(printline2)
create_output(printline1, printline2)



df = train[['Classification','New_Rating','Sentiment1','Sentiment2','Pivot']]
print('*****************************','\nAll Model Comparison','\n*****************************')
print(df.pivot_table(index=['Classification','New_Rating','Sentiment1','Sentiment2'], aggfunc='count'))


######### Data exploration ##########
""" dataframe exploration """
"""

train.ix[:,'Review':] #view new dataframe
train.shape #see data structure: number of rows, number of columns
print(*reviews[10:20], sep="\n") # print 10 reviews on a new line
print(train["Review"][0]) #see first review

pd.crosstab([train.Doctor, train.Classification], train.New_Rating,  margins=True)
train[train['Classification']=='NEG'] #filter dataframe to only reviews classified as neg
train[(train.Classification=='NEG') & (train.New_Rating=='POS')]
check = cleaned[49:50]
[[(a,b,c,d,e,f,g,h,i) for a,b,c,d,e,f,g,h,i in y if b!='IRR'] for y in check] #filter multilevel list
"""



#precision gives amount of false positives (Type I error), calculates how many predictions were correct (positive predictive value)
#while recall gives amount of false negatives (Type II error), calculates how many test cases were caught (sensitivity)
