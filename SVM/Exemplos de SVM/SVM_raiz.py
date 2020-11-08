# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 22:52:05 2020

@author: Luiz Renato
"""

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split#separa os dados de treinamento e valicadao
from sklearn.datasets import load_breast_cancer#importa o dataset do cancer
from sklearn.svm import SVC #importa o SVM
import numpy as np
from mlxtend.plotting import plot_decision_regions#regiao de decisao da SVM

X = np.array([[1,1],[2,2],[1,2],[8,1],[1,7], [6,6],[6,7],[7,6],[8,7],[10,10],[13,15],[2,13],[10,8],[11,2]])#o dado deve ter dimensao (n_sample x n_feature)  OBS:n_feature<n_samples
Y = np.array([0,0,0,0,0,1,1,1,1,2,2,2,2,2])# dimensao (n_sample) pode ter mais de 2 classes
model = SVC(kernel='poly',degree=6,C=1)
model.fit(X, Y)
# Print out the support vectors
print(model.support_vectors_)
# Let us make a prediction
teste=np.array([7,8])
pred=model.predict(teste.reshape(1,-1))
if pred == 0:
    cor='blue'
if pred==1:
    cor='orange'
if pred==2:
    cor='blue'

plt.figure()
plot_decision_regions(X=X, y=Y, clf=model, legend=2)
plt.xlabel("x", size=5)
plt.ylabel("y", size=5)
plt.title('SVM Decision Region Boundary', size=6)
plt.scatter(teste[0],teste[1],color=cor,marker='+')
plt.show()