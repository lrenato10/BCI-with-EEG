#from BigDataSetEEG import ConcatenateDataSetEEG
from Classificador.BigDataSetEEG import ConcatenateDataSetEEG 
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split#separa os dados de treinamento e valicadao
from sklearn.datasets import load_breast_cancer#importa o dataset do cancer
from sklearn.svm import SVC #importa o SVM
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA #importa o LDA
import numpy as np
from mlxtend.plotting import plot_decision_regions#regiao de decisao da SVM
from collections import Counter

class MyClassifier():
    def __init__(self,primeiro_ID=4,ultimo_ID=4,Remove_EOG=True): 
        EEG=ConcatenateDataSetEEG(primeiro_ID,ultimo_ID,Remove_EOG)#importa o dataset do(primeiro sujeito, ultimo sujeito)
        self.label=EEG.Data_Label#rotulos do dataset
        self.E=EEG.Data_bandas#energia dos sinais
        self.E_indice=np.concatenate((self.E,np.transpose([range(len(self.label))])),axis=1)#cria uma coluna extra para identificar cada amostra
        self.Signal=EEG.EEG_Signal
    
    def treinar(self):
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.E_indice,self.label,test_size=0.3)#embaralha os dados e separa em dados de treinamento e validacao com aquele percentual para dados de validacao 
        #self.model=SVC(kernel='rbf',degree=3,C=10, tol=1e-5,gamma='scale',cache_size=20000)#chama o modelo como um classificador de vetores de suporte
        self.indices_train=self.X_train[:,-1]
        self.X_train=self.X_train[:,0:-1]#retira a ultima coluna
        self.indices_test=self.X_test[:,-1]
        self.X_test=self.X_test[:,0:-1]#retira a ultima coluna
        self.model=LDA(solver='lsqr',shrinkage='auto', tol=1e-8)
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
        
#C=MyClassifier(1,9)
#C.treinar()
#C.acuracia()
