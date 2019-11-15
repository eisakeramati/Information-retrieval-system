# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 18:23:14 2019

@author: eisak
"""
import numpy as np
import math

def TP_matrix(mat, alpha):
    n = len(mat)
    TPM = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if (str(j+1) in mat[i]):
                TPM[j][i] = 1
            else:
                TPM[j][i] = 0
    for i in range(n):
        temp = TPM[i]
        x = np.count_nonzero(temp)
        if x != 0:
            for j in range(n):
                if temp[j] == 1:
                    temp[j] = (1.0/(x))*(1-alpha) + (alpha/n)
                else:
                    temp[j] = (alpha/n)
        else:
            temp.fill(1.0/n)
        TPM[i] = temp
    return TPM

def convergence(mat):
    vec = np.zeros((1,len(mat[0])))
    vec[0][0] = 1
    #for i in range(int(math.log(len(mat[0])))):
    for i in range(20):
        vec = vec.dot(mat)
    return vec

def normalize(mat):
    minn = np.amin(mat)
    maxx = np.amax(mat)
    for i in range(len(mat)):
        mat[i] = (mat[i] - minn)/(maxx - minn)
    return mat

a=[[],['1'],['1','2'],['3','2']]
p = TP_matrix(a,0.2)
print(normalize(convergence(p)))
