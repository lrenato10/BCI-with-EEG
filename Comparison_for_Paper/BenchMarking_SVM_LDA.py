# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 10:38:12 2020

@author: Luiz Renato
"""

#from Extraindo_Amostras_EEG import DataSetEEG
from BigDataSetEEG import ConcatenateDataSetEEG
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split#separa os dados de treinamento e valicadao
from sklearn.datasets import load_breast_cancer#importa o dataset do cancer
from sklearn.svm import SVC #importa o SVM
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA #importa o LDA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
import numpy as np
from mlxtend.plotting import plot_decision_regions#regiao de decisao da SVM

EEG=ConcatenateDataSetEEG( ID_inicial=2 , ID_final=2 , Remove_EOG=True, Bands='AB', Feature='duplo') #Bands ('AB' ou 'todas' ou 'unica')
E=EEG.Data_bandas#energia os sinais
label=EEG.Data_Label#rotulos do dataset

scores_train=[]
scores_test=[]
#E=E/np.min(E)
#%% ===================================================treinar modelo====================================================
for i in range(50):
    X_train, X_test, Y_train, Y_test = train_test_split(E,label,test_size=0.3)#separa dados de treinamento e validacao com 20% de validacao
    model=LDA(solver='lsqr',shrinkage='auto', tol=1e-8)
    #model=LDA(solver='svd', tol=1e-8)
    #model=QDA()
    #model=SVC(kernel='rbf',degree=3,C=1, tol=1e-5,gamma='scale',cache_size=20000)#chama o modelo como um classificador de vetores de suporte
    #C grande reduz a margem, kernel altera o formato do hiperplano
    #C=>inverso da margem
    #gamma => inverso do raio do rbf
    model.fit(X_train,Y_train)#treina o modelo com o classificador selecionado
    
    score_train=model.score(X_train,Y_train)
    scores_train=np.append(scores_train,score_train)
    
    score_test=model.score(X_test,Y_test)
    scores_test=np.append(scores_test,score_test)

media_train=np.average(scores_train)*100
standard_deviation_train=np.std(scores_train)*100
media_test=np.average(scores_test)*100
standard_deviation_test=np.std(scores_test)*100