# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:48:48 2019

@author: eisak
"""

import numpy as np
import math
from collections import Counter
from collections import OrderedDict

def TF(input_dict, doc):
    vector = np.zeros(len(input_dict))
    occ = Counter(doc)
    for i in range(len(doc)):
        vector[input_dict.keys().index(doc[i])] = 1+ math.log(occ.get(doc[i]), 10)
    return vector

def IDF(input_dict, number):
    vector = np.zeros(len(input_dict))
    for key, value in input_dict.items():
        vector[input_dict.keys().index(key)] = math.log(1 + (number/int(value)), 10)
    return vector

def TFIDF(input_dict, idf, doc):
    vector = np.zeros(len(input_dict))
    tf = TF(input_dict, doc)
    vector = tf*idf
    return vector

def cosine_similarity(a, b):
    inner = np.inner(a,b)
    norma = np.linalg.norm(a)
    normb = np.linalg.norm(b)
    return inner/(norma*normb)
