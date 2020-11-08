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

class DataSetEEG():
    def __init__(self):
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
        
        self.n=0
        for p in range(len(posicao)):
            ant=tipo[p-1]
            if (tipo[p]==769 or tipo[p]==770) and ant!=1023:#mao direita ou esquerda eliminando as rejeitadas
                self.n+=1
        
        r=0
        for p in range(len(posicao)):
            if tipo[p]==1023:#tentativas rejeitadas
                r+=1
        
        #variaveis para extrassao do sinal
        self.inicio=np.zeros(self.n)
        self.fim=np.zeros(self.n)
        self.label=np.zeros(self.n)
        self.label_str=['']*self.n
        
        
        i=0
        for p in range(len(posicao)):
            ant=tipo[p-1]
            if tipo[p]==769 and ant!=1023:#mao esquerda eliminando as rejeitadas
                self.label_str[i]='esquerda'
                self.label[i]=0
                self.inicio[i]=posicao[p]
                self.fim[i]=posicao[p]+4
                i+=1
                
            if tipo[p]==770 and ant!=1023:#mao direita eliminando as rejeitadas
                self.label_str[i]='direita'
                self.label[i]=1
                self.inicio[i]=posicao[p]
                self.fim[i]=posicao[p]+4
                i+=1
        
        #4 segundos a 250 Hz=1000 amostras
        self.x=np.zeros((self.n,4*250))#matriz de estado x tempo
        self.y=np.zeros((self.n,4*250,3))#matriz de estado x amplitude x canal
        self.E=np.zeros((self.n,3))
        #separa o dataset em varias amostras
        for i in range(i):
            start_stop_seconds = np.array([self.inicio[i], self.fim[i]])#tempo inicial e final
            start_sample, stop_sample = (start_stop_seconds * sampling_freq).astype(int)
            megs_chans = raw[ch_names[0:3], start_sample:stop_sample]#pega os tres primeiros canais entre os intantes definidos
            self.x[i] = megs_chans[1]#tempo
            self.y[i] = megs_chans[0].T#matriz dos vetores
        #calculo da energia
        for i in range(self.n):
            self.X=self.x[i,:]#tempo
            self.Y=self.y[i,:,:]#eletrodo c3 cz c4
            Y2=self.Y**2#amplitude ao quadrado do sinal dos eletodos
            
            for t in range(len(Y2)):#integra no tempo
                self.E[i][0]=self.E[i][0]+Y2[t][0]*(1/250)#energia C3
                self.E[i][1]=self.E[i][1]+Y2[t][1]*(1/250)#energia CZ
                self.E[i][2]=self.E[i][2]+Y2[t][2]*(1/250)#energia C4
        
        self.EC_3Z4=np.array(self.E).flatten()
            #olha o grafico dos 3 canais sobrepostos
            #plt.figure()
            #lines = plt.plot(X, Y)#plota
            #plt.legend(lines, ch_names)
            #plt.grid()
        
        
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
        # plt.title(label_str[teste])

#D=DataSetEEG()