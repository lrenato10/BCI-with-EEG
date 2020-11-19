from tkinter import*#para toda a interface grafica
import tk_tools
from gerargif import ImageLabel
from open_dataset import AbrirEEG
from threading import Thread 
import random
import time
from SVM.Extraindo_Amostras_EEG import DataSetEEG
from SVM.BigDataSetEEG import ConcatenateDataSetEEG 
import matplotlib.pyplot as plt
from Real_time_plot import StripChart

class Janela_Operacao():
    def __init__(self,classifier): 
        self.classifier=classifier
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
        
        Button(self.operacao, text='Abrir EEG', width=20, bg='#f29cc2',fg='white',command=self.IniciarEEG).grid(row=4, column=0,columnspan=2,padx=10,pady=10)
        
        self.classifier.treinar()
        
    def Thread_Predicao(self):
        count=0
        acertos=0
        while (count<len(self.classifier.Y_test) and self.threadrunning_gif):#roda o gif 120 vezes
            #amostra=random.randint(0,len(self.classifier.Y_test)-1)#pega uma amostra aleatoria de validacao
            self.classifier.predizer([self.classifier.X_test[count,:]])#prediz o dado de teste para o tentativa count
            predicao=self.classifier.Y_predict
            print(predicao)
            real=self.classifier.Y_test[count]
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
        self.threadrunning_gif=True
        self.tgif=Thread(target=self.Thread_Predicao)
        self.tgif.start()
    
    def PararPredicao(self):
        self.threadrunning=False
        
        #self.Data_Label
        #self.Data_bandas
    
    def IniciarEEG(self):
        self.EEG = Toplevel()
        StripChart(self.EEG,self.classifier.Signal,self.classifier.indices_test)
        
    
    # def Thread_EEG(self):
    #     while self.threadrunning_EEG:
    #         fig=plt.figure()
    #         fc3=fig.add_subplot(1,1,1)
    #         #fcz=fig.add_subplot(2,1,2)
    #         #fc4=fig.add_subplot(3,1,3)
    #         fig.show()
    #         i=0
    #         t,c3,cz,c4=[],[],[],[]
    #         while True:#self.threadrunning_EEG:
    #             t.append(i/250)#tempo
    #             #print(t)
    #             c3.append(self.SVM.Signal[0,i,0])#sinal eletrodo c3
    #             #print(c3)
    #             #cz.append(SVM[0,i,0])
    #             #c4.append(SVM[0,i,0])
    #             fc3.plot(t,c3,color='b')
    #             #fig.canvas.draw()
    #             fig.canvas.draw_idle()
    #             fc3.set_xlim(left=max(0,i-1000),right=i+100)
    #             time.sleep(0.1)
    #             i=i+1
            
    # def IniciarEEG(self):
    #     self.threadrunning_EEG=True
    #     self.tEEG=Thread(target=self.Thread_EEG)
    #     self.tEEG.start()
    
    # def PararEEG(self):
    #     self.threadrunning_EEG=False
