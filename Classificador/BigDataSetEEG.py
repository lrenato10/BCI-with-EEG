# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 15:38:23 2020

@author: Luiz Renato
"""

from Classificador.Extraindo_Amostras_EEG import DataSetEEG
#from Extraindo_Amostras_EEG import DataSetEEG 
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split#separa os dados de treinamento e valicadao
from sklearn.datasets import load_breast_cancer#importa o dataset do cancer
from sklearn.svm import SVC #importa o SVM
import numpy as np
from mlxtend.plotting import plot_decision_regions#regiao de decisao da SVM

class ConcatenateDataSetEEG():
    def __init__(self,ID_inicial=4,ID_final=4):#pega apenas para o primeiro sujeito
        Data1=[]
        Data2=[]
        self.Base=DataSetEEG(ID_inicial,1)
        self.Data_Label=np.zeros((0))
        self.Data_bandas=np.zeros((0,6))
        self.EEG_Signal=np.zeros((0,250*self.Base.temp_amostra,3))#tentativa, valores coletados no tempo da amostra, eletrodos C3 CZ C4
        for i in range(ID_final-ID_inicial+1):
            #extrai os dados do usuario de ID i
            self.Data1=DataSetEEG(i+ID_inicial,1)
            self.Data2=DataSetEEG(i+ID_inicial,2)
    
            #concatena os dados do usuario de ID i
            self.Data12_label=np.concatenate((self.Data1.label, self.Data2.label), axis=0)#concatena na vertical
            self.Data12_bandas=np.concatenate((self.Data1.bandas, self.Data2.bandas), axis=0)#concatena na vertical
            self.EEG_Signal12=np.concatenate((self.Data1.y,self.Data2.y),axis=0)#concatena na vertical
            
            #concatena todos os ID para um unico DataSet
            self.Data_Label=np.concatenate((self.Data_Label, self.Data12_label), axis=0)#concatena na verticl
            self.Data_bandas=np.concatenate((self.Data_bandas, self.Data12_bandas), axis=0)#concatena na vertical
            self.EEG_Signal=np.concatenate((self.EEG_Signal,self.EEG_Signal12),axis=0)#concatena na vertical
            
        #self.Data_Label=np.delete(self.Data_Label,0,0)#apega primeira linha
        #self.Data_bandas=np.delete(self.Data_bandas,0,0)#apega primeira linha
    

#D=ConcatenateDataSetEEG(1,2)