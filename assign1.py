# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 20:25:25 2019

@author: eisak
"""
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

def arranger2(input_list, index):
    string = ""
    while ".B" not in input_list[index]:
        string = string + input_list[index]
        string = string + " "
        index = index + 1
    return string

def arranger(input_list, index):
    string = ""
    while ".N" not in input_list[index]:
        string = string + input_list[index]
        string = string + " "
        index = index + 1
    return string

def stopword_remover(string, sett):
    string = string.lower()
    word_tokens = word_tokenize(string)
    filtered_sentence = []
    for w in word_tokens: 
        if w not in sett: 
            filtered_sentence.append(w) 
    return filtered_sentence

def stemmer(input_list):
    output = []
    ps = PorterStemmer()
    for word in input_list:
        output.append(ps.stem(word))
    return output
    

full_list = []
f = open("cacm/cacm.all", "r")
f_line = f.readlines()
f = open("stopwords.txt", "r")
set_alph = set()
f_line2 = f.readlines()
for i in range (len(f_line2)):
    set_alph.add(f_line2[i][0:len(f_line2[i])-1])
temp = dict.fromkeys(["ID", "Title", "Abstract", "Date", "Authors"])
for x in range(760):
    if ".I" in f_line[x]:
        temp = dict.fromkeys(["ID", "Title", "Abstract", "Date", "Authors"])
        temp['ID'] = f_line[x][2:len(f_line)]
    if ".T" in f_line[x]:
        #temp['Title'] = stopword_remover(f_line[x+1], set_alph)
        temp['Title'] = stemmer(stopword_remover(f_line[x+1], set_alph))
    if ".W" in f_line[x]:
        #temp['Abstract'] = stopword_remover(arranger2(f_line, x+1), set_alph)
        temp['Abstract'] = stemmer(stopword_remover(arranger2(f_line, x+1), set_alph))
    if ".B" in f_line[x]:
        temp['Date'] = f_line[x+1][5:len(f_line)]
    if ".A" in f_line[x]:
        temp['Authors'] = arranger(f_line, x+1)
    if ".X" in f_line[x]:
        full_list.append(temp)
        
print("----------------")
for i in range(len(full_list)):
    print(full_list[i].get('Abstract'))
    print(full_list[i].get('Authors'))
    print(full_list[i].get('Date'))
    print(full_list[i].get('ID'))
    print(full_list[i].get('Title'))
    print('------------------------------------------')



    
