# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 10:56:36 2019

@author: eisak
"""

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

def arranger(input_list, index, stemm):
    string = ""
    ps = PorterStemmer()
    while input_list[index] != ".N\n":
        if input_list[index] == ".A\n":
            break
        if stemm == 1:
            string = string + ps.stem(input_list[index])
        else:
            string = string + input_list[index]
        string = string + " "
        index = index + 1
    return string   

def intersection(lst1, lst2): 
    lst3 = []
    for i in range(len(lst1)):
        if str(int(lst1[i])) in lst2:
            lst3.append(lst1[i])
    return lst3     
        
###############################################
def query_file_reader(stemm):
    full_list = []
    f = open("cacm/query.text", "r")
    f_line = f.readlines()
    for x in range(len(f_line)):
        if f_line[x] == ".W\n":
            full_list.append(arranger(f_line, x+1, stemm))
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

def recall(list1, list2):
    return len(intersection(list1, list2))*100/len(list2)

def precision(list1, list2):
    return (len(intersection(list1, list2))*100/len(list1))

def AP_finder(list1, list2):
    num = 0.0
    count = 0.0
    for i in range(len(list1)):
        if str(int(list1[i])) in list2:
            count  = count + 1
            num = num + (count/float(i+1))
    return (num / len(list2))

def R_prec(list1, list2):
    sum = 0.0 
    for i in range(len(list2)):
        if str(int(list1[i])) in list2:
            sum = sum + 1
    return sum/float(len(list2))



