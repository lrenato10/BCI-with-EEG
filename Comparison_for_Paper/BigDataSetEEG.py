# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 15:38:23 2020

@author: Luiz Renato
"""
from Extraindo_Amostras_EEG_sem_EOG import DataSetEEG_sem_EOG
#from Classificador.Extraindo_Amostras_EEG_sem_EOG import DataSetEEG_sem_EOG
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split#separa os dados de treinamento e valicadao
from sklearn.datasets import load_breast_cancer#importa o dataset do cancer
from sklearn.svm import SVC #importa o SVM
import numpy as np
from mlxtend.plotting import plot_decision_regions#regiao de decisao da SVM

class ConcatenateDataSetEEG():
    def __init__(self,ID_inicial=4,ID_final=4,Remove_EOG=True, Bands='AB', Feature='WAMP'):#pega apenas para o primeiro sujeito
        Data1=[]
        Data2=[]
        
        #chama o dataset
        self.Base=DataSetEEG_sem_EOG(ID_inicial, 1, Remove_EOG, Bands, Feature)#sinal sem EOG
        
        self.Data_Label=np.zeros((0))
        
        if (Feature=='duplo'):
            if Bands=='AB':
                self.Data_bandas=np.zeros((0,2*6))
            if Bands=='todas':
                self.Data_bandas=np.zeros((0,5*6))
            if Bands=='unica' or Bands=='A' or Bands=='B':
                self.Data_bandas=np.zeros((0,1*6))
            if Bands=='AB/':
                self.Data_bandas=np.zeros((0,6*6))
        
        else:
            if Bands=='AB':
                self.Data_bandas=np.zeros((0,2*3))
            if Bands=='todas':
                self.Data_bandas=np.zeros((0,5*3))
            if Bands=='unica' or Bands=='A' or Bands=='B':
                self.Data_bandas=np.zeros((0,1*3))
            if Bands=='AB/':
                self.Data_bandas=np.zeros((0,6*3))
        
        
        self.EEG_Signal=np.zeros((0,250*self.Base.temp_amostra,3))#tentativa, valores coletados no tempo da amostra, eletrodos C3 CZ C4
        for i in range(ID_final-ID_inicial+1):
            #extrai os dados do usuario de ID i
            self.Data1=DataSetEEG_sem_EOG(i+ID_inicial,1, Remove_EOG, Bands, Feature)
            self.Data2=DataSetEEG_sem_EOG(i+ID_inicial,2, Remove_EOG, Bands, Feature)    
    
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