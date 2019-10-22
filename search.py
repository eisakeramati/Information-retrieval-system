# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 18:48:48 2019

@author: eisak
"""

import numpy as np
import math
from collections import Counter

def TF(input_dict, doc, query):
    vector = np.zeros(len(doc) + len(query))
    vector2 = np.zeros(len(doc) + len(query)) 
    occ = Counter(doc)
    occ2 = Counter(query)
    dic = {}
    for i in range(len(doc)):
        if doc[i] not in dic:
            dic.update({doc[i]:i})
    for i in range(len(query)):
        if query[i] not in dic:
            dic.update({query[i]:i+len(doc)})
    for i in range(len(doc)):
        if doc[i] in input_dict.keys():
            temp = 1+ math.log(occ.get(doc[i]), 10)
            vector[dic.get(doc[i])] = temp
    for i in range(len(query)):
        if query[i] in input_dict.keys():
            temp = 1+ math.log(occ2.get(query[i]), 10)
            vector2[dic.get(query[i])] = temp
            #temp = 1+ math.log(occ.get(doc[i]), 10)
            #vector[input_dict.keys().index(doc[i])] = temp
    return vector, vector2

def IDF(input_dict, number, doc, query):
    vector = np.zeros(len(doc) + len(query))
    dic = {}
    for i in range(len(doc)):
        if doc[i] not in dic:
            dic.update({doc[i]:i})
    for i in range(len(query)):
        if query[i] not in dic:
            dic.update({query[i]:i+len(doc)})
    for key, value in dic.items():
    #for i in range(len(doc)):
        #print(key)
        if key in input_dict.keys():
            v2 = input_dict.get(key)
            vector[value] = math.log(1 + (number/int(v2)), 10)
    return vector

def TFIDF(input_dict, doc, query, number):
    vector = np.zeros(len(doc)+len(query))
    vector2 = np.zeros(len(doc)+len(query))
    (tf, tf2) = TF(input_dict, doc, query)
    idf = IDF(input_dict, number, doc, query)
    vector = tf*idf
    vector2 = tf2*idf
    return vector, vector2

def cosine_similarity(a, b):
    inner = np.inner(a,b)
    norma = np.linalg.norm(a)
    normb = np.linalg.norm(b)
    return inner/(norma*normb)
