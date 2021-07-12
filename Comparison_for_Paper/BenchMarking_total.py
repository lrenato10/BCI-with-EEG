# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 13:02:42 2021

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

feature_media_LDA=np.zeros((4,6))
feature_std_LDA=np.zeros((4,6))

feature_media_SVM=np.zeros((4,6))
feature_std_SVM=np.zeros((4,6))

for b in range (4):#percorre as banda
    if b==0:
        band='todas'
    elif b==1:
        band='unica'
    elif b==2:
        band='AB'
    elif b==3:
        band='AB/'
    
    for f in range (6):#percorre as features
        if f==0:
            feature='WAMP'
        elif f==1:
            feature='RMS'
        elif f==2:
            feature='NE'
        elif f==3:
            feature='LL'
        elif f==4:
            feature='MAV'
        elif f==5:
            feature='duplo'
        
        for i in range(1,10):#passa pelos individuos
            EEG=ConcatenateDataSetEEG( ID_inicial=i , ID_final=i , Remove_EOG=True, Bands=band, Feature=feature) #Bands ('AB', 'A','B', 'AB/', 'todas' ou 'unica') Feature ('WAMP', 'RMS', 'duplo','NE' , 'LL' ou 'PSD')
            E=EEG.Data_bandas#energia os sinais
            label=EEG.Data_Label#rotulos do dataset
            
            scores_train_LDA=[]
            scores_test_LDA=[]
            scores_train_SVM=[]
            scores_test_SVM=[]
            #E=E/np.min(E)
            #===================================================treinar modelo====================================================
            for j in range(50):#itera varias vezes para tirar media da acuracia
                X_train, X_test, Y_train, Y_test = train_test_split(E,label,test_size=0.3)#separa dados de treinamento e validacao com 20% de validacao
                #model=LDA(solver='lsqr',shrinkage='auto', tol=1e-8)
                #model=LDA(solver='svd', tol=1e-8)
                #model=QDA()
                #model=SVC(kernel='rbf',degree=3,C=1, tol=1e-5,gamma='scale',cache_size=20000)#chama o modelo como um classificador de vetores de suporte
                #C grande reduz a margem, kernel altera o formato do hiperplano
                #C=>inverso da margem
                #gamma => inverso do raio do rbf
                
                
                model=LDA(solver='lsqr',shrinkage='auto', tol=1e-8)
                model.fit(X_train,Y_train)#treina o modelo com o classificador selecionado
                
                score_train_LDA=model.score(X_train,Y_train)
                scores_train_LDA=np.append(scores_train_LDA,score_train_LDA)
                
                score_test_LDA=model.score(X_test,Y_test)
                scores_test_LDA=np.append(scores_test_LDA,score_test_LDA)
                
                
                model=SVC(kernel='poly',degree=3,C=1, tol=1e-5,gamma='scale',cache_size=20000)#chama o modelo como um classificador de vetores de suporte
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
        
        feature_media_LDA[b,f]=np.average(media_test_LDA)
        feature_std_LDA[b,f]=np.std(media_test_LDA)
        
        feature_media_SVM[b,f]=np.average(media_test_SVM)
        feature_std_SVM[b,f]=np.std(media_test_SVM)

np.savetxt("feature_media_LDA_3.csv", feature_media_LDA, delimiter=",", fmt='%1.2f')
np.savetxt("feature_std_LDA_3.csv", feature_std_LDA, delimiter=",", fmt='%1.2f')
np.savetxt("feature_media_SVM_3.csv", feature_media_SVM, delimiter=",", fmt='%1.2f')
np.savetxt("feature_std_SVM_3.csv", feature_std_SVM, delimiter=",", fmt='%1.2f')