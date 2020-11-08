# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 15:07:16 2020

@author: Luiz Renato
"""

import os
import numpy as np
import mne
from mne import read_evokeds
import matplotlib.pyplot as plt

#def AbrirEEG():
raw=mne.io.read_raw_gdf('DataSet/BCICIV_2b_gdf/B0101T.gdf')

raw.info['bads'] = ['EOG:ch01','EOG:ch02','EOG:ch03']#retira os sinais EOG
print(raw)
print(raw.info)

#%% ===================================================plot pronto====================================================
#raw.plot_psd(fmax=125)#espectro de frequencia com valor maximo em 110 Hz
#raw.plot(duration=20, n_channels=3)#duracao da amostra de 150 s e mostra os 3 primeiros canais (EEG)


# #%% ==============================================plot a partir de vetor==============================================

#extraindo os eventos
extras=raw._raw_extras
event=extras[0]['events']
posicao=event[1]/250#tempo inicial do evento
tipo=event[2]#tipo de evento (segue a tabela)
duracao=event[4]/250#duracao do evento

n_time_samps = raw.n_times
time_secs = raw.times#tempo de aquisicao
ch_names = raw.ch_names#nome dos canais
sampling_freq = raw.info['sfreq']#frequencia da amostra

n=0
for p in range(len(posicao)):
    if tipo[p]==769 or tipo[p]==770:
        n+=1

#variaveis para extrassao do sinal
inicio=np.zeros(n)
fim=np.zeros(n)
tag=['']*n



i=0
for p in range(len(posicao)):
    if tipo[p]==769:
        tag[i]='esquerda'
        inicio[i]=posicao[p]
        fim[i]=posicao[p]+4
        
    if tipo[p]==770:
        tag[i]='direita'
        inicio[i]=posicao[p]
        fim[i]=posicao[p]+4
        
    if tipo[p]==769 or tipo[p]==770:
        i+=1

#4 segundos a 250 Hz=1000 amostras
x=np.zeros((n,4*250))#matriz de estado x tempo
y=np.zeros((n,4*250,3))#matriz de estado x amplitude x canal
#separa o dataset em varias amostras
for i in range(i):
    start_stop_seconds = np.array([inicio[i], fim[i]])#tempo inicial e final
    start_sample, stop_sample = (start_stop_seconds * sampling_freq).astype(int)
    megs_chans = raw[ch_names[0:3], start_sample:stop_sample]#pega os tres primeiros canais entre os intantes definidos
    x[i] = megs_chans[1]#tempo
    y[i] = megs_chans[0].T#matriz dos vetores
#valida o grafico dessas amostras
for i in range(2):
    X=x[i,:]
    Y=y[i,:,:]
    lines = plt.plot(X, Y)#plota
    plt.legend(lines, ch_names)
    plt.grid()
    plt.figure()


#plota o grafico no estado teste desejado
# teste=1
# start_stop_seconds = np.array([inicio[teste], fim[teste]])#tempo inicial e final
# start_sample, stop_sample = (start_stop_seconds * sampling_freq).astype(int)
# megs_chans = raw[ch_names[0:3], start_sample:stop_sample]#pega os tres primeiros canais entre os intantes definidos
# y_offset = np.array([6e-5,3e-5, 0])  #cria um offset para separar os canais
# x = megs_chans[1]#tempo
# y = megs_chans[0].T + y_offset#matriz dos vetores
# lines = plt.plot(x, y)#plota
# plt.legend(lines, ch_names)
# plt.grid()
# plt.title(tag[teste])

#AbrirEEG()