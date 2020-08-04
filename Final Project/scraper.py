"""
Scrape Data from Scryfall, store it in csv
"""

import csv
import os.path
import re
import requests
import time

from bs4 import BeautifulSoup
from selenium import webdriver

#Project Imports
import trainingDataParser as tDP
#from tDP import fullFileReader


def checkDataParsed(filename):
    if os.path.exists(filename):
        return True
    else:
        return False


def driverBuilder(url):
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)
    time.sleep(2)

    return driver


def randomLinkGenerator():
    driver = driverBuilder('http://www.scryfall.com')
    randomCardLink = driver.find_element_by_link_text('Random Card')
    url = randomCardLink.get_attribute('href')
    driver.quit()
    return url


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

 
def myStrip(scrapedData):
    cleanText = scrapedData.text.strip()

    return cleanText 


def scrapeCard(cardPageText):
    cardData = {'cardName': None,
                'cardCost': None,
                'cardType': None,
                'cardSubtypes': None,
                'cardText': None}

    cardSoup = BeautifulSoup(cardPageText, 'lxml') 
    cardName = cardSoup.find('h1', {'class': 'card-text-title'})
    cardCost = cardSoup.find('span', {'class': 'card-text-mana-cost'})
    cardType = cardSoup.find('p', {'class':'card-text-type-line'})   
    cardText = cardSoup.find('div', {'class':'card-text-oracle'})
    
    if cardName and cardCost:
        cardName = myStrip(cardName)
        cardCost = myStrip(cardCost)
        try:
            cardName = cardName.replace(cardCost,'')
        except:
            print('Failed on ' + cardName)
        cardData['cardName'] = cardName.strip()
        cardData['cardCost'] = cardCost
    else:
        if cardName:
            cardData['cardName'] = myStrip(cardName).strip()
        if cardCost:
            cardData['cardCost'] = myStrip(cardCost)
    if cardType:
        cardType = myStrip(cardType)
        hasHyphen = cardType.find('—')
        if hasHyphen == -1:
            cardData['cardType'] = cardType
        else:
            cardData['cardType'] = cardType[0:hasHyphen].strip()
            cardData['cardSubtypes'] = cardType[hasHyphen+1:len(cardType)].strip()
    if cardText:
        cardData['cardText'] = myStrip(cardText)
    
    return cardData


def csvWriter(cardData, dataFilename):
    if not checkDataParsed(dataFilename):
        with open(dataFilename, 'w', encoding='utf8') as outfile:
            writer = csv.writer(outfile, lineterminator='\n')
            writer.writerow([cardData])
    else:
        with open(dataFilename, 'a', encoding='utf8') as outfile:
            writer = csv.writer(outfile, lineterminator='\n')
            writer.writerow([cardData])

    return


def run(dataFilename='trainingCards.txt', rebuildTraining=True, setSize=10000):
    alreadyScrapedSet = set()
    if checkDataParsed(dataFilename) and rebuildTraining==False:
        return
    else:
        if checkDataParsed(dataFilename) and rebuildTraining == True:
            os.remove(dataFilename)
        for i in range(setSize):
            url = randomLinkGenerator()
            response = requestBuilder(url)
            cardData = scrapeCard(response.text)
            print('Scraping ' + cardData['cardName'])
            if checkDataParsed(dataFilename):    
                alreadyScrapedSet = tDP.fullFileReader(dataFilename)
            if set(cardData) in alreadyScrapedSet:
                print('Already seen ' + cardData['cardName'])
                i = i-1
                continue
            csvWriter(cardData, dataFilename)
    print('Done')

#run(setSize=1, rebuildTraining=False, dataFilename='authors.txt')
#run(setSize=1, rebuildTraining=False)
#run(setSize=1)
run(setSize=7)
