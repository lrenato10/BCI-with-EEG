# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 15:07:16 2020

@author: Luiz Renato
"""

import os
import numpy as np
import mne
import numpy as np
import matplotlib.pyplot as plt


raw=mne.io.read_raw_gdf('BCICIV_2b_gdf/B0101T.gdf')

raw.info['bads'] = ['EOG:ch01','EOG:ch02','EOG:ch03']#retira os sinais EOG
print(raw)
print(raw.info)

#=====================plot pronto=========================
#raw.plot_psd(fmax=110)#espectro de frequencia com valor maximo em 110 Hz
#raw.plot(duration=40, n_channels=3)#duracao da amostra de 150 s e mostra os 3 primeiros canais (EEG)




#======================plot a partir de vetor=====================
n_time_samps = raw.n_times
time_secs = raw.times#tempo de aquisicao
ch_names = raw.ch_names#nome dos canais


sampling_freq = raw.info['sfreq']#frequencia da amostra
start_stop_seconds = np.array([11, 13])#tempo inicial e final
start_sample, stop_sample = (start_stop_seconds * sampling_freq).astype(int)
two_meg_chans = raw[ch_names[0:3], start_sample:stop_sample]#pega os tres primeiros canais entre os intantes definidos
y_offset = np.array([5e-5,2e-5, 0])  #cria um offset para separar os canais
x = two_meg_chans[1]#tempo
y = two_meg_chans[0].T + y_offset#matriz dos vetores
lines = plt.plot(x, y)#plota
plt.legend(lines, ch_names)