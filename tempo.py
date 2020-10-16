# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 18:53:25 2020

@author: Luiz Renato
"""
import time

tempo_inicial=time.time()#tempo inicial
tempo=time.time()
while(time.time()-tempo_inicial<=10.1):
    if((time.time()-tempo)>=1):#incremento de tempo
            print(time.time()-tempo_inicial)
            print(int(time.time()-tempo_inicial))
            tempo=time.time()        
