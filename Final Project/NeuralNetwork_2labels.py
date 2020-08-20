import SentimentAnalysis as SA
import SentimentAnalysis_2labels as SA2
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from numpy import array
from keras.layers.core import Activation, Dropout, Dense
from keras.layers import Flatten
from keras.layers import GlobalMaxPooling1D
from keras.layers.embeddings import Embedding
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
import seaborn as sns


def preprocess_text(sen):
    # Removing html tags
    sentence = remove_tags(sen)
    # Remove punctuations and numbers
    sentence = re.sub('[^a-zA-Z]', ' ', sentence)
    # Single character removal
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)
    # Removing multiple spaces
    sentence = re.sub(r'\s+', ' ', sentence)
    return sentence

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

def model(X=None):
    
    df = SA2.run()
    sns.countplot(x='Decisions', data=df)

    X = []
    sentences = list(df['Carddata'])
    for sen in sentences:
        X.append(preprocess_text(sen))

    y = df['Decisions']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    tokenizer = Tokenizer(num_words=10000)
    tokenizer.fit_on_texts(X_train)

    X_train = tokenizer.texts_to_sequences(X_train)
    X_test = tokenizer.texts_to_sequences(X_test)
    vocab_size = len(tokenizer.word_index) + 1
    maxlen = 300

    X_train = pad_sequences(X_train, padding='post', maxlen=maxlen)
    X_test = pad_sequences(X_test, padding='post', maxlen=maxlen)


    embeddings_dictionary = dict()
    glove_file = open('glove.42B.300d.txt', encoding="utf8")

    for line in glove_file:
        records = line.split()
        word = records[0]
        vector_dimensions = np.asarray(records[1:], dtype='float32')
        embeddings_dictionary [word] = vector_dimensions
    glove_file.close()

    embedding_matrix = np.zeros((vocab_size, 300))
    for word, index in tokenizer.word_index.items():
        embedding_vector = embeddings_dictionary.get(word)
        if embedding_vector is not None:
            embedding_matrix[index] = embedding_vector

    model = Sequential()
    embedding_layer = Embedding(vocab_size, 300, weights=[embedding_matrix], input_length=maxlen , trainable=False)
    model.add(embedding_layer)
    model.add(Flatten())
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])

    print(model.summary())
    history = model.fit(X_train, y_train, batch_size=128, epochs=6, verbose=1, validation_split=0.2)
    score = model.evaluate(X_test, y_test, verbose=1)
    print("Score:", score[0])
    print("Test Accuracy:", score[1])
    return model

def run():
    model()

# Testing:
def testingNN():
    tokenizer = Tokenizer(num_words=5000)
    X = []
    model = model(X)
    test = X[4]
    print(test)
    test = tokenizer.texts_to_sequences(test)
    sentlist = []
    for sublist in test:
        for item in sublist:
            sentlist.append(item)

    sentlist = [sentlist]

    test = pad_sequences(sentlist, padding='post', maxlen=300)

    print(model.predict(test))
