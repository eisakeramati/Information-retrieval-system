# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 10:56:36 2019

@author: eisak
"""

from nltk.tokenize import word_tokenize

def arranger(input_list, index):
    string = ""
    while input_list[index] != ".N\n":
        if input_list[index] == ".A\n":
            break
        string = string + input_list[index]
        string = string + " "
        index = index + 1
    return string       
        
###############################################
def query_file_reader():
    full_list = []
    f = open("cacm/query.text", "r")
    f_line = f.readlines()
    for x in range(len(f_line)):
        if f_line[x] == ".W\n":
            full_list.append(arranger(f_line, x+1))
    return full_list

def qrels_file_reader():
    full_list = []
    f = open("cacm/qrels.text", "r")
    f_line = f.readlines()
    size = int(word_tokenize(f_line[len(f_line)-1])[0])
    print(size)
    for i in range(size):
        temp = []
        full_list.append(temp)
    for i in range(len(f_line)):
        item = word_tokenize(f_line[i])
        s_list = full_list[int(item[0])-1]
        s_list.append(item[1])
        full_list[int(item[0])-1] = s_list    
    return full_list
    

print(qrels_file_reader())


