# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 20:25:25 2019

@author: eisak
"""
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import collections

########################################
#SECTION 0: Helping functions and classes
########################################
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

class posting:
    def __init__(self, pos, term_freq, doc_id):
        self.positions = pos
        self.TD = term_freq
        self.ID = doc_id

def position_finder(string, doc):
    position_list=[]
    index = doc.find(string)
    sum = 0
    while (index != -1):
        sum = sum + index 
        position_list.append(sum)
        sum = sum + len(string)
        doc = doc[index+len(string): len(doc)]
        index = doc.find(string)
    return position_list

########################################
#SECTION 1: Storing the input data
########################################
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
st = " ".join(str(x) for x in full_list[39].get('Abstract'))
print(st)  

########################################
#SECTION 2: creating the postings list
########################################
word_index_list = []
for i in range(len(full_list)):
    temp = full_list[i].get('Title')
    temp2 = full_list[i].get('Abstract')
    if temp is not None:
        for j in range(len(temp)):
            if temp[j] not in word_index_list:
                word_index_list.append(temp[j])
    if temp2 is not None:
        for j in range(len(temp2)):
            if temp2[j] not in word_index_list:
                word_index_list.append(temp2[j])
word_index_list.sort()
print(word_index_list)    

posting_list = []
for j in range (len(word_index_list)):
    posting_list_indiv = []
    for i in range(len(full_list)):
        if full_list[i].get('Title') is not None and full_list[i].get('Abstract') is not None:
            st = " ".join(str(x) for x in full_list[i].get('Title')) + " ".join(str(x) for x in full_list[i].get('Abstract'))
        elif full_list[i].get('Title') is not None and full_list[i].get('Abstract') is None:
            st = " ".join(str(x) for x in full_list[i].get('Title'))
        else:
            st = " ".join(str(x) for x in full_list[i].get('Abstract'))
        temp = position_finder(word_index_list[j], st)
        if len(temp) != 0:
            posting_list_indiv.append(posting(temp, len(temp), full_list[i].get('ID')))
    posting_list.append(posting_list_indiv)


########################################
#SECTION 3: creating the df dictionary
########################################      
dict = collections.OrderedDict()
for j in range(len(word_index_list)):
    num = 0
    for i in range(len(full_list)):
        if full_list[i].get('Title') is not None and full_list[i].get('Abstract') is not None:
            st = " ".join(str(x) for x in full_list[i].get('Title')) + " ".join(str(x) for x in full_list[i].get('Abstract'))
        elif full_list[i].get('Title') is not None and full_list[i].get('Abstract') is None:
            st = " ".join(str(x) for x in full_list[i].get('Title'))
        else:
            st = " ".join(str(x) for x in full_list[i].get('Abstract'))
        if word_index_list[j] in st:
            num = num + 1
    dict.update({word_index_list[j]:num})
print(dict)
    
########################################
#SECTION 4: saving the outputs in files
########################################  
with open('dictionary.csv', 'w') as f:
    for key in dict.keys():
        f.write("%s,%s\n"%(key, dict[key]))

with open('posting_list.txt', 'w') as f:
    for i in range(len(posting_list)):
        temp = posting_list[i]
        for j in range(len(temp)):
            f.write("%s"%(len(temp[j].positions)))
            f.write(",")
            for k in range(len(temp[j].positions)):
                f.write("%s"%(temp[j].positions[k]))
                f.write(",")
            f.write("%s"%(temp[j].TD))
            f.write(",")
            f.write("%s"%(temp[j].ID))
            f.write("-------------------------------------------\n")


        
            
    

    
            
            


            




    
