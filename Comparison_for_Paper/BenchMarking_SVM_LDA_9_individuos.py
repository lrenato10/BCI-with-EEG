# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 08:48:21 2021

@author: Luiz Renato
"""

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


#dados estatisticos LDA
media_train_LDA=np.zeros(9)
std_train_LDA=np.zeros(9)
media_test_LDA=np.zeros(9)
std_test_LDA=np.zeros(9)

#dados estatistico SVM
media_train_SVM=np.zeros(9)
std_train_SVM=np.zeros(9)
media_test_SVM=np.zeros(9)
std_test_SVM=np.zeros(9)

for i in range(1,10):#passa pelos individuos
    EEG=ConcatenateDataSetEEG( ID_inicial=i , ID_final=i , Remove_EOG=True, Bands='AB', Feature='duplo') #Bands ('AB', 'A','B', 'AB/', 'todas' ou 'unica') Feature ('WAMP', 'RMS', 'duplo','NE' , 'LL' ou 'PSD')
    E=EEG.Data_bandas#energia os sinais
    label=EEG.Data_Label#rotulos do dataset
    
    scores_train_LDA=[]
    scores_test_LDA=[]
    scores_train_SVM=[]
    scores_test_SVM=[]
    #E=E/np.min(E)
    #%% ===================================================treinar modelo====================================================
    for j in range(50):
        X_train, X_test, Y_train, Y_test = train_test_split(E,label,test_size=0.3)#separa dados de treinamento e validacao com 20% de validacao
        #model=LDA(solver='lsqr',shrinkage='auto', tol=1e-8)
        #model=LDA(solver='svd', tol=1e-8)
        #model=QDA()
        #model=SVC(kernel='rbf',degree=3,C=1, tol=1e-5,gamma='scale',cache_size=20000)#chama o modelo como um classificador de vetores de suporte
        #C grande reduz a margem, kernel altera o formato do hiperplano
        #C=>inverso da margem
        #gamma => inverso do raio do rbf
        
        
        model=LDA(solver='lsqr',shrinkage='auto', tol=1e-7)
        model.fit(X_train,Y_train)#treina o modelo com o classificador selecionado
        
        score_train_LDA=model.score(X_train,Y_train)
        scores_train_LDA=np.append(scores_train_LDA,score_train_LDA)
        
        score_test_LDA=model.score(X_test,Y_test)
        scores_test_LDA=np.append(scores_test_LDA,score_test_LDA)
        
        
        model=SVC(kernel='rbf',degree=3,C=1, tol=1e-5,gamma='scale',cache_size=20000)#chama o modelo como um classificador de vetores de suporte
        model.fit(X_train,Y_train)#treina o modelo com o classificador selecionado
        
        score_train_SVM=model.score(X_train,Y_train)
        scores_train_SVM=np.append(scores_train_SVM,score_train_SVM)
        
        score_test_SVM=model.score(X_test,Y_test)
        scores_test_SVM=np.append(scores_test_SVM,score_test_SVM)
    
    media_train_LDA[i-1]=np.average(scores_train_LDA)*100
    std_train_LDA[i-1]=np.std(scores_train_LDA)*100
    media_test_LDA[i-1]=np.average(scores_test_LDA)*100
    std_test_LDA[i-1]=np.std(scores_test_LDA)*100
    
    media_train_SVM[i-1]=np.average(scores_train_SVM)*100
    std_train_SVM[i-1]=np.std(scores_train_SVM)*100
    media_test_SVM[i-1]=np.average(scores_test_SVM)*100
    std_test_SVM[i-1]=np.std(scores_test_SVM)*100
    
feature_media_LDA=np.average(media_test_LDA)
feature_std_LDA=np.std(media_test_LDA)

feature_media_SVM=np.average(media_test_SVM)
feature_std_SVM=np.std(media_test_SVM)

np.savetxt("media_test_LDA.csv", media_test_LDA, delimiter=",", fmt='%1.2f')
np.savetxt("std_test_LDA.csv", std_test_LDA, delimiter=",", fmt='%1.2f')
np.savetxt("media_test_SVM.csv", media_test_SVM, delimiter=",", fmt='%1.2f')
np.savetxt("std_test_SVM.csv", std_test_SVM, delimiter=",", fmt='%1.2f')