#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 09:05:19 2022

@author: jacob
"""

"""EXFOR DATA READING SCRIPT"""""
"""MAKE SURE YOU HAVE A FOLDER CALLED EXFORDATA IN YOUR CWD"""
"""NAME THE FILES WHAT YOU WOULD CALL EACH PLOT """

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob



countlines = int
countstarts = int
loopVAR= 0
rep=[]
lines=[]
Dict={}
leg=[]
cwd=os.getcwd()
Files=sorted(glob.glob(cwd+ "/EXFORDATA/*"))
#print(Files)
length=len(Files)
Reactions={}
Columns={}
NMBCol={}
Sets={}
Author={}
Energy={}
size=np.zeros((length))
Starts=np.zeros((length,5)) ##DOUBLE CHECK THAT THE AMOUNT OF DATA SETS MATCH THE NUMBER
Ends=np.zeros((length,5))
#This actually works really well for getting data points. Think it may acually be robust
for k in range (len(Files)):
    countlines = 0
    countstarts = 0
    loopVAR += 1
    Dataset=0
    with open(Files[k]) as f:
            oldlines=f.readlines()
            size[k]=int(len(oldlines))+size[k]
            
            for line in oldlines:
                line=line.strip()
                lines.append(line)                
                Dict[k,countlines]=line 
                countlines += 1
                if line[0:20]== "#+   Header    : EN ":
                    tempstr=oldlines[countlines-4]
                    Columns[k,countstarts-1]=int(tempstr[5]) 
                if line[0:10] == "#REACTION ":
                    Reactions[k,countstarts]=line[16:40] # This may be too short or too long 
                if line[0:9] == "#COLUMNS ":
                    NMBCol[k,countstarts]=int(line[16])
                if line[0:9] == "#COLUMNS ":
                    NMBCol[k,countstarts]=int(line[16])    
                if line[0:9] == "#AUTHOR1 ":
                    Author[k,countstarts]=line[16:32] # See line 67
                if line[0:5] == "#YEAR":
                    Author[k,countstarts]= Author[k,countstarts] + " "+ (line[16:20])
                if line[0:6]  == "#DATA ":
                    Starts[k,countstarts]=countlines
                if line[0:6]  == "!DATA ":
                    Energy[k,countstarts]=line
                    Energy[k,countstarts]=line.find("EN")
                if line[0:9] == "#ENDDATA ":
                    Ends[k,countstarts]=countlines-1
                    countstarts += 1
    Sets[k]=countstarts              
    f.close  

#for k in range (len(Files)):   
#    for l in range(len(Starts)):
#        length=int(size[k])
#        for j in range(0,length):
#            String_Dict=Dict[k,j]
#            PlotArray[j]=String_Dict
        #PlotArray_np=pd.DataFrame(PlotArray)    
#Cleans the new line vestigal /n from unix [FIXED IN TOP LOOP USING DICT]

#
Cleaned=[]
linenumber=0
r=0
size_int=0
#Reconstructs the original files in a 2-D array but without the \n[FIXED USING DICT IN TOP LOOP]
for l  in range(length):
   #print(size_int) 
   
   for j in range (0,4):
         if  Starts[l,j]>0:
             Starts[l,j] = Starts[l,j]+size_int
             
   size_int=int(size[l])+size_int 
size_int=0   
for l  in range(length):
   #print(size_int) 
   
   for j in range (0,4):
         if  Ends[l,j]>0:
             Ends[l,j] = Ends[l,j]+size_int
             
   size_int=int(size[l])+size_int     
FinalArr=np.zeros((length,20,1000,20))   
for k in range (len(Files)):   
    for l in range(0,4):
        
        Array_pd=pd.DataFrame(lines[int(Starts[k,l]):int(Ends[k,l])], columns= ["CS"])
        Array_pd["CS"].str.split( expand=True)
        Array_np=np.array(Array_pd)
        
       
        for g in  range(len(Array_np)):
            Temp= Array_np[g,0].split() 
            Temp1 =Array_np[g,0]
#            Temp= re.split("\t",Array_np[g,0])
            for f in range(len(Temp)):
                
                FinalArr[k,l,g,f]=float(Temp[f])
            if len((Temp)) < NMBCol[k,l]:
                    b=NMBCol[k,l]-len((Temp))
                    FinalArr[k,l,g,Columns[k,l]-1]=float(Temp1[Energy[k,l]-1:Energy[k,l]+4])
#                   FinalArr[k,l,g,f]=0
#        if  FinalArr[k,l,g,f] == 0:
#                    FinalArr[k,l,g,f] = 'NaN'
            
#Final Arr structure:
#   First index: File
#   Second index: Dataset
#   Third index : Value
#   Fourth index : Variable 
#IMPLEMENT CHECK FOR DATA VALUES
File=int(input("Select reaction:"))

#DataColumn=Columns[File,Sets]
for t in range(Sets[File]):
    DataColumn=Columns[File,t]-1
    plt.scatter(FinalArr[File,t,:,DataColumn],FinalArr[File,t,:,0],marker="+")
    leg.append(Author[File,t])
#plt.plot(FinalArr[Plot,1,:,2],FinalArr[Plot,1,:,0])
plt.title(Reactions[File,0])
plt.xlabel("Energy(MeV)")
plt.ylabel("Cross section (mb)")    
plt.legend(leg)
plt.xlim(8,50)

