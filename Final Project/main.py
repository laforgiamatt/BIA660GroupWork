"""
runs scraper, sentiment analysis and neural net
options to rebuild and sizes
no params to use old trainingcards data without having to rescrape
first param number of cards to scrape
"""

import sys

import scraper as Scraper
import SentimentAnalysis as SentimentAnalysis

def main():
    params = sys.argv[1:]
    if len(params) == 0:
        Scraper.run(rebuildTraining=False)
    else:
        numberofcards = int(params[0])
        Scraper.run(setSize=numberofcards)
    
    SentimentAnalysis.run()

if __name__ == "__main__":
    main()