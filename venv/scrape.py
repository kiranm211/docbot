from bs4 import BeautifulSoup
import urllib.request
import csv

parser = 'html.parser'  # or 'lxml' (preferred) or 'html5lib', if installed
resp = urllib.request.urlopen("https://www.mayoclinic.org/diseases-conditions/index?letter=0")
soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
blk  = soup.find(id = 'index')
blk2=blk.findAll("li")
names=[]
URLS=[]
for link in blk2:
    temp=link.findAll("span")
    if len(temp)==0 :
        anchor=link.find("a")
        name=anchor.text
        name1=name.replace(', ',' ')
        URL="https://www.mayoclinic.org" +anchor['href']
        name3=''.join(name1.split()).lower()
        #print(name1)
        names.append(name3)
        # add to list
        URLS.append(URL)

    else:
        anchor = link.find("a")
        temp1=link.find("span")
        if len(temp1)!= 0:
            name = temp1.text
            name1 = name[:-6]
            name2= name1.replace(", "," ")
            name3=''.join(name2.split()).lower()
            URL = "https://www.mayoclinic.org" + anchor['href']
            #print(name2)
            names.append(name3)  # add to list
            URLS.append(URL)

print('\n'.join(map(str, names)))
diseases = dict(zip(names,URLS))
for key in diseases:
    print(key, ' : ', diseases[key])





