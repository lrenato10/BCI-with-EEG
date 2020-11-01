# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 13:28:51 2020

@author: Luiz Renato
"""

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split#separa os dados de treinamento e valicadao
from sklearn.datasets import load_iris#importa o dataset iris
from sklearn.svm import SVC #importa o SVM

iris=load_iris()#importa o dataset


df=pd.DataFrame(iris.data, columns=iris.feature_names)#pega os dados do data set e chama as colunas com o nome das caracteristicas
df.head()#printa o dataframe

df['target']=iris.target#cria uma nova coluna com os rotulos
iris.target_names#fala o que cada rotulo eh

#separa as classes
df0=df[df.target==0]
df1=df[df.target==1]
df2=df[df.target==2]

#plotando as classes pela sepala
plt.figure()
plt.xlabel('sepal length (cm)')
plt.ylabel('sepal width (cm)')
plt.scatter(df0['sepal length (cm)'],df0['sepal width (cm)'],color='green',marker='+')#plota um grafico de pontos da classe 0
plt.scatter(df1['sepal length (cm)'],df1['sepal width (cm)'],color='red',marker='+')#plota um grafico de pontos da classe 1
#plotando as classes pela petala
plt.figure()
plt.xlabel('petal length (cm)')
plt.ylabel('petal width (cm)')
plt.scatter(df0['petal length (cm)'],df0['petal width (cm)'],color='green',marker='+')#plota um grafico de pontos da classe 0
plt.scatter(df1['petal length (cm)'],df1['petal width (cm)'],color='red',marker='+')#plota um grafico de pontos da classe 1
#
plt.figure()
plt.title('mais bagunçado')
plt.xlabel('petal length (cm)')
plt.ylabel('petal width (cm)')
plt.scatter(df1['petal width (cm)'],df0['sepal length (cm)'],color='green',marker='+')#plota um grafico de pontos da classe 0
plt.scatter(df2['petal width (cm)'],df1['sepal length (cm)'],color='red',marker='+')#plota um grafico de pontos da classe 1



X=df.drop(['target'],axis='columns')#atribui o dataframe sem os rotulos
Y=df['target']

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2)#separa dados de treinamento e validacao com 20% de validacao

model=SVC(kernel='linear',C=1)#chama o modelo como um classificador de vetores de suporte
model.fit(X_train,Y_train)#treina o modelo com a SVM
Y_predict=model.predict(X_test)#passa no modelo para fazer a predicao

print(model.score(X_test,Y_test))#ve a acuracia da validacao
