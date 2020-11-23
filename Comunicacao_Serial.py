# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 08:14:27 2020

@author: Luiz Renato
"""

from tkinter import *
from tkinter import messagebox#para as caixas de mensagem
import serial
from threading import Thread 
import time
import numpy as np
from matplotlib import pyplot as plt
from Plot_Potenciometro import PlotPot


class Janela_Comunicacao_Serial():
    def __init__(self):
        self.cs=Tk()
        self.cs.title('Comunicação Serial')
        self.cs['bg'] = '#86cee4'
        self.cs.resizable(False, False)
        Label(self.cs,text='Informe a Porta:', font=('helvetica', 20),bg='#86cee4').grid(row=0,column=0)
        self.porta=Entry(self.cs,font=('helvetica',20),width=8)
        self.porta.grid(row=0,column=1,padx=20,pady=20)
        Button(self.cs,text='Iniciar Conexão',command=self.create_porta, font=('helvetica', 20),bg= '#f29cc2',fg='white').grid(row=1,column=0,columnspan=1,padx=20,pady=20)
        self.Estado_Conexao=Label(self.cs, text='Desconectado', font=('helvetica', 20), fg='red',bg= '#86cee4')
        self.Estado_Conexao.grid(row=1,column=1,columnspan=2,padx=20,pady=20)
        Button(self.cs,text='Ler Dados',command=self.IniciaLeitura, font=('helvetica', 20),bg='#f29cc2',fg='white').grid(row=2,column=0,columnspan=1,padx=20,pady=20)
        Button(self.cs,text='Encerrar Leitura',command=self.fim,font=('helvetica', 20),bg='#f29cc2',fg='white').grid(row=4,column=0,columnspan=2,padx=20,pady=20)
        self.Estado_Leitura=Label(self.cs, text='Clique em Ler', font=('helvetica', 20), fg='black',bg= '#86cee4'  )
        self.Estado_Leitura.grid(row=2,column=1,columnspan=1,padx=20,pady=20)
        Button(self.cs,text='Plotar EEG do uC',command=self.plotEEG,font=('helvetica', 20),bg='#f29cc2',fg='white').grid(row=5,column=0,columnspan=2,padx=20,pady=20)
        Label(self.cs, text='Sinal Potenciômetro:', font=('helvetica', 20), fg='black',bg= '#86cee4').grid(row=6,column=0,columnspan=1,padx=20,pady=20)
        self.Pot_Val=Label(self.cs, text='---', font=('helvetica', 20), fg='black',bg= '#86cee4')
        self.Pot_Val.grid(row=6,column=1,columnspan=1,padx=20,pady=20)
        
        #variaveis para leitura do sinal do EEG
        self.Vc3=np.zeros((0))#sinal eletrodo C3
        self.Vcz=np.zeros((0))#sinal eletrodo CZ
        self.Vc4=np.zeros((0))#sinal eletrodo C4
        self.pot=np.zeros((0))#sinal potenciometro
        self.resolucao=2**16-1#conversor AD de 16bits (ultimo valor 2^n-1)
        self.ganho=10e3#ganho do circuito do dataset
        self.cs.mainloop()

    def create_porta(self):
        try:
            global USB
            USB=serial.Serial(self.porta.get(),250000)#inicia a comunicacao serial com a porta selecionada e o baud rate em bits/s
            self.Estado_Conexao['text'] = 'Conectado'
            self.Estado_Conexao['fg']='green'
        except:
            messagebox.showinfo('Erro!', 'Erro na conexão ou no nome da porta')
    def Thread_Leitura(self):
        count=0
        while (self.threadrunning):#Loop da thread
            #print(count)
            while (USB.in_waiting):#Serial.available (verifica o numero de bytes no buffer)        
                self.Estado_Leitura['text'] = 'Lendo...'
                #faz apenas 1 leitura para verificar os 2 ifs
                self.SB=USB.read(1)
                self.SP=self.SB#n pode ler outro byte
                #print('IF---1')
                if (self.SB==b'S'):#Verifica start byte
                    #print(self.SB)
                    
                    #DADOS DO EEG
                    self.C3=USB.read(1)   
                    if (self.C3==b'3'):#Verifica byte do C3
                        #print(self.C3)
                        self.MSB=USB.read(1)#le o byte mais significativo
                        #print(self.MSB)
                        self.LSB=USB.read(1)#le o byte menos significativo
                        #print(self.LSB)
                        #transforma em um inteiro a partir de MSB e LSB -> int(MSB<<8+LSB)
                        int16=int.from_bytes(self.MSB+self.LSB,byteorder='big',signed=False)#inteiro de 16 bits positivo com byte mais significativo primeiro
                        int16A=(int16-((2**16)/2-1))*2
                        int16A=int16A/(self.resolucao*self.ganho)
                        self.Vc3=np.append(self.Vc3,int16A)#concatena em um vetor coluna
                        #print(int16A)
                    
                    self.CZ=USB.read(1)
                    if (self.CZ==b'Z'):#Verifica byte do CZ
                        #print(self.CZ)
                        self.MSB=USB.read(1)#le o byte mais significativo
                        #print(self.MSB)
                        self.LSB=USB.read(1)#le o byte menos significativo
                        #print(self.LSB)
                        #transforma em um inteiro a partir de MSB e LSB -> int(MSB<<8+LSB)
                        int16=int.from_bytes(self.MSB+self.LSB,byteorder='big',signed=False)#inteiro de 16 bits positivo com byte mais significativo primeiro
                        int16A=(int16-((2**16)/2-1))*2
                        int16A=int16A/(self.resolucao*self.ganho)
                        self.Vcz=np.append(self.Vcz,int16A)#concatena em um vetor coluna
                        #print(int16A)
                    
                    self.C4=USB.read(1)
                    if (self.C4==b'4'):#Verifica byte do C4
                        #print(self.C4)
                        self.MSB=USB.read(1)#le o byte mais significativo
                        #print(self.MSB)
                        self.LSB=USB.read(1)#le o byte menos significativo
                        #print(self.LSB)
                        #transforma em um inteiro a partir de MSB e LSB -> int(MSB<<8+LSB)
                        int16=int.from_bytes(self.MSB+self.LSB,byteorder='big',signed=False)#inteiro de 16 bits positivo com byte mais significativo primeiro
                        int16A=(int16-((2**16)/2-1))*2
                        int16A=int16A/(self.resolucao*self.ganho)
                        self.Vc4=np.append(self.Vc4,int16A)#concatena em um vetor coluna
                        #print(int16A)
                    
                    self.EB=USB.read(1)
                    if(self.EB != b'E'):#byte final de verificacao
                        messagebox.showinfo('Perda de dado EEG!')    
                        print('Perda de dado EEG!')
                        self.threadrunning=False
                
                #print('IF---2')
                #DADOS DO POTENCIOMETRO
                if (self.SP==b'P'):#Verifica start byte
                    self.MSB=USB.read(1)#le o byte mais significativo
                    #print(self.MSB)
                    self.LSB=USB.read(1)#le o byte menos significativo
                    #print(self.LSB)
                    #transforma em um inteiro a partir de MSB e LSB -> int(MSB<<8+LSB)
                    int16=int.from_bytes(self.MSB+self.LSB,byteorder='big',signed=False)#inteiro de 16 bits positivo com byte mais significativo primeiro
                    self.pot=np.append(self.pot,int16)#concatena em um vetor coluna
                    #print(int16)
                    self.Pot_Val['text']=f'{int16}'
                    self.EP=USB.read(1)
                    if(self.EP != b'F'):#byte final de verificacao
                        messagebox.showinfo('Perda de dado POT!')  
                        print('Perda de dado POT!')
                        self.threadrunning=False
            count+=1

        print(count)
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
        self.Estado_Leitura['text'] = 'Encerrado'
        
    def plotEEG(self):        
        fig, axs = plt.subplots(3, 1, figsize=(16, 6))#cria um plot com 5 colunas de imagem
        fig.subplots_adjust(left=0.0625, right=0.95, wspace=0.1)
        PC3=axs[0].plot(np.arange(0,1,1/250),self.Vc3 , lw =2.0 , color="green", label = "C3")
        axs[0].set_title('C3')
        axs[0].set_xlabel('Tempo [s]')
        axs[0].set_ylabel('Tensão [V]')
        axs[0].grid()
        PCZ=axs[1].plot(np.arange(0,1,1/250),self.Vcz , lw =2.0 , color="red", label = "CZ")
        axs[1].set_title('CZ')
        axs[1].set_xlabel('Tempo [s]')
        axs[1].set_ylabel('Tensão [V]')
        axs[1].grid()
        PC4=axs[2].plot(np.arange(0,1,1/250),self.Vc4 , lw =2.0 , color="blue", label = "C4")
        axs[2].set_title('C4')
        axs[2].set_xlabel('Tempo [s]')
        axs[2].set_ylabel('Tensão [V]')
        axs[2].grid()
        
        #axs.legend((PC3,PCZ,PC4),('Eletrodo C3','Eletrodo CZ','Eletrodo C4'))
    
    def Potenciometro(self):
        PlotPot(self.cs,self)
        


     
