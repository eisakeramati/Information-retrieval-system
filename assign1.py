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
    if type(input_list)=='str':
       input_list = word_tokenize(input_list) 
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

def position_finder_list(string, input_list):
    position_list=[]
    temp = input_list
    index = 0
    if string in input_list:
        index = input_list.index(string, index)
        position_list.append(index)
        temp = input_list[index+1:len(input_list)]
        while (string in temp):
            index= index+1
            index = input_list.index(string, index)
            position_list.append(index)
            temp = input_list[index+1:len(input_list)]
    return position_list

def gen_tokenizer(string):
    return word_tokenize(string.lower())

########################################
#SECTION 1: Storing the input data
########################################

def main_func(sw, stm):
    full_list = []
    f = open("cacm/cacm.all", "r")
    f_line = f.readlines()
    f = open("stopwords.txt", "r")
    set_alph = set()
    f_line2 = f.readlines()
    for i in range (len(f_line2)):
        set_alph.add(f_line2[i][0:len(f_line2[i])-1])
    temp = dict.fromkeys(["ID", "Title", "Abstract", "Date", "Authors"])
    for x in range(len(f_line)):
        if ".I" in f_line[x]:
            temp = dict.fromkeys(["ID", "Title", "Abstract", "Date", "Authors"])
            temp['ID'] = f_line[x][2:len(f_line)]
        if ".T" in f_line[x]:
            #temp['Title'] = stopword_remover(f_line[x+1], set_alph)
            if sw != 'y' and stm != 'y':
                temp['Title'] = gen_tokenizer(f_line[x+1])
            elif sw =='y' and stm != 'y':
                temp['Title'] = stopword_remover(f_line[x+1], set_alph)
            elif sw != 'y' and stm =='y':
                temp['Title'] = stemmer(gen_tokenizer(f_line[x+1]))
            else:
                temp['Title'] = stemmer(stopword_remover(f_line[x+1], set_alph))
        if ".W" in f_line[x]:
            if sw != 'y' and stm != 'y':
                temp['Abstract'] = gen_tokenizer(arranger2(f_line, x+1))
            elif sw =='y' and stm != 'y':
                temp['Abstract'] = stopword_remover(arranger2(f_line, x+1), set_alph)
            elif sw != 'y' and stm =='y':
                temp['Abstract'] = stemmer(gen_tokenizer(arranger2(f_line, x+1))) 
            #temp['Abstract'] = stopword_remover(arranger2(f_line, x+1), set_alph)
            else:
                temp['Abstract'] = stemmer(stopword_remover(arranger2(f_line, x+1), set_alph))
        if ".B" in f_line[x]:
            temp['Date'] = f_line[x+1][5:len(f_line)]
        if ".A" in f_line[x]:
            temp['Authors'] = arranger(f_line, x+1)
        if ".X" in f_line[x]:
            full_list.append(temp)
            
    
    ########################################
    #SECTION 2: creating the postings list
    ########################################
    print('section 2...')
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
    print('first part out')
    posting_list = []
    for i in range(len(word_index_list)):
        posting_list_indiv =[]
        posting_list.append(posting_list_indiv)
#    for j in range (len(word_index_list)):
#        posting_list_indiv = []
#        for i in range(len(full_list)):
#            if full_list[i].get('Title') is not None and full_list[i].get('Abstract') is not None:
#                st = " ".join(str(x) for x in full_list[i].get('Title')) + " ".join(str(x) for x in full_list[i].get('Abstract'))
#            elif full_list[i].get('Title') is not None and full_list[i].get('Abstract') is None:
#                st = " ".join(str(x) for x in full_list[i].get('Title'))
#            elif full_list[i].get('Abstract') is not None:
#                st = " ".join(str(x) for x in full_list[i].get('Abstract'))
#            else:
#                continue
#            temp = position_finder(word_index_list[j], st)
#            if len(temp) != 0:
#                posting_list_indiv.append(posting(temp, len(temp), full_list[i].get('ID')))
#        posting_list.append(posting_list_indiv)
        
    for i in range(len(full_list)):
        if full_list[i].get('Title') is not None and full_list[i].get('Abstract') is not None:
            #st = " ".join(str(x) for x in full_list[i].get('Title')) + " ".join(str(x) for x in full_list[i].get('Abstract'))
            st = full_list[i].get('Title')
            st.extend(full_list[i].get('Abstract'))
        elif full_list[i].get('Title') is not None and full_list[i].get('Abstract') is None:
           # st = " ".join(str(x) for x in full_list[i].get('Title'))
            st = full_list[i].get('Title')
        elif full_list[i].get('Abstract') is not None:
            #st = " ".join(str(x) for x in full_list[i].get('Abstract'))
            st = full_list[i].get('Abstract')
        else:
            continue
        stored = []
        if full_list[i].get('Abstract') is not None:
            for j in range(len(full_list[i].get('Abstract'))):
                if full_list[i].get('Abstract')[j] not in stored:
                    posting_list_indiv = posting_list[word_index_list.index(full_list[i].get('Abstract')[j])]
                    #temp = position_finder(full_list[i].get('Abstract')[j], st)
                    temp = position_finder_list(full_list[i].get('Abstract')[j], st)
                    stored.append(full_list[i].get('Abstract')[j])
                    if len(temp) != 0:
                        posting_list_indiv.append(posting(temp, len(temp), full_list[i].get('ID')))
                        posting_list[word_index_list.index(full_list[i].get('Abstract')[j])] = posting_list_indiv
        if full_list[i].get('Title') is not None:
            for j in range(len(full_list[i].get('Title'))):
                if full_list[i].get('Title')[j] not in stored:
                    posting_list_indiv = posting_list[word_index_list.index(full_list[i].get('Title')[j])]
                    #temp = position_finder(full_list[i].get('Title')[j], st)
                    temp = position_finder_list(full_list[i].get('Title')[j], st)
                    if len(temp) != 0:
                        posting_list_indiv.append(posting(temp, len(temp), full_list[i].get('ID')))
                        posting_list[word_index_list.index(full_list[i].get('Title')[j])] = posting_list_indiv
    
    ########################################
    #SECTION 3: creating the df dictionary
    ########################################  
    print('section 3...')    
    dictn = collections.OrderedDict()
    for j in range(len(word_index_list)):
        num = len(posting_list[j])
        dictn.update({word_index_list[j]:num})
    #print(dictn.get('23'))
    #print(len(dictn))
        
    ########################################
    #SECTION 4: saving the outputs in files
    ########################################  
    print('section 4...')
    with open('dictionary.csv', 'w') as f:
        for key in dictn.keys():
            if key == ',':
                f.write("%s,%s\n"%('","', dictn[key]))
            else:
                f.write("%s,%s\n"%(key, dictn[key]))
    
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
                
#main_func(sw, stm)


        
            
    

    
            
            


            




    
