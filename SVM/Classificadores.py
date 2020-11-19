# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 10:38:12 2020

@author: Luiz Renato
"""

from SVM.Extraindo_Amostras_EEG import DataSetEEG
from SVL.BigDataSetEEG import ConcatenateDataSetEEG
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split#separa os dados de treinamento e valicadao
from sklearn.datasets import load_breast_cancer#importa o dataset do cancer
from sklearn.svm import SVC #importa o SVM
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA #importa o LDA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
import numpy as np
from mlxtend.plotting import plot_decision_regions#regiao de decisao da SVM

EEG=ConcatenateDataSetEEG(4,4)#importa o dataset do(primeiro sujeito, ultimo sujeito)
E=EEG.Data_bandas#energia os sinais
label=EEG.Data_Label#rotulos do dataset

#E=E/np.min(E)
#%% ===================================================treinar a SVM====================================================
X_train, X_test, Y_train, Y_test = train_test_split(E,label,test_size=0.3)#separa dados de treinamento e validacao com 20% de validacao
model=LDA(solver='lsqr',shrinkage='auto', tol=1e-8)
#model=QDA()
#model=SVC(kernel='rbf',degree=3,C=1, tol=1e-5,gamma='scale',cache_size=20000)#chama o modelo como um classificador de vetores de suporte
#C grande reduz a margem, kernel altera o formato do hiperplano
#C=>inverso da margem
#gamma => inverso do raio do rbf
model.fit(X_train,Y_train)#treina o modelo com a SVM
Y_predict=model.predict(X_test)#passa no modelo para fazer a predicao
print('Treinamento')
print(model.score(X_train,Y_train))#ve a acuracaia do treinamento
print('Validacao')
print(model.score(X_test,Y_test))#ve a acuracia da validacao
#%%=============================================plota padrao===============
fig, ax = plt.subplots(1, 2, figsize=(16, 6))#cria um plot com 5 colunas de imagem
fig.subplots_adjust(left=0.0625, right=0.95, wspace=0.1)
title=['Alfa','Alfa','Alfa','Beta','Beta','Beta']
for axi, i in zip(ax, range(0,6,3)):
    train=axi.scatter(X_train[:,i], X_train[:,i+2],c=Y_train, s=50,cmap='autumn')
    test=axi.scatter(X_test[:,i], X_test[:,i+2],c='purple', s=10,cmap='autumn')
    axi.set_title(title[i], size=14)
    axi.set_xlabel('C3')
    axi.set_ylabel('C4')
    axi.legend((train,test),('Treinamento','Validação'))

