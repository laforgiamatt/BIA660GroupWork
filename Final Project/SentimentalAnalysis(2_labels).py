import ast
import json
import pandas as pd

def loadLexicon(fname):
    newLex=set()
    lex_conn=open(fname)
    #add every word in the file to the set
    for line in lex_conn:
        newLex.add(line.strip())# remember to strip to remove the lin-change character
    lex_conn.close()
    return newLex

def analysis(final):
    decisions=[]
    carddata=[]
    #load the positive and negative lexicons
    goodLex=loadLexicon('positive-words.txt')
    badLex=loadLexicon('negative-words.txt')

    for line in final: # for every line in the file (1 review per line)
        goodList=[] #list of good words in the review
        badList=[] #list of bad words in the review

        line=line.lower().strip()
        carddata.append(line)

        words=line.split(' ') # slit on the space to get list of words

        for word in words: #for every word in the review
            if word in goodLex: # if the word is in the good lexicon
                goodList.append(word) #update the good list for this card
            if word in badLex: # if the word is in the bad lexicon
                badList.append(word) #update the bad list for this card

        decision=0  
        if len(goodList)>len(badList): # more pos words than neg
            decision=1 # 1 for positive
        elif len(badList)>len(goodList):  # more neg than pos
            decision=0 # 0 for negative
        decisions.append(decision)

    return carddata, decisions

def finalBuilder():
    f = open('trainingCards.txt')
    no_of_cards = [i for i in f]
    op = [ast.literal_eval(i[1:-2]) for i in no_of_cards]
    final = [str(i['cardType'])+' '+str(i['cardText']) for i in op]
    return final

def dataframebuilder(carddata,decisions):
    df = pd.DataFrame()
    for i in range(len(carddata)):
        df['Carddata'] = list(carddata)
        df['Decisions'] = list(decisions)
        return df

def run():
    final = finalBuilder()
    carddata,decisions= analysis(final)
    df = dataframebuilder(carddata,decisions)
    print('Sentiment analysis')
    print(df)
    return df
