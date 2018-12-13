# -*- coding: utf-8 -*-
from typing import List, Iterable, Union, Tuple, Dict, Optional
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn


import math 
from collections import Counter
import re
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.tokenize import RegexpTokenizer
import numpy as np

WORD = re.compile(r'\w+')
tokenizer = RegexpTokenizer(r'\w+')
stop_words = ['that', 'is']

def vectorize(text_list):
     return Counter(text_list)

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator
    
def preprocess(description):
    tokens = tokenizer.tokenize(description)
    tokens = [x for x in tokens if x not in stop_words]
    return [x.lower() for x in tokens]
    
class nearest_neighbor:
    
    def __init__(self):
        self.table = {}

    def fit(self, X: List[str], y: List[str]):
        
        assert all(isinstance(elem, str) for elem in X) and all(isinstance(elem, str) for elem in y)
        assert len(X) == len(y)
        
        for index, description in enumerate(X):
            self.table[description] = y[index]
            
    
    def predict(self, input_sent):
        
        input_sent = vectorize(preprocess(input_sent))
        
        list_desc = list(self.table.keys())
        scores = [get_cosine(input_sent, vectorize(preprocess(x))) for x in list_desc]

        return self.table[list_desc[np.argmax(scores)]]
    
clf = nearest_neighbor()

#example table
X = ['create not even list from 0 to 100',
     'create list from 0 to 100 that is not not even',
     'create list from 0 to 100 that is not not not even']

y = ['[x for x in range(0, 101) if x % 2 == 0]',
     '[x for x in range(0, 101) if x % 2 == 0]',
     '[x for x in range(0, 101) if not x % 2 == 0]']
     
clf.fit(X,y)
print(clf.predict('create list from 0 to 100 that is not not not not even'))