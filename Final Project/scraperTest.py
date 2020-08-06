
"""
unit tests for scraper
"""
#import response
import unittest
import requests
import csv
import os.path
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver

import scraper as myScraper


dataFilename='test_trainingCards.txt'
#Test Url
url = 'https://scryfall.com/card/bng/135/raised-by-wolves'
response = myScraper.requestBuilder(url)
cardData = myScraper.scrapeCard(response.text)

def checkDataParsedTest():
    assert myScraper.checkDataParsed('authors.txt') == True

def requestBuilderTest():
    assert myScraper.requestBuilder('http://www.google.com').status_code == 200

def driverBuilderTest():
#   Assert Driver is built
    driver.get('https://www.w3schools.com/html/html_examples.asp')
    print(driver.title)
    assert driver.title == 'HTML Examples'

def randomLinkGeneratorTest():
    #Assert Link exists
    assert myScraper.randomLinkGenerator()=="https://scryfall.com/random"

def myStripTest():
    htmltxt = "<p>Hello World</p>"
    soup = BeautifulSoup(htmltxt, 'lxml')
    assert myScraper.myStrip(soup) == 'Hello World'

def scrapeCardTest():
    assert len(cardData['cardName'])>1
    assert len(cardData['cardType'])>1
    #assert len(cardData['cardText'])>1

def csvWriterTest():
    cardData = myScraper.scrapeCard(response.text)
    assert len(cardData['cardName'])>1
    assert len(cardData['cardType'])>1
    assert len(cardData['cardText'])>1

def csvWriterTest():
    myScraper.csvWriter(cardData, dataFilename)
    assert myScraper.checkDataParsed(dataFilename)==True

def runTest():
#     myScraper.run()
    fname = 'test_trainingCards.txt'

    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    no_of_lines_count =i + 1
    assert no_of_lines_count > 1

if __name__ == "__main__":
    checkDataParsedTest()
    requestBuilderTest()
    randomLinkGeneratorTest()
    myStripTest()
    scrapeCardTest()
    csvWriterTest()
    runTest()
    print("Tests all passed")
