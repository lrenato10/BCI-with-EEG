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
    def __init__(self,ID=9,N=1):#abre o primeiro dataset por default
        #raw=mne.io.read_raw_gdf('DataSet/BCICIV_2b_gdf/B0101T.gdf')
        adress='DataSet/BCICIV_2b_gdf/B0'+str(ID)+'0'+str(N)+'T.gdf'
        #adress='D:\Engenharia\Python\IB1 EEG\EEG\SVM\DataSet\BCICIV_2b_gdf'+str(ID)+'0'+str(N)+'T.gdf'
        #print(adress)
        raw=mne.io.read_raw_gdf(adress)
        raw.info['bads'] = ['EOG:ch01','EOG:ch02','EOG:ch03']#retira os sinais EOG
        #print(raw)
        #print(raw.info)
        # #%% ==============================================Extraindo Dados EEG==============================================
        
        temp_amostra=4#tempo em que o sinal sera extraido por tentativa
        
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
                #self.inicio[i]=posicao[p]+(4-temp_amostra)#inicio partindo do fim da imaginacao motora
                #self.fim[i]=posicao[p]+4#fim da imaginacao motora
                self.inicio[i]=posicao[p]#inicio partindo do fim da imaginacao motora
                self.fim[i]=posicao[p]+temp_amostra#fim da imaginacao motora
                i+=1
                
            if tipo[p]==770 and ant!=1023:#mao direita eliminando as rejeitadas
                self.label_str[i]='direita'
                self.label[i]=1
                #self.inicio[i]=posicao[p]+(4-temp_amostra)#inicio partindo do fim da imaginacao motora
                #self.fim[i]=posicao[p]+4#fim da imaginacao motora
                self.inicio[i]=posicao[p]#inicio partindo do fim da imaginacao motora
                self.fim[i]=posicao[p]+temp_amostra#fim da imaginacao motora
                i+=1
        
        #tmepo da amostra [s] a 250 Hz (250 amostras por segundo)
        N=temp_amostra*250
        self.x=np.zeros((self.n,N))#matriz de estado x tempo
        self.y=np.zeros((self.n,N,3))#matriz de estado x amplitude x canal
        self.E=np.zeros((self.n,3))
        #separa o dataset em varias amostras
        for i in range(i):
            start_stop_seconds = np.array([self.inicio[i], self.fim[i]])#tempo inicial e final
            start_sample, stop_sample = (start_stop_seconds * sampling_freq).astype(int)
            megs_chans = raw[ch_names[0:3], start_sample:stop_sample]#pega os tres primeiros canais entre os intantes definidos
            self.x[i] = megs_chans[1]#tempo
            self.y[i] = megs_chans[0].T#matriz dos vetores
        #calculo da energia
        dt=1/250;#tempo discreto
        self.PSD=np.zeros((N,3))
        self.bandas=np.zeros((self.n,9))
        self.teta=np.zeros((self.n,3))
        self.alfa=np.zeros((self.n,3))
        self.delta=np.zeros((self.n,3))
        self.beta=np.zeros((self.n,3))
        self.gamma=np.zeros((self.n,3))
        for i in range(self.n):#percorre todas as tentativas
            self.X=self.x[i,:]#tempo
            self.Y=self.y[i,:,:]#eletrodo c3 cz c4
            for j in range(3):# percorre os 3 eletrodos C3 CZ C4
                self.fhat=np.fft.fft(self.Y[:,j],N)#calcula a FFT (numero imaginario da amplitude e fase dos sin)
                self.PSD[:,j]=self.fhat*np.conj(self.fhat)/N#calcula a densidade espectral
                self.freq=(1/(temp_amostra))*np.arange(N)#calcula as frequencias dos sin
                L=np.arange(1,np.floor(N/5),dtype='int')#pega metade das frequencias mais baixas
                for k in range(temp_amostra*250):
                    if (self.freq[k]>0.5) and (self.freq[k]<4):#delta
                        self.delta[i,:]=self.delta[i,:]+self.PSD[k,:]
                    if (self.freq[k]>=4) and (self.freq[k]<8):#teta
                        self.teta[i,:]=self.teta[i,:]+self.PSD[k,:]
                    if (self.freq[k]>=8) and (self.freq[k] <14):#alfa
                        self.alfa[i,:]=self.alfa[i,:]+self.PSD[k,:]
                    if (self.freq[k]>=14) and (self.freq[k] <30):#beta
                        self.beta[i,:]=self.beta[i,:]+self.PSD[k,:]
                    if (self.freq[k]>=30) and (self.freq[k]<100):#gamma
                        self.gamma[i,:]=self.gamma[i,:]+self.PSD[k,:]
                #plt.plot(self.freq[L],self.PSD[L,j])
                #plt.xlim(self.freq[L[0]],self.freq[L[-1]])
        self.bandas=np.concatenate((self.delta,self.teta, self.alfa,self.beta, self.gamma), axis=1)#concatena na horizontal
            
            
            
            #Y2=self.Y**2#amplitude ao quadrado do sinal dos eletodos
        #     for t in range(len(Y2)):#integra no tempo
        #         self.E[i][0]=self.E[i][0]+Y2[t][0]*(1/250)#energia C3
        #         self.E[i][1]=self.E[i][1]+Y2[t][1]*(1/250)#energia CZ
        #         self.E[i][2]=self.E[i][2]+Y2[t][2]*(1/250)#energia C4
        
        # self.EC_3Z4=np.array(self.E).flatten()
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