"""
Created on Sat Oct 31 13:28:51 2020

@author: Luiz Renato
"""

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split#separa os dados de treinamento e valicadao
from sklearn.datasets import load_breast_cancer#importa o dataset do cancer
from sklearn.svm import SVC #importa o SVM
import numpy as np
from mlxtend.plotting import plot_decision_regions#regiao de decisao da SVM

cancer=load_breast_cancer()#importa o dataset


df=pd.DataFrame(cancer.data, columns=cancer.feature_names)#pega os dados do data set e chama as colunas com o nome das caracteristicas
df=df.drop(df.columns[np.arange(2,len(cancer.feature_names))],axis=1)#tira todas as colunas e deixa so as duas primeiras
df.head()#printa o dataframe

df['target']=cancer.target#cria uma nova coluna com os rotulos
cancer.target_names#fala o que cada rotulo eh

#separa as classes
df0=df[df.target==0]
df1=df[df.target==1]

#plotando as classes pela sepala
plt.figure()
plt.xlabel('mean radius')
plt.ylabel('mean area')
plt.scatter(df0['mean radius'],df0['mean texture'],color='green',marker='+')#plota um grafico de pontos da classe 0
plt.scatter(df1['mean radius'],df1['mean texture'],color='red',marker='+')#plota um grafico de pontos da classe 1

X=np.array(df.drop(['target'],axis='columns'))#atribui o dataframe sem os rotulos
Y=np.array(df['target'])

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2)#separa dados de treinamento e validacao com 20% de validacao

model=SVC(kernel='poly',degree=3,C=100000)#chama o modelo como um classificador de vetores de suporte
#C grande reduz a margem, kernel altera o formato do hiperplano
model.fit(X_train,Y_train)#treina o modelo com a SVM
Y_predict=model.predict(X_test)#passa no modelo para fazer a predicao
print('Treinamento')
print(model.score(X_train,Y_train))#ve a acuracaia do treinamento
print('Validacao')
print(model.score(X_test,Y_test))#ve a acuracia da validacao

plt.figure()
plot_decision_regions(X=X, y=Y, clf=model, legend=2)
plt.xlabel("x", size=5)
plt.ylabel("y", size=5)
plt.title('SVM Decision Region Boundary', size=6)
# Visualize support vectors
plt.scatter(model.support_vectors_[:, 0], model.support_vectors_[:, 1],s=100, linewidth=1.5, marker='o',facecolors='None',edgecolors='red')
plt.title('Linearly separable data with support vectors')
#plt.show()
# Get support vectors themselves
print(len(model.support_vectors_))
