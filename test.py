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
from search import TFIDF
from search import IDF
from search import cosine_similarity
import operator
from eval import query_file_reader
from eval import qrels_file_reader 
from eval import recall 
from eval import precision 

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
    while input_list[index] != ".N\n":
        if input_list[index] == ".K\n" or input_list[index] == ".C\n":
            break
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

def stopword_remover2(string, sett, cont):
    string = string.lower()
    ps = PorterStemmer()
    word_tokens = word_tokenize(string)
    filtered_sentence = []
    for w in word_tokens: 
        if w not in sett: 
            if cont=='y':
                print(w)
                filtered_sentence.append(ps.stem(w)) 
            else:
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
use = raw_input("Which mode are you using(1/2): ")
if use == '1':
    q = raw_input("Enter a word: ")
else:
    q = raw_input("Enter a phrase: ")
cons = raw_input("Do you want your query to be stemmed(y/n): ") 
if cons=='y':
    ps = PorterStemmer()
    q = ps.stem(q)
sw = raw_input("Do you want stop word removal(y/n): ")
stm = raw_input("Do you want stemming(y/n): ") 
start = time.time()
#main_func(sw, stm)
full_list = []
f = open("cacm/cacm.all", "r")
f_line = f.readlines()
f = open("cacm/unwanted.txt", "r")
set_alph = set()
f_line2 = f.readlines()
for i in range (len(f_line2)):
    set_alph.add(f_line2[i][0:len(f_line2[i])-1])
temp = dict.fromkeys(["ID", "Title", "Abstract", "Date", "Authors"])
for x in range(len(f_line)):
    if ".I " in f_line[x]:
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
        a = gen_tokenizer(arranger(f_line, x+1))
        while '.' in a:
            a.remove('.')
        while ',' in a:
            a.remove(',')
        if stm == 'y':
            temp['Authors'] = stemmer(a) 
        else:
            temp['Authors'] = a
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
def first_func(q):
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
        
        
def second_func(q, cont):
    
    words = stopword_remover2(q, set_alph, cont)
    #words = gen_tokenizer(q)
    print(words)
    idf = IDF(dict, len(full_list))
    a = TFIDF(dict, idf, words)
    list_mul=collections.OrderedDict()
    doc_list = []
    seen=[]
    for i in range (len(words)):
        if words[i] in seen:
            break
        else:
            seen.append(words[i])
        query = words[i]
        if query in dict:
            print(query)
            temp_list=[]
            with open('posting_list.txt') as f:
                index = 0
                f_line = f.readlines()
                for key in dict.keys():
                    if key == query:
                        break
                    index = index + int(dict[key])*2
                    
            flag = index + int(dict[key])*2
            while index < flag:
                doc_num = str(int(disconnector(f_line[index]))-1)
                if doc_num not in temp_list:
                    temp_list.append(doc_num)
                   # print(doc_num)
                index = index + 2
            temp_score={}
            print('here0')
            print(query)
            print(temp_list)
            count = len(temp_list)
            if len(temp_list)>15:
                count = 15
            for j in range (len(temp_list)):
                body=[]
                if full_list[int(temp_list[j])].get('Title') is not None and full_list[int(temp_list[j])].get('Abstract') is not None:
                    body = full_list[int(temp_list[j])].get('Title') + full_list[int(temp_list[j])].get('Abstract')
                    if full_list[int(temp_list[j])].get('Authors') is not None:
                        body = body + full_list[int(temp_list[j])].get('Authors') 
                if full_list[int(temp_list[j])].get('Title') is not None and full_list[int(temp_list[j])].get('Abstract') is None:
                    body = full_list[int(temp_list[j])].get('Title')
                    if full_list[int(temp_list[j])].get('Authors') is not None:
                        body = body + full_list[int(temp_list[j])].get('Authors') 
                else:
                    body = full_list[int(temp_list[j])].get('Abstract')
                    if full_list[int(temp_list[j])].get('Authors') is not None:
                        body = body + full_list[int(temp_list[j])].get('Authors') 
                b = TFIDF(dict, idf, body)
                sim = cosine_similarity(a, b)
                print(sim)
                print(full_list[int(temp_list[j])].get('ID'))
                temp_score.update({temp_list[j]:sim})
            print('here')
            sorted_score = sorted(temp_score.items(), key=operator.itemgetter(1))
            if len(sorted_score)<30:
                for q in range(0, len(sorted_score)):
                   (ind, sc) = sorted_score[len(sorted_score)-1-q]
                   list_mul.update({ind:sc})
            else:
                for q in range(0, 30):
                   (ind, sc) = sorted_score[len(sorted_score)-1-q]
                   list_mul.update({ind:sc})
    
    score = collections.OrderedDict()
    sorted_score = sorted(list_mul.items(), key=operator.itemgetter(1))
    if len(sorted_score)<25:
        for q in range(0, len(sorted_score)):
            (ind, sc) = sorted_score[len(sorted_score)-1-q]
            score.update({ind:sc})
    else:
        for q in range(0, 25):
            (ind, sc) = sorted_score[len(sorted_score)-1-q]
            score.update({ind:sc})
    score = sorted(score.items(), key=operator.itemgetter(1))
    for i in range(len(score)):
        print(i+1)
        id_doc = full_list[int(ind)].get('ID')
        print("Document ID:"+ id_doc)
        doc_list.append(id_doc)
        (ind, sc) = score[len(score)-1-i]
        tit = full_list[int(ind)].get('Title')
        if tit is not None:
            print(" ".join(str(x) for x in tit))
        if full_list[int(ind)].get('Authors') is not None:
            print('Author(s): ')
            for k in range(len(full_list[int(ind)].get('Authors'))):
                print(full_list[int(ind)].get('Authors')[k])
        print("score: "+str(sc))
        print('--------------------------------------------')
    return doc_list

queries = query_file_reader(0)
qrels = qrels_file_reader()
list_query = second_func(queries[39], cons)
print(qrels[39])
print(list_query)
print(str(recall(list_query, qrels[39]))+' percent')
print(str(precision(list_query, qrels[39])) +' percent')
print("execution time in seconds: "+ str(time.time()-start))
        

        
        
