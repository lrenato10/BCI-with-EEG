from gerargif import ImageLabel
from SVM.Class_Classifier import MyClassifier#importa o classificar
from SVM.Extraindo_Amostras_EEG import DataSetEEG
from SVM.BigDataSetEEG import ConcatenateDataSetEEG 
from Treinamento import Janela_Treinamento
from Instrucoes import Janela_Instrucoes
from Operacao import Janela_Operacao
from open_dataset import AbrirEEG
from tkinter import*#para toda a interface grafica
from tkinter import messagebox#para as caixas de mensagem
from tkinter import ttk#treeview eh um metodo de ttk
import time
#bilbioteca para por a imagem
import PIL as p
import PIL.ImageTk as ptk
import random
from threading import Thread 


classifier=MyClassifier(4,4)#cria o DATASET do indivíduo 1 até o 9

class Janela_Carregamento():
    def __init__(self):#metodo construtor, é sempre executado quando chama a classe
        #self é um escopo geral da variavel, pode usar self.x em todos os metodos pq deixa de ser var local
        self.carregamento=Tk()
        self.carregamento.title('EEG')
        self.carregamento['bg'] = '#524f4f'
        self.pic = 'Imagens/Imagem IB1 projeto final.png'
        self.pic1 = p.Image.open(self.pic)
        self.photo = ptk.PhotoImage(self.pic1)
        labelImage = Label(self.carregamento, image=self.photo)
        labelImage.grid(row=0, column=0)
        Label(self.carregamento, text='V 1.0',fg='white',bg= '#524f4f'  ).grid(row=0, column=0, columnspan=2, padx=10,pady=10)  # centraliza o label na coluna
        self.carregamento.after(2000, self.destroi)
        self.carregamento.mainloop()
        
    def destroi(self):
        self.carregamento.destroy()
        Janela_Opcoes(classifier)
        
        
class Janela_Opcoes():
    def __init__(self,classifier):#metodo construtor, é sempre executado quando chama a classe
        #self é um escopo geral da variavel, pode usar self.x em todos os metodos pq deixa de ser var local
        self.opcoes=Tk()
        self.opcoes.title('Opções')
        self.opcoes['bg'] = '#86cee4'
        self.opcoes.resizable(True, True)
        Label(self.opcoes, font=('helvetica',20), text='Selecione uma das opções',fg='black',bg= '#86cee4'  ).grid(row=0, column=0, columnspan=1, padx=10,pady=10) # centraliza o label na coluna
        Button(self.opcoes, font=('helvetica',15),text='Treinamento',width=15, height=2, relief=GROOVE, bg='#f29cc2',fg='black',command=Janela_Treinamento).grid(row=1, column=0, padx=70, pady=40)#cOres criadas em https://html-color-codes.info/
        Button(self.opcoes, font=('helvetica', 15), text='Operação', width=15, height=2, relief=GROOVE ,bg='#f29cc2',fg='black',command=lambda : Janela_Operacao(classifier)).grid(row=2, column=0, padx=70, pady=40)
        Button(self.opcoes, font=('helvetica', 15), text='Instruções', width=15, height=2, relief=GROOVE, bg='#f29cc2',fg='black',command=Janela_Instrucoes).grid(row=3, column=0,padx=70,pady=40)
        self.opcoes.mainloop()
    

    
Janela=Janela_Carregamento()