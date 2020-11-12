from tkinter import*#para toda a interface grafica
from gerargif import ImageLabel
from open_dataset import AbrirEEG
from threading import Thread 
import random
import time

class Janela_Treinamento():
    def __init__(self):     
        self.treinamento = Toplevel()  # é uma instancia de tk se a janela root for fechada ela tambpem será fechada
        self.treinamento.resizable(False, False) # ampliar a janela
        self.treinamento.title('Treinamento')
        self.treinamento['bg'] = '#86cee4'
        
        self.Lcontador=Label(self.treinamento, text='120/120',fg='black',bg= '#86cee4'  )
        self.Lcontador.grid(row=3, column=0, columnspan=2, padx=10,pady=10)  # centraliza o label na coluna
        
        self.gif_esq = ImageLabel(self.treinamento)
        self.gif_esq.grid(row=0, column=0)
        self.gif_esq.load('Imagens/esquerda.gif',10**8,self.Lcontador)
        self.Lesquerda=Label(self.treinamento, text='Mão Esquerda',font=('helvetica',20),fg='black',bg= '#86cee4'  )
        self.Lesquerda.grid(row=1, column=0, columnspan=1, padx=10,pady=10)  # posiciona leganda da mao esquerda
        
        self.gif_dir = ImageLabel(self.treinamento)
        self.gif_dir.grid(row=0, column=1)
        self.gif_dir.load('Imagens/direita.gif',10**8,self.Lcontador)
        self.Ldireita=Label(self.treinamento, text='Mão Direita',font=('helvetica',20),fg='black',bg= '#86cee4'  )
        self.Ldireita.grid(row=1, column=1, columnspan=1, padx=10,pady=10)  # posiciona leganda da mao direita
        
        
        
        Button(self.treinamento, text='Abrir EEG', width=20, bg='#f29cc2',fg='white',command=AbrirEEG).grid(row=4, column=0,columnspan=2,padx=10,pady=30)
        #Button(self.treinamento, text='Esquerda', width=20, bg='#0404B4',fg='white',command=self.ApenasEsquerda).grid(row=5, column=0,columnspan=1,padx=10,pady=30)
        #Button(self.treinamento, text='Direita', width=20, bg='#0404B4',fg='white',command=self.ApenasDireita).grid(row=5, column=1,columnspan=1,padx=10,pady=30)
        Button(self.treinamento, text='Iniciar', width=20, bg='#f8ef83',fg='black',command=self.IniciaDataSet).grid(row=5, column=0,columnspan=1,padx=10,pady=30)
        Button(self.treinamento, text='Parar!!!', width=20, bg='#f8ef83',fg='red',command=self.ParadeDeEmergencia).grid(row=5, column=1,columnspan=1,padx=10,pady=30)
        
        self.threadrunning=False
       
        self.treinamento.mainloop()
    '''
    def Start(self):
        tempo_inicial=time.time()#tempo inicial
        tempo=time.time()
        if((time.time()-tempo)>=1):#incremento de tempo
                acao['text'] = 2#int(time.time()-tempo_inicial)
                tempo=time.time()
       ''' 
    
    def Thread_DataSet(self):
        count=0
        while (count<120 and self.threadrunning):#roda o gif 120 vezes
            mao=random.randint(0,1)
            if (mao==0):#mao esquerda
                self.ApenasEsquerda()
                self.Lesquerda['fg']='green'
                self.Ldireita['fg']='black'
            elif (mao==1):#mao direita
                self.ApenasDireita()
                self.Ldireita['fg']='green'
                self.Lesquerda['fg']='black'
            count+=1
            self.Lcontador['text']='{}/120'.format(120-count)
            time.sleep(4)#tempo para imaginacao motora
            time.sleep(1.5+random.random())
    
    def IniciaDataSet(self):
        self.threadrunning=True
        self.t=Thread(target=self.Thread_DataSet)
        self.t.start()
    
    def ParadeDeEmergencia(self):
        self.threadrunning=False
                     
    def ApenasDireita(self):
        #self.gif_dir.unload()
        self.gif_dir.load('Imagens/direita.gif',100,self.Lcontador)
        #self.gif_esq.unload()
        #self.gif_esq.load('esquerda.gif',10**8,self.Lcontador)
    def ApenasEsquerda(self):
        #self.gif_dir.unload()
        #self.gif_dir.load('direita.gif',10**8,self.Lcontador)
        #self.gif_esq.unload()
        self.gif_esq.load('Imagens/esquerda.gif',100,self.Lcontador)

