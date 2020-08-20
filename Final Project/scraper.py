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
    cleanText = cleanText.replace("'","")
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


def scrapeFunctions(dataFilename, setSize):
    alreadySeen = set()
    for i in range(setSize):
        url = randomLinkGenerator()
        response = requestBuilder(url)
        cardData = scrapeCard(response.text)
        if cardData['cardName'] in alreadySeen:
            print('Already seen ' + cardData['cardName'])
            i = i-1
            continue
        alreadySeen.add(cardData['cardName'])
        print('Scraping ' + cardData['cardName'])
        csvWriter(cardData, dataFilename)

    return

def run(dataFilename='trainingCards.txt', rebuildTraining=True, setSize=10000, scrapeMore=False):
    if checkDataParsed(dataFilename) and rebuildTraining==False and scrapeMore == False:
        return
    else:
        if checkDataParsed(dataFilename) and rebuildTraining == True and scapeMore == False:
            os.remove(dataFilename)
            scrapeFunctions(dataFilename, setSize)
        if checkDataParsed(dataFilename) and scrapeMore == True:
            scrapeFunctions(dataFilename, setSize)
    print('Done')