"""
Scrape Data from Scryfall, store it in json
"""

import os.path
import requests
import time

from selenium import webdriver

#check if data exists
def checkDataParsed(filename):
    if os.path.exists(filename):
        return True
    else:
        return False

#scrape data (10 000 random sources)
def driverBuilder(url):
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    time.sleep(2)

    return driver

def closeDriverPage():
    #TODO: Close the driver page as it opens a new page for each card
    return

def randomLinkGenerator():
    driver = driverBuilder('http://www.scryfall.com')
    randomCardLink = driver.find_element_by_link_text('Random Card')
    url = randomCardLink.get_attribute('href')
    closeDriverPage()
    return url

#try and build url request
def requestBuilder(url):
    for i in range(5):
        response=requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
        if response:
            break
        else:
            time.sleep(2)

    if not response: 
        return None
    else:
        return response

 
#scrape data individual data
def scrapeCard(cardPageText):
    #TODO
    cardData = True
    return cardData

#store as json
def jsonWriter(cardData):
    #TODO
    return print('Writer')

#possible json helper function


def run(dataFilename='trainingCards.txt', rebuildTraining=True, setSize=10000):
    if checkDataParsed(dataFilename) and rebuildTraining==False:
        return
    else:
        for i in range(setSize):
            url = randomLinkGenerator()
            response = requestBuilder(url)
            cardData = scrapeCard(response.text)
            jsonWriter(cardData)

#run(setSize=1, rebuildTraining=False, dataFilename='authors.txt')
#run(setSize=1, rebuildTraining=False)
#run(setSize=1)
run(setSize=5)