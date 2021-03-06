#!/usr/bin/env python
# coding: utf-8




#test.py or test.m - should take CSV file as input and return predicted labels for the given time series data
#Ziming Dong
#CSE 572 Assignment2
import matplotlib.pyplot as plt
import pandas as pd
import os,glob
import warnings
import numpy as np
import seaborn
from scipy.fftpack import fft,ifft
from scipy.stats import kurtosis,skew
from sklearn.decomposition import PCA
from numpy import linalg as LA
from sklearn.model_selection import train_test_split
from sklearn import datasets
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report
import pickle
import csv
from csv import writer
from csv import reader

# Write a function to read input data and append to a list
def CSVlist(filename):
    File=[]
    with open(filename,newline='')as file:
        data = csv.reader(file)
        for row in data:
            File.append(row)
    return File

#
#Change the file name here !
# You can change the input cvs file name as you need in here to finish the test!
# Now I just simply use mealData1 file for testing.
#
Data=CSVlist('mealData1.csv')

# Don't change the code below
def clean(data):
    x = []
    for i in range (len(data)):
        data[i] = data[i][::-1]
        data[i] = data[i][:30]
        if (len(data[i])!= 30):
            x.append(i)
        elif 'NaN' in data[i]:
            x.append(i)      
    for j in range (len(x),0,-1):
        del data[x[j-1]]
    return data 

#Clean Data
Data=clean(Data)
#len(Data)

dfdata = pd.DataFrame(Data)

#Extract input data`s fft feature
fft_data_total=[]
for i in range(len(Data)):
    y=dfdata.iloc[i]
    yy=abs(fft(y))              
    yy1=np.delete(yy,0)
    yy2=np.unique(yy1)
    Max5=np.partition(yy2,-4)[-4:]
    normMax5=Max5/Max5.max(axis=0)
    fft_data_total.append(Max5)
#fft_data_total

dfFFT=pd.DataFrame(fft_data_total)
#dfFFT.shape

#Extract input data `s interquartile range feature
q_data_total=[]
for i in range(len(Data)):
    q=np.asarray(dfdata.iloc[i],dtype=np.float32)
    q1_x=np.quantile(q,0.25,interpolation='midpoint')
    q3_x=np.quantile(q,0.75,interpolation='midpoint')
    q4=np.array(q3_x-q1_x)
    q_data_total.append(q4)
#len(q_data_total)

#Extract input data`s skewness feature
s_data_total=[]
for i in range(len(Data)):
    s1=np.asarray(dfdata.iloc[i],dtype=np.float32)
    s2=np.array(skew(s1))
    s_data_total.append(s2)
#len(s_data_total)

feature_qs=feature=np.column_stack((q_data_total,s_data_total))
#feature_qs.shape

# Generate Feature matrix.
feature=np.column_stack((dfFFT,feature_qs))
#feature.shape

# Use the model which generated by train.py to predict the model
clf = pickle.load(open('model.pickle', 'rb'))
predict_result=clf.predict(feature)


result=predict_result.transpose()

# 20 points for developing a code in Python or Matlab that
# implements a function to take a test input and run the trained machine 
# to provide the class label as output
np.savetxt('labels.csv', result, fmt="%d")






