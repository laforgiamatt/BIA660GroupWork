"""
runs scraper, sentiment analysis and neural net
options to rebuild and sizes
no params to use old trainingcards data without having to rescrape
first param number of cards to scrape
"""

import sys

import scraper as Scraper
import SentimentAnalysis as SentimentAnalysis
import neuralnetwork as Neuralnetwork
import SentimentAnalysis_2labels as SA2
import NeuralNetwork_2labels as nn2

def main():
    params = sys.argv[1:]
    if len(params) == 0:
        Scraper.run(rebuildTraining=False)
    elif params[1] == 'scrapeMore':
        numberofcards = int(params[0])
        Scraper.run(setSize=numberofcards, rebuildTraining=False, scrapeMore=True)
    else:
        numberofcards = int(params[0])
        Scraper.run(setSize=numberofcards)
    
    #SentimentAnalysis.run()

    #Neuralnetwork.run()
    SA2.run()
    nn2.run()


if __name__ == "__main__":
    main()