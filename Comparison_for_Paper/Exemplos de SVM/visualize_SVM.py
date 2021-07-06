# -*- coding: utf-8 -*-
"""
https://jakevdp.github.io/PythonDataScienceHandbook/05.07-support-vector-machines.html
Created on Sun Nov  1 15:43:11 2020

@author: Luiz Renato
"""

%matplotlib
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.datasets.samples_generator import make_blobs
from sklearn.svm import SVC #importa o SVM
# use seaborn plotting defaults
import seaborn as sns; sns.set()

def plot_svc_decision_function(model, ax=None, plot_support=True):#funcoa que plota a margem q os vetores de suporte
    """Plot the decision function for a 2D SVC"""
    if ax is None:
        ax = plt.gca()
    xlim = ax.get_xlim()#limite do eixo x
    ylim = ax.get_ylim()#limita do eixo y
    
    # create grid to evaluate model
    x = np.linspace(xlim[0], xlim[1], 30)
    y = np.linspace(ylim[0], ylim[1], 30)
    Y, X = np.meshgrid(y, x)#cria os pontos da malha
    xy = np.vstack([X.ravel(), Y.ravel()]).T
    P = model.decision_function(xy).reshape(X.shape)
    
    # plot decision boundary and margins
    ax.contour(X, Y, P, colors='k',
               levels=[-1, 0, 1], alpha=0.5,
               linestyles=['--', '-', '--'])
    
    # plot support vectors
    if plot_support:
        ax.scatter(model.support_vectors_[:, 0],
                   model.support_vectors_[:, 1],
                   s=300, linewidth=1, marker='o',facecolors='None',edgecolors='black');
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)


X, y = make_blobs(n_samples=50, centers=2,
                  random_state=0, cluster_std=1.2)#gera agrupamento de pontos gaussianos

fig, ax = plt.subplots(1, 5, figsize=(16, 6))#cria um plot com 5 colunas de imagem
fig.subplots_adjust(left=0.0625, right=0.95, wspace=0.1)
KERNEL='poly'
plt.title(KERNEL)

for axi, C in zip(ax, [1000, 10, 1, 0.1, 0.01]):
    model = SVC(kernel=KERNEL, C=C,degree=4,).fit(X, y)
    axi.scatter(X[:, 0], X[:, 1], c=y, s=50, cmap='autumn')#plota os pontos com cor de acordo com o target Y
    plot_svc_decision_function(model, axi)
    axi.scatter(model.support_vectors_[:, 0],
                model.support_vectors_[:, 1],
                s=300, lw=1, facecolors='none');
    print(C)
    print(model.support_vectors_)
    axi.set_title('C = {0:.2f}'.format(C), size=14)