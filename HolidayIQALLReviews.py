__author__ = 'Rahul G'
import urllib.request
from bs4 import BeautifulSoup
#Beautifulsoup is not only beautiful but extremely powerful :D
import sqlite3
conn=sqlite3.connect('TravelIQReviews')

primaryURL = "http://www.holidayiq.com/destinations/"
primaryHTML = urllib.request.urlopen(primaryURL).read()
soup = BeautifulSoup(primaryHTML,'html.parser')
weekendList=soup.find_all("ul", {"id" : "weekend-getaway-list"})[0].find_all("li")
statesUrl=[]
for states in weekendList:
    statesUrl.append(states.find_all("a",{})[0].get("href"))
namesList=[]
for url in statesUrl:
    htmlData = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(htmlData,'html.parser')
    destinations = soup.find_all("div",{"class":"weekend-section-one"})
    for namesOfDestinations in destinations:
        namesList.append(namesOfDestinations.get("data-destination-name"))

for place in namesList:
    placeUrl=primaryURL+place
    try:
        htmlData = urllib.request.urlopen(placeUrl).read()
        soup = BeautifulSoup(htmlData,'html.parser')
        reviews=(soup.find_all("div",{"id":"REVIEWS"}))
        for i in reviews:
            reviewSet = i.find_all("div", {"class":"hotel-view"})
            for i in reviewSet:
                name=i.find_all("li",{"class":"reviewer-name"})[0].text
                header=i.find_all("a",{"class":"reviews-tag-line-link"})[0].text
                review=i.find_all("blockquote",{"class":"margin0 review_datail_height"})[0].text
                #print(place,names,header,review,'\n')
                conn.execute("INSERT INTO Reviews (place,name,heading,review) VALUES(?,?,?,?)" ,(place,name,header,review))
                conn.commit()
    except:
        print(place)
        pass
conn.close()


