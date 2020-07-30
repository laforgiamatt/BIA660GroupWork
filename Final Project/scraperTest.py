"""
unit tests for scraper
"""

#import response
import unittest

import scraper as myScraper

def checkDataParsedTest():
    assert myScraper.checkDataParsed('authors.txt') == True

def requestBuilderTest():
    assert myScraper.requestBuilder('http://www.google.com').status_code == 200

def driverBuilderTest():
    #TODO
    #Assert Driver is built

def randomLinkGeneratorTest():
    #TODO
    #Assert Link exists

def myStripTest():
    #TODO

def scrapeCardTest():
    #TODO

def csvWriterTest():
    #TODO

def runTest():
    assert True

if __name__ == "__main__":
    checkDataParsedTest()
    requestBuilderTest()
    runTest()
    print("Tests all passed")
