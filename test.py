# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 08:51:23 2019

@author: eisak
"""

import collections
import csv
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from colorama import Style
from colorama import Back
from assign1 import main_func
import time

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

def disconnector(string):
    pos_list = position_finder(',', string)
    return string[pos_list[len(pos_list)-1]+2:len(string)]

def gen_tokenizer(string):
    return word_tokenize(string.lower())

def inside_word(string, doc):
    for item in doc:
        if string in item:
            return doc.index(item)
    return -1

########################################
#SECTION 1: reading the corpus
########################################
q = raw_input("Enter a word: ")
cons = raw_input("Do you want your query to be stemmed(y/n): ") 
if cons=='y':
    ps = PorterStemmer()
    q = ps.stem(q)
sw = raw_input("Do you want stop word removal(y/n): ")
stm = raw_input("Do you want stemming(y/n): ") 
start = time.time()
main_func(sw, stm)
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
#SECTION 2: reading input files
########################################   
dict = collections.OrderedDict()
with open('dictionary.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if len(row)==2:
            dict.update({row[0]:row[1]})
        else:
            st=''
            for k in range(len(row)-1):
                st = st + row[k]+","
            st = st[0:len(st)-1]
            dict.update({st:row[len(row)-1]})

#query = 'acceler'
#print(dict)
#print(len(dict))
#print
query = q
print(query +":")
if query in dict:
    print("This term was seen in "+dict[query]+ " documents.")
    print('-------------------------------------------\n')
    with open('posting_list.txt') as f:
        index = 0
        f_line = f.readlines()
        for key in dict.keys():
            if key == query:
                break
            index = index + int(dict[key])*2
    
    ########################################
    #SECTION 3: output construction
    ######################################## 
    flag = index + int(dict[key])*2
    while index < flag:
        doc_num = str(int(disconnector(f_line[index]))-1)
        print('Document number '+ str(int(disconnector(f_line[index]))) +" :")
        print('This term is seen in this document '+ f_line[index][0: position_finder(',', f_line[index])[0]] +' times.')
        if full_list[int(doc_num)].get('Title') is not None and full_list[int(doc_num)].get('Abstract') is not None:
            tit = full_list[int(doc_num)].get('Title')
            abst = full_list[int(doc_num)].get('Abstract')
            print('Title: ')
            print(" ".join(str(x) for x in full_list[int(doc_num)].get('Title')) +"\n")
            if query in tit or inside_word(query, tit)!= -1:
                if query in tit:
                    point = tit.index(query)
                else:
                    point = inside_word(query, tit)
                if point-1>=0:
                    if point-6>=0:
                        st1 = " ".join(str(x) for x in tit[point-6:point])
                    else:
                        st1 = " ".join(str(x) for x in tit[0:point])
                else:
                    st1 = ""
                if point + 1 <= len(tit):
                    if point + 6 <= len(tit):
                        st2 = " ".join(str(x) for x in tit[point+1:point+ 6])
                    else:
                        st2 = " ".join(str(x) for x in tit[point+1:len(tit)])
                else:
                    st2 = ""
                print(st1+ " " +Back.CYAN + tit[point] + Style.RESET_ALL+" " + st2)
                
            if query in abst or inside_word(query, abst)!= -1:
                if query in abst:
                    point = abst.index(query)
                else:
                    point = inside_word(query, abst)
                if point-1>=0:
                    if point-6>=0:
                        st1 = " ".join(str(x) for x in abst[point-6:point])
                    else:
                        st1 = " ".join(str(x) for x in abst[0:point])
                else:
                    st1 = ""
                if point + 1 <= len(abst):
                    if point + 6 <= len(abst):
                        st2 = " ".join(str(x) for x in abst[point+1:point+ 6])
                    else:
                        st2 = " ".join(str(x) for x in abst[point+1:len(abst)])
                else:
                    st2 = ""
                print(st1+" "+ Back.CYAN + abst[point] + Style.RESET_ALL+" " + st2)
            
        elif full_list[int(doc_num)].get('Title') is not None and full_list[int(doc_num)].get('Abstract') is None:
            tit = full_list[int(doc_num)].get('Title')
            print('Title : ')
            print(" ".join(str(x) for x in full_list[int(doc_num)].get('Title')) +"\n")
            if query in tit:
                point = tit.index(query)
            else:
                point = inside_word(query, tit)
            if point-1>=0:
                if point-6>=0:
                    st1 = " ".join(str(x) for x in tit[point-6:point])
                else:
                    st1 = " ".join(str(x) for x in tit[0:point])
            else:
                st1 = ""
            if point + 1 <= len(tit):
                if point + 6 <= len(tit):
                    st2 = " ".join(str(x) for x in tit[point+1:point+ 6])
                else:
                    st2 = " ".join(str(x) for x in tit[point+1:len(tit)])
            else:
                st2 = ""
            print(st1+ " "+Back.CYAN + tit[point] + Style.RESET_ALL+" " + st2)
        else:
            abst = full_list[int(doc_num)].get('Abstract')
            if query in abst:
                point = full_list.index(query)
            else:
                point = inside_word(query, abst)
            if point-1>=0:
                if point-6>=0:
                    st1 = " ".join(str(x) for x in abst[point-6:point])
                else:
                    st1 = " ".join(str(x) for x in abst[0:point])
            else:
                st1 = ""
            if point + 1 <= len(abst):
                if point + 6 <= len(abst):
                    st2 = " ".join(str(x) for x in abst[point+1:point+ 6])
                else:
                    st2 = " ".join(str(x) for x in abst[point+1:len(abst)])
            else:
                st2 = ""
            print(st1+ " "+Back.CYAN + abst[point]+ Style.RESET_ALL +" " + st2)  
                
        print('positions : '+f_line[index][position_finder(',', f_line[index])[0]+1:position_finder(',', f_line[index])[len(position_finder(',', f_line[index]))-2]])
        print('-------------------------------------------\n')
        index = index + 2
else:
    print('This term is not present in the documents.')
    
print("execution time in seconds: "+ str(time.time()-start))
        

        
        
