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
from collections import Counter

class DataSetEEG_sem_EOG():
    def __init__(self,ID=4,N=1):#abre o primeiro dataset por default
        #raw=mne.io.read_raw_gdf('DataSet/BCICIV_2b_gdf/B0101T.gdf')
        #adress='DataSet/BCICIV_2b_gdf/B0'+str(ID)+'0'+str(N)+'T.gdf'
        adress='D:\Engenharia\Python\IB1 EEG\EEG\Classificador\DataSet\BCICIV_2b_gdf\B0'+str(ID)+'0'+str(N)+'T.gdf'
        #print(adress)
        raw=mne.io.read_raw_gdf(adress)
        #raw.info['bads'] = ['EOG:ch01','EOG:ch02','EOG:ch03']#retira os sinais EOG
        #print(raw)
        #print(raw.info)
        # #%% ==============================================Extraindo Dados EEG==============================================
        
        self.temp_amostra=2#tempo em que o sinal sera extraido por tentativa
        
        #extraindo os eventos
        extras=raw._raw_extras
        event=extras[0]['events']
        posicao=event[1]/250#tempo inicial do evento
        tipo=event[2]#tipo de evento (segue a tabela)
        #print(Counter(tipo))#print a quantidade de cada flag
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
        self.inicioEOG=np.zeros(6)
        self.fimEOG=np.zeros(6)
        self.label=np.zeros(self.n)
        self.label_str=['']*self.n
        
        
        i=0
        eog=0
        for p in range(len(posicao)):
            
            #DADOS PARA REGRESSSAO DO EOG
            if ID!=1:#so o ondividuo 1 nao tem a balibração
                if (tipo[p]==276 or tipo[p]==277):#olhos abertos ou fechados
                    #self.inicio[i]=posicao[p]+(4-self.temp_amostra)#inicio partindo do fim da imaginacao motora
                    #self.fim[i]=posicao[p]+4#fim da imaginacao motora
                    self.inicioEOG[eog]=posicao[p]+0.0#inicio partindo do fim da imaginacao motora
                    self.fimEOG[eog]=posicao[p]+60#fim da imaginacao motora
                    eog+=1
                    
                if (tipo[p]==1077 or tipo[p]==1078 or tipo[p]==1079 or tipo[p]==1081):#olhos em movimento
                    #self.inicio[i]=posicao[p]+(4-self.temp_amostra)#inicio partindo do fim da imaginacao motora
                    #self.fim[i]=posicao[p]+4#fim da imaginacao motora
                    self.inicioEOG[eog]=posicao[p]+0.0#inicio partindo do fim da imaginacao motora
                    self.fimEOG[eog]=posicao[p]+15#fim da imaginacao motor
                    eog+=1
            
            #DADOS PARA TREINAMENTO E VALIDACAO DA IA COM EEG
            ant=tipo[p-1]
            
        
            if tipo[p]==769 and ant!=1023:#mao esquerda eliminando as rejeitadas
                self.label_str[i]='esquerda'
                self.label[i]=0
                #self.inicio[i]=posicao[p]+(4-self.temp_amostra)#inicio partindo do fim da imaginacao motora
                #self.fim[i]=posicao[p]+4#fim da imaginacao motora
                self.inicio[i]=posicao[p]+0.5#inicio partindo do fim da imaginacao motora
                self.fim[i]=posicao[p]+self.temp_amostra+0.5#fim da imaginacao motora
                i+=1
                
            if tipo[p]==770 and ant!=1023:#mao direita eliminando as rejeitadas
                self.label_str[i]='direita'
                self.label[i]=1
                #self.inicio[i]=posicao[p]+(4-self.temp_amostra)#inicio partindo do fim da imaginacao motora
                #self.fim[i]=posicao[p]+4#fim da imaginacao motora
                self.inicio[i]=posicao[p]+0.5#inicio partindo do fim da imaginacao motora
                self.fim[i]=posicao[p]+self.temp_amostra+0.5#fim da imaginacao motora
                i+=1
        
        #tmepo da amostra [s] a 250 Hz (250 amostras por segundo)
        N=self.temp_amostra*250
        self.x=np.zeros((self.n,N))#matriz de estado x tempo
        self.y=np.zeros((self.n,N,3))#matriz de estado x amplitude x canal
        self.y_eeg_sem_EOG=np.zeros((self.n,N,3))
        self.E=np.zeros((self.n,3))
        self.y_eog=np.zeros((self.n,N,3))
        self.y_eog_bip=np.zeros((self.n,N,2))
        
        
        self.x_EOG=np.zeros((0))#matriz de estado x tempo
        self.y_EOG=np.zeros((0,3))#matriz de estado x amplitude x canal
        self.y_eog_EOG=np.zeros((0,3))
        
        #separa o dataset em varias amostras
        #DADOS DE TREINAMENTO EEG
        for i in range(i):
            start_stop_seconds = np.array([self.inicio[i], self.fim[i]])#tempo inicial e final
            start_sample, stop_sample = (start_stop_seconds * sampling_freq).astype(int)
            megs_chans = raw[ch_names[0:3], start_sample:stop_sample]#pega os tres primeiros canais entre os intantes definidos (EEG)
            self.x[i] = megs_chans[1]#tempo
            self.y[i] = megs_chans[0].T#matriz dos vetores EEG
            
            if ID!=1:
                eog_chans= raw[ch_names[3:6], start_sample:stop_sample]#pega os tres ultimos canais (EOG)
                self.y_eog[i]=eog_chans[0].T#matriz dos vetores EOG
        
        #DADOS PARA CALIBRACAO EOG
        for eog in range(eog):
            start_stop_seconds = np.array([self.inicioEOG[eog], self.fimEOG[eog]])#tempo inicial e final
            start_sample, stop_sample = (start_stop_seconds * sampling_freq).astype(int)
            megs_chans_EOG = raw[ch_names[0:3], start_sample:stop_sample]#pega os tres primeiros canais entre os intantes definidos (EEG)
            
            if ID!=1:
                eog_chans_EOG= raw[ch_names[3:6], start_sample:stop_sample]#pega os tres ultimos canais (EOG)
                self.x_EOG=np.concatenate((self.x_EOG, megs_chans_EOG[1]), axis=0)#concatena na vertical
                self.y_EOG=np.concatenate((self.y_EOG, megs_chans_EOG[0].T), axis=0)#concatena na vertical
                self.y_eog_EOG=np.concatenate((self.y_eog_EOG, eog_chans_EOG[0].T), axis=0)#concatena na vertical
            #self.x_EOG[i] = megs_chans[1]#tempo
            #self.y_EOG[i] = megs_chans[0].T#matriz dos vetores EEG
            #self.y_eog_EOG[i]=eog_chans[0].T#matriz dos vetores EOG    
        
        if ID!=1:
            #converte para leitura bipolar
            bip = np.array([[1, -1, 0], [0, -1, 1]])#matriz que vai converter leitura do eletrodo monopolar em bipolar 
            self.y_eog_EOG_bip = (bip @ self.y_eog_EOG.T).T#converte para leitura bipolar
            for tentativa in range(self.n):
                self.y_eog_bip[tentativa,:,:] = (bip @ self.y_eog[tentativa,:,:].T).T#converte para leitura bipolar
            
            #calcula a matriz dos coeficientes da regressao
            #self.b_bip = np.linalg.solve(self.y_eog_EOG_bip.T @ self.y_eog_EOG_bip, self.y_eog_EOG_bip.T @ self.y_EOG)#coeficiente para bipolar
            self.b = np.linalg.solve(self.y_eog_EOG.T @ self.y_eog_EOG, self.y_eog_EOG.T @ self.y_EOG)#coeficiente para unipolar
            
            #CALCULA NOVO EEG sem o EOG
            for tentativa in range(self.n):
                #self.y_eeg_sem_EOG[tentativa,:,:]=(self.y[tentativa,:,:] - self.y_eog_bip[tentativa,:,:] @ self.b_bip)#EEG corrigido pelo EOG bipolar
                self.y_eeg_sem_EOG[tentativa,:,:]=(self.y[tentativa,:,:] - self.y_eog[tentativa,:,:] @ self.b)#EEG corrigido pelo EOG unipolar
        
        if ID==1:
            self.y_eeg_sem_EOG=self.y
        
        #calculo da energia
        dt=1/250;#tempo discreto
        self.sinal_alto=np.array([])
        self.count_alto=0
        self.PSD=np.zeros((N,3))
        self.bandas=np.zeros((self.n,9))
        self.teta=np.zeros((self.n,3))
        self.alfa=np.zeros((self.n,3))
        self.delta=np.zeros((self.n,3))
        self.beta=np.zeros((self.n,3))
        self.gamma=np.zeros((self.n,3))
        for i in range(self.n):#percorre todas as tentativas
            self.X=self.x[i,:]#tempo
            self.Y=self.y_eeg_sem_EOG[i,:,:]#eletrodo c3 cz c4 no tempo

            if np.max(np.abs(self.Y))>30e-6:#pega as tentativas com sinal com alto valor -> pode ser movimento ocular
                    self.sinal_alto=np.concatenate((self.sinal_alto, [i]), axis=0)#concatena na vertical
                    self.count_alto+=1
            for j in range(3):# percorre os 3 eletrodos C3 CZ C4
                self.fhat=np.fft.fft(self.Y[:,j],N)#calcula a FFT (numero imaginario da amplitude e fase dos sin)
                self.PSD[:,j]=self.fhat*np.conj(self.fhat)/N#calcula a densidade espectral
                self.freq=(1/(self.temp_amostra))*np.arange(N)#calcula as frequencias dos sin
                L=np.arange(1,np.floor(N/5),dtype='int')#pega metade das frequencias mais baixas
                for k in range(self.temp_amostra*250):
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
                
        self.bandas=np.concatenate((self.alfa,self.beta), axis=1)#concatena na horizontal
        
        #joga fora os sinais com valores elevados
        #self.bandas=np.delete(self.bandas,self.sinal_alto.astype(int),0)#retira os sinais com maiores valor
        #self.label=np.delete(self.label,self.sinal_alto.astype(int),0)#retira os sinais com maiores valor
        #self.y_eeg_sem_EOG=np.delete(self.y_eeg_sem_EOG,self.sinal_alto.astype(int),0)#retira os sinais com maiores valor
    
D=DataSetEEG_sem_EOG(2,1)