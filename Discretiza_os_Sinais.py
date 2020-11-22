# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 07:43:59 2020

@author: Luiz Renato
"""

#from Extraindo_Amostras_EEG import DataSetEEG
#from BigDataSetEEG import ConcatenateDataSetEEG
from SVM.Extraindo_Amostras_EEG import DataSetEEG
from SVM.BigDataSetEEG import ConcatenateDataSetEEG 
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split#separa os dados de treinamento e valicadao
from sklearn.datasets import load_breast_cancer#importa o dataset do cancer
from sklearn.svm import SVC #importa o SVM
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA #importa o LDA
import numpy as np
from mlxtend.plotting import plot_decision_regions#regiao de decisao da SVM
from collections import Counter

EEG=ConcatenateDataSetEEG(1,1)#importa o dataset do(primeiro sujeito, ultimo sujeito)
Signal=EEG.EEG_Signal
SignalTentativa=Signal[0,:,:]
resolucao=2**16-1#conversor AD de 16bits (ultimo valor 2^n-1)
ganho=10e3#ganho para levar 100uV em 1V->para discretizar em relacao a 1

SignalA=SignalTentativa*ganho*resolucao#calculo do valor de saida do conversor AD
#os valores adquirios foram flutuante quase inteiros
SignalD=np.round(SignalA).astype(int)#arredonda eles para o inteiro mais próximo
SignalDp=SignalD/2+((2**16)/2-1)#todos os numeros sao pares entao podemos dividilos por 2, e somarmos a metade da escala
SignalDp=np.round(SignalDp).astype(int)

eletrodo=['C3','CZ','C4']
def escreve_txt():
    arq_data=open('EEG_Signal (C3,CZ,C4).txt','w')#escreve um arquivo em branco ou cria um
    for j in range(np.shape(SignalDp)[1]):
        arq_data.write(f'\n{eletrodo[j]}:\n')
        for i in range(np.shape(SignalDp)[0]-250):
            arq_data.write(f'{SignalDp[i][j]},')
        
    arq_data.close()
def plotEEG():        
        fig, axs = plt.subplots(3, 1, figsize=(16, 6))#cria um plot com 5 colunas de imagem
        fig.subplots_adjust(left=0.0625, right=0.95, wspace=0.1)
        PC3=axs[0].plot(np.arange(0,1,1/250),SignalTentativa[:250,0] , lw =2.0 , color="green", label = "C3")
        axs[0].set_title('C3')
        axs[0].set_xlabel('Tempo [s]')
        axs[0].set_ylabel('Tensão [V]')
        axs[0].grid()
        PCZ=axs[1].plot(np.arange(0,1,1/250),SignalTentativa[:250,1] , lw =2.0 , color="red", label = "CZ")
        axs[1].set_title('CZ')
        axs[1].set_xlabel('Tempo [s]')
        axs[1].set_ylabel('Tensão [V]')
        axs[1].grid()
        PC4=axs[2].plot(np.arange(0,1,1/250),SignalTentativa[:250,2] , lw =2.0 , color="blue", label = "C4")
        axs[2].set_title('C4')
        axs[2].set_xlabel('Tempo [s]')
        axs[2].set_ylabel('Tensão [V]')
        axs[2].grid()
escreve_txt()
plotEEG()