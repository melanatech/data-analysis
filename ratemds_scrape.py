# scrape the Ratemds reviews


#imports
import requests, csv
from bs4 import BeautifulSoup

# Access the main page
target_URL = 'https://www.ratemds.com/doctor-ratings/877154/Dr-Alen+J.-Salerian-WASHINGTON-DC.html'
page = requests.get(target_URL).text
soup = BeautifulSoup(page,"html.parser")

baseURL=['baseURL']
Doctor=['Doctor']
Reviewtext=['ReviewText']
Staff=['Staff']
Punctuality = ['Punctuality']
Helpfulness = ['Helpfulness']
Knowledge =['Knowledge']
Ratingslist = ['Ratingslist']
Ratingshdr = ['Ratingshdr']


#set up data
for a in soup.find_all("p","rating-comment-body"):
        Reviewtext.append(a.text)

for b in soup.find_all("span","value"):
        Ratingslist.append(b.text)

for c in soup.find_all("div","type"):
        Ratingshdr.append(c.text)

rmax=len(Reviewtext)
for d in soup.find_all("link", rel='canonical', href=True):
        baseURL.extend([d.get('href')]*rmax)

e=soup.h1.get_text()
Doctor.extend([e.strip('\n')]*rmax)

pages = [f.attrs.get('href') for f in soup.select('a[href^=?p]')]

#Create the dataset
dataset = zip(baseURL, Doctor, Reviewtext)

with open('example_webscrape_output.csv', 'wb') as myfile:
    wr = csv.writer(myfile)
    for row in dataset:
        wr.writerow(row)

