# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 08:14:27 2020

@author: Luiz Renato
"""

from tkinter import *
import serial
from threading import Thread 
import time
import numpy as np


class Comunicacao_Serial():
    def __init__(self):
        self.cs=Tk()
        Label(self.cs,text='Informe a Porta:', font=('helvetica', 20)).grid(row=0,column=0)
        self.porta=Entry(self.cs)
        self.porta.grid(row=0,column=1)
        Button(self.cs,text='Iniciar Conexão',command=self.create_porta, font=('helvetica', 20)).grid(row=1,column=0,columnspan=1)
        self.Estado_Conexao=Label(self.cs, text='Desconectado', font=('helvetica', 20), fg='black',bg= '#f29cc2'  )
        self.Estado_Conexao.grid(row=1,column=1,columnspan=2)
        Button(self.cs,text='Ler',command=self.IniciaLeitura, font=('helvetica', 20)).grid(row=2,column=0,columnspan=1)
        Button(self.cs,text='Encerrar',command=self.fim,font=('helvetica', 20)).grid(row=4,column=0,columnspan=2)
        self.Estado_Leitura=Label(self.cs, text='Clique em Ler', font=('helvetica', 20), fg='black',bg= '#f29cc2'  )
        self.Estado_Leitura.grid(row=2,column=1,columnspan=1)
        self.Vc3=np.zeros((0))
        self.Vcz=np.zeros((0))
        self.Vc4=np.zeros((0))
        self.resolucao=2**16-1#conversor AD de 16bits (ultimo valor 2^n-1)
        self.ganho=10e3#ganho do circuito do dataset
        self.cs.mainloop()

    def create_porta(self):
        global USB
        USB=serial.Serial(self.porta.get(),9600)#inicia a comunicacao serial com a porta selecionada e o baud rate em bits/s
        self.Estado_Conexao['text'] = 'Conectado'
    
    def Thread_Leitura(self):
        count=0
        while (USB.in_waiting and self.threadrunning):#Serial.available (verifica o numero de bytes no buffer)
            self.Estado_Leitura['text'] = 'Lendo...'
            self.SB=USB.read(1)
            if (self.SB==b'S'):#Verifica start byte
                print(self.SB)
                
                self.C3=USB.read(1)   
                if (self.C3==b'3'):#Verifica byte do C3
                    print(self.C3)
                    self.MSB=USB.read(1)#le o byte mais significativo
                    #print(self.MSB)
                    self.LSB=USB.read(1)#le o byte menos significativo
                    #print(self.LSB)
                    #transforma em um inteiro a partir de MSB e LSB -> int(MSB<<8+LSB)
                    int16=int.from_bytes(self.MSB+self.LSB,byteorder='big',signed=False)#inteiro de 16 bits positivo com byte mais significativo primeiro
                    int16A=(int16-((2**16)/2-1))*2
                    int16A=int16A/(self.resolucao*self.ganho)
                    self.Vc3=np.append(self.Vc3,int16A)#concatena em um vetor coluna
                    print(int16A)
                
                self.CZ=USB.read(1)
                if (self.CZ==b'Z'):#Verifica byte do CZ
                    print(self.CZ)
                    self.MSB=USB.read(1)#le o byte mais significativo
                    #print(self.MSB)
                    self.LSB=USB.read(1)#le o byte menos significativo
                    #print(self.LSB)
                    #transforma em um inteiro a partir de MSB e LSB -> int(MSB<<8+LSB)
                    int16=int.from_bytes(self.MSB+self.LSB,byteorder='big',signed=False)#inteiro de 16 bits positivo com byte mais significativo primeiro
                    int16A=(int16-((2**16)/2-1))*2
                    int16A=int16A/(self.resolucao*self.ganho)
                    self.Vcz=np.append(self.Vcz,int16A)#concatena em um vetor coluna
                    print(int16A)
                
                self.C4=USB.read(1)
                if (self.C4==b'4'):#Verifica byte do C4
                    print(self.C4)
                    self.MSB=USB.read(1)#le o byte mais significativo
                    #print(self.MSB)
                    self.LSB=USB.read(1)#le o byte menos significativo
                    #print(self.LSB)
                    #transforma em um inteiro a partir de MSB e LSB -> int(MSB<<8+LSB)
                    int16=int.from_bytes(self.MSB+self.LSB,byteorder='big',signed=False)#inteiro de 16 bits positivo com byte mais significativo primeiro
                    int16A=(int16-((2**16)/2-1))*2
                    int16A=int16A/(self.resolucao*self.ganho)
                    self.Vc4=np.append(self.Vc4,int16A)#concatena em um vetor coluna
                    print(int16A)
                
                self.EB=USB.read(1)
                if(self.EB != b'E'):
                    print('Perda de dado!')
                    self.threadrunning=False
                
                
            time.sleep(1/250)#250 Hz
        self.Estado_Leitura['text'] = 'Fim dos Dados'
    
    def IniciaLeitura(self):
        self.threadrunning=True
        self.t=Thread(target=self.Thread_Leitura)
        self.t.start()
    
    def ParaLeitura(self):
        self.threadrunning=False
    
    def fim(self):
        self.ParaLeitura()
        USB.close()
        print('fim')
        
        
abrir=Comunicacao_Serial()
    

