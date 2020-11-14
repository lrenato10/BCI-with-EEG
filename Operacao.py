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
    def __init__(self,SVM): 
        self.SVM=SVM
        self.operacao = Toplevel()  # é uma instancia de tk se a janela root for fechada ela tambpem será fechada
        #self.operacao.resizable(False, False) # ampliar a janela
        self.operacao.title('Operação')
        self.operacao['bg'] = '#86cee4'
        #GIF do movimento
        self.gif_mov = ImageLabel(self.operacao)
        self.gif_mov.grid(row=0, column=0, columnspan=1)
        self.gif_mov.load('Imagens/esquerda.gif',10**8)
        self.Lesquerda=Label(self.operacao, text='Movimento Real',font=('helvetica',20),fg='black',bg= '#86cee4'  )
        self.Lesquerda.grid(row=1, column=0, columnspan=1, padx=10,pady=10)# posiciona leganda
        #GIF da predicao
        self.gif_pred = ImageLabel(self.operacao)
        self.gif_pred.grid(row=2, column=0,columnspan=1)
        self.gif_pred.load('Imagens/direita.gif',10**8)
        self.Ldireita=Label(self.operacao, text='Predição do Movimento',font=('helvetica',20),fg='black',bg= '#86cee4'  )
        self.Ldireita.grid(row=3, column=0, columnspan=1, padx=10,pady=10)# posiciona leganda
         
        
        
        Button(self.operacao, text='Iniciar', width=20, bg='#f29cc2',fg='white',command=self.IniciarPredicao).grid(row=0, column=1,columnspan=1,padx=10,pady=10)
        Button(self.operacao, text='Parar', width=20, bg='#f29cc2',fg='white',command=self.PararPredicao).grid(row=1, column=1,columnspan=1,padx=10,pady=10)
        
        self.led =tk_tools.Led(self.operacao, size=100)
        self.led.grid(row=2,column=1, columnspan=2)
        self.led.to_red()
        self.led.to_green(on=False)
        self.led.to_red(on=False)
        
        self.Acertos=Label(self.operacao, text='Taxa de Acerto: 0/0',font=('helvetica',20),fg='black',bg= '#86cee4'  )#contador de acertos
        self.Acertos.grid(row=3, column=1, columnspan=1, padx=10,pady=10)# posiciona contador de acertos
        
        
        self.SVM.treinar()
        
    def Thread_Predicao(self):
        count=0
        acertos=0
        while (count<len(self.SVM.Y_test) and self.threadrunning):#roda o gif 120 vezes
            #amostra=random.randint(0,len(self.SVM.Y_test)-1)#pega uma amostra aleatoria de validacao
            self.SVM.predizer([self.SVM.X_test[count,:]])
            predicao=self.SVM.Y_predict
            print(predicao)
            real=self.SVM.Y_test[count]
            print(real)
            if (real==0):#mao esquerda
                self.gif_mov.load('Imagens/esquerda.gif',100)
            if (real==1):#mao direita
                self.gif_mov.load('Imagens/direita.gif',100)
            time.sleep(1)#atraso entre o movimento e a predicao
            
            if (predicao==0):#mao esquerda
                self.gif_pred.load('Imagens/esquerda.gif',100)
            if (predicao==1):#mao direita
                self.gif_pred.load('Imagens/direita.gif',100)

            if (predicao==real):
                self.led.to_green(on=True)
                acertos+=1
            else:
                self.led.to_red(on=True)
                
                
            count+=1
            self.Acertos['text']='Taxa de Acerto: {}/{}'.format(acertos,count)
            time.sleep(4)#tempo para imaginacao motora
            time.sleep(1.5+random.random())
    
    def IniciarPredicao(self):
        self.threadrunning=True
        self.t=Thread(target=self.Thread_Predicao)
        self.t.start()
    
    def PararPredicao(self):
        self.threadrunning=False
        
        #self.Data_Label
        #self.Data_bandas
