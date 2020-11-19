# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 10:38:12 2020

@author: Luiz Renato
"""

from Extraindo_Amostras_EEG import DataSetEEG
from BigDataSetEEG import ConcatenateDataSetEEG
#from SVM.Extraindo_Amostras_EEG import DataSetEEG
#from SVM.BigDataSetEEG import ConcatenateDataSetEEG 
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split#separa os dados de treinamento e valicadao
from sklearn.datasets import load_breast_cancer#importa o dataset do cancer
from sklearn.svm import SVC #importa o SVM
import numpy as np
from mlxtend.plotting import plot_decision_regions#regiao de decisao da SVM
from collections import Counter

class mySVM():
    def __init__(self,primeiro_ID=4,ultimo_ID=4): 
        EEG=ConcatenateDataSetEEG(primeiro_ID,ultimo_ID)#importa o dataset do(primeiro sujeito, ultimo sujeito)
        self.E=EEG.Data_bandas#energia dos sinais
        self.label=EEG.Data_Label#rotulos do dataset
        self.Signal=EEG.EEG_Signal
    
    def treinar(self):
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.E,self.label,test_size=0.3)#embaralha os dados e separa em dados de treinamento e validacao com aquele percentual para dados de validacao 
        self.model=SVC(kernel='rbf',degree=3,C=10, tol=1e-5,gamma='scale',cache_size=20000)#chama o modelo como um classificador de vetores de suporte
        #C grande reduz a margem, kernel altera o formato do hiperplano
        #C=>inverso da margem
        #gamma => inverso do raio do rbf
        self.model.fit(self.X_train,self.Y_train)#treina o modelo com a SVM
    
    def acuracia(self):
        print('Treinamento')
        print(self.model.score(self.X_train,self.Y_train))#ve a acuracaia do treinamento
        print('Validacao')
        print(self.model.score(self.X_test,self.Y_test))#ve a acuracia da validacao
    
    def predizer(self,X_predict):
        self.Y_predict=self.model.predict(X_predict)#passa no modelo para fazer a predicao
        print(type(self.Y_predict))

C=mySVM(1,9)
#%% resto
C.treinar()
print(Counter(C.Y_train))
C.acuracia()
C.predizer([C.X_test[1,:]])
#x=C.Y_predict
