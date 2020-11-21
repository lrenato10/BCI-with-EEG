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

#https://rosettacode.org/wiki/Decimal_floating_point_number_to_binary#Python
hex2bin = dict('{:x} {:04b}'.format(x,x).split() for x in range(16))
bin2hex = dict('{:b} {:x}'.format(x,x).split() for x in range(16))
 
def float_dec2bin(d):
    neg = False
    if d < 0:
        d = -d
        neg = True
    hx = float(d).hex()
    p = hx.index('p')
    bn = ''.join(hex2bin.get(char, char) for char in hx[2:p])
    return (('-' if neg else '') + bn.strip('0') + hx[p:p+2]
            + bin(int(hx[p+2:]))[2:])
 
def float_bin2dec(bn):
    neg = False
    if bn[0] == '-':
        bn = bn[1:]
        neg = True
    dp = bn.index('.')
    extra0 = '0' * (4 - (dp % 4))
    bn2 = extra0 + bn
    dp = bn2.index('.')
    p = bn2.index('p')
    hx = ''.join(bin2hex.get(bn2[i:min(i+4, p)].lstrip('0'), bn2[i])
                 for i in range(0, dp+1, 4))
    bn3 = bn2[dp+1:p]
    extra0 = '0' * (4 - (len(bn3) % 4))
    bn4 = bn3 + extra0
    hx += ''.join(bin2hex.get(bn4[i:i+4].lstrip('0'))
                  for i in range(0, len(bn4), 4))
    hx = (('-' if neg else '') + '0x' + hx + bn2[p:p+2]
          + str(int('0b' + bn2[p+2:], 2)))
    return float.fromhex(hx)


EEG=ConcatenateDataSetEEG(1,1)#importa o dataset do(primeiro sujeito, ultimo sujeito)
Signal=EEG.EEG_Signal
SignalTentativa=Signal[0,:,0]
SignalTentativa16=SignalTentativa.astype(np.float16)
signalBin=list(str(' ')*len(SignalTentativa))
signalFloat=np.zeros(len(SignalTentativa))

for i in range(len(SignalTentativa)):
    signalBin[i]=float_dec2bin(SignalTentativa16[i])
    signalFloat[i]=float_bin2dec(signalBin[i])

#n64=np.array(1.234)
#n16=n64.astype(np.float16)
#a=float_dec2bin(n16)
