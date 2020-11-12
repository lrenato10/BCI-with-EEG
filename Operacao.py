from tkinter import*#para toda a interface grafica
import tk_tools
from gerargif import ImageLabel
from open_dataset import AbrirEEG
from threading import Thread 
import random
import time
from SVM.Extraindo_Amostras_EEG import DataSetEEG
from SVM.BigDataSetEEG import ConcatenateDataSetEEG 

class Janela_Operacao():
    def __init__(self): 
        self.operacao = Toplevel()  # é uma instancia de tk se a janela root for fechada ela tambpem será fechada
        self.operacao.resizable(False, False) # ampliar a janela
        self.operacao.title('Operação')
        self.operacao['bg'] = '#86cee4'
        #GIF do movimento
        self.gif_mov = ImageLabel(self.operacao)
        self.gif_mov.grid(row=0, column=0)
        self.gif_mov.load('Imagens/esquerda.gif',10**8)
        self.Lesquerda=Label(self.operacao, text='Movimento Real',font=('helvetica',20),fg='black',bg= '#86cee4'  )
        self.Lesquerda.grid(row=1, column=0, columnspan=1, padx=10,pady=10)# posiciona leganda
        #GIF da predicao
        self.gif_pred = ImageLabel(self.operacao)
        self.gif_pred.grid(row=2, column=0)
        self.gif_pred.load('Imagens/direita.gif',10**8)
        self.Ldireita=Label(self.operacao, text='Predição do Movimento',font=('helvetica',20),fg='black',bg= '#86cee4'  )
        self.Ldireita.grid(row=3, column=0, columnspan=1, padx=10,pady=10)# posiciona leganda
                
        #w = Canvas(self.operacao, width=200, height=100)
        #w.grid(row=4,column=0)
        led =tk_tools.Led(self.operacao, size=50)
        led.grid(row=5,column=0)
        led.to_red()
        led.to_green(on=True)
        led.to_red(on=True)
        
        #self.Data_Label
        #self.Data_bandas
