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