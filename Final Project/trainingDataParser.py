"""
Training Data Parser
"""

def fullFileReader(fileName):
    newLex = set()
    cardLex = open(fileName)
    for line in cardLex:
        newLex.add(line.strip())
    cardLex.close()
    return newLex

def getAllNames():
    return

def getAllCardTypes():
    return

#Get all data types so we can try and ensure we have a balanced amount of Data, lete term
#We can also speedup the already seen stuff by just keying it off of name instead of the entire entry