### scrape the Ratemds reviews ###

#imports
import requests, csv, time, re
from bs4 import BeautifulSoup


# Set up variables
reviewer=['Reviewer']
doctor=['Doctor']
reviewtext=['ReviewText']
reviewdate=['SubmitDate']
counter = 0

root = 'https://www.ratemds.com'
base = root+'/best-doctors/ny/new-york/'
search_urls = [base]
page_urls = []
sub_urls = []

# Define functions to access the main pages
def get_page_urls(url1):
    page = requests.get(url1).text
    soup = BeautifulSoup(page,"html.parser")
    links=[]
    for g in soup.find_all("a", class_="search-item-doctor-link"):
        links.append(root + g.get('href'))
    return links;

def get_subs(url2):
    page = requests.get(url2).text
    soup = BeautifulSoup(page,"html.parser")
    d = [c.attrs.get('href') for c in soup.select('a[href^=?p]')]
    f=[]
    for e in d:
        g=re.findall(r'\d+', e)
        for h in g:
            f.append(int(h))
    link2=max(f)
    return link2;

def get_page_data(url3):
    page = requests.get(url3).text
    soup = BeautifulSoup(page,"html.parser")
    rtext=[]
    rvw=[]
    dts=[]
    for a in soup.find_all("p","rating-comment-body"):
        rtext.append(a.text)
        counter=counter+1
        count=counter
        rvw.append('User'+str(counter))    
    for c in soup.find_all("meta", {"itemprop":"dateCreated datePublished"}):
        dts.append(c['content'])
    rmax=len(rtext)
    b=soup.h1.get_text()
    doctor.extend([b.strip('\n')]*rmax)
    for l in rtext:
        reviewtext.append(l)
    for m in rvw:
        reviewer.append(m)
    for n in dts:
        reviewdate.append(n)
    return count;


#Build a list of links to scrape from
for i in range(2, 901):
    search_urls.append(base+'?page='+str(i))

for x in search_urls:
    time.sleep(0.2)
    links = get_page_urls(x)
    for a in links:    
        page_urls.append(a)

for x in page_urls:
    time.sleep(0.2)
    maxsubs = get_subs(x)
    while maxsubs>0:
        new_url=x+'?page='+str(maxsubs)
        sub_urls.append(new_url)
        maxsubs=maxsubs-1

all_urls = page_urls+sub_urls

#Retrieve review data from each website
for x in all_urls:
    time.sleep(0.2)    
    placehold = get_page_data(x)


#Create the dataset
dataset = zip(reviewer, doctor, reviewtext, reviewdate)

with open('reviews_NYC.csv', 'w') as myfile:
    wr = csv.writer(myfile)
    for row in dataset:
        wr.writerow(row)


