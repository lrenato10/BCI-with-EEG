from gerargif import ImageLabel
from tkinter import*#para toda a interface grafica
from tkinter import messagebox#para as caixas de mensagem
from tkinter import ttk#treeview eh um metodo de ttk
import time
#bilbioteca para por a imagem
import PIL as p
import PIL.ImageTk as ptk

class Janela_Carregamento():
    def __init__(self):#metodo construtor, é sempre executado quando chama a classe
        #self é um escopo geral da variavel, pode usar self.x em todos os metodos pq deixa de ser var local
        self.carregamento=Tk()
        self.carregamento.title('EEG')
        self.carregamento['bg'] = '#524f4f'
        pic = 'Imagem IB1 projeto final.png'
        pic1 = p.Image.open(pic)
        photo = ptk.PhotoImage(pic1)
        labelImage = Label(self.carregamento, image=photo)
        labelImage.grid(row=0, column=0)
        Label(self.carregamento, text='V 1.0',fg='white',bg= '#524f4f'  ).grid(row=0, column=0, columnspan=2, padx=10,pady=10)  # centraliza o label na coluna
        self.carregamento.after(50, self.destroi)
        self.carregamento.mainloop()
        
    def destroi(self):
        self.carregamento.destroy()
        Janela_Opcoes()
        
        
class Janela_Opcoes():
    def __init__(self):#metodo construtor, é sempre executado quando chama a classe
        #self é um escopo geral da variavel, pode usar self.x em todos os metodos pq deixa de ser var local
        self.opcoes=Tk()
        self.opcoes.title('Janela de opções')
        self.opcoes['bg'] = '#524f4f'
        self.count=1
        Label(self.opcoes, text='Selecione Uma das Opções',fg='white',bg= '#524f4f'  ).grid(row=0, column=0, columnspan=1, padx=10,pady=10)  # centraliza o label na coluna
        Button(self.opcoes, text='Treinamento',width=20, bg='#0404B4',fg='white',command=self.Treinamento).grid(row=1, column=0, padx=50, pady=20)#cares criadas em https://html-color-codes.info/
        Button(self.opcoes, text='Operação', width=20, bg='#0404B4',fg='white',command=self.Operacao).grid(row=2, column=0, padx=50, pady=20)
        Button(self.opcoes, text='Instruções', width=20, bg='#0404B4',fg='white',command=self.Instrucoes).grid(row=3, column=0,padx=50,pady=20)
        self.opcoes.mainloop()
    

    #=============================================Janela de Treinamento=================================================
    def Treinamento(self):
        self.treinamento = Toplevel()  # é uma instancia de tk se a janela root for fechada ela tambpem será fechada
        self.treinamento.resizable(False, False) # ampliar a janela
        self.treinamento.title('Treinamento')
        self.treinamento['bg'] = '#8A0808'
        picEsquerda = 'Imagem IB1 projeto final.png'
        picEsquerda1 = p.Image.open(picEsquerda)
        photo = ptk.PhotoImage(picEsquerda1)
        labelImage = Label(self.carregamento, image=photo)
        labelImage.grid(row=0, column=0)
        picDireita = 'Imagem IB1 projeto final.png'
        picDireita1 = p.Image.open(picDireita)
        photo = ptk.PhotoImage(pic1)
        labelImage = Label(self.carregamento, image=photo)
        labelImage.grid(row=0, column=1)
        Button(self.instrucoes, text='Abrir EEG', width=20, bg='#0404B4',fg='white',command=self.AbrirEEG).pack(side=LEFT)

    def AbrirEEG(self):
        pass
        


    def Operacao(self):
        self.operacao = Toplevel()  # é uma instancia de tk se a janela root for fechada ela tambpem será fechada
        self.operacao.resizable(False, False) # ampliar a janela
        self.operacao.title('Operação')
        self.operacao['bg'] = '#8A0808'
        gif = ImageLabel(self.operacao)
        gif.pack()
        gif.load('direita.gif')

        gif = ImageLabel(self.operacao)
        gif.pack()
        gif.load('esquerda.gif')


    #==============================================Janela de Instruções================================================
    def Instrucoes(self):
        self.instrucoes = Toplevel()  # é uma instancia de tk se a janela root for fechada ela tambpem será fechada
        #self.instrucoes.resizable(False, False) # ampliar a janela
        #self.instrucoes.geometry('700x340')
        self.instrucoes.title('Instruções')
        self.instrucoes['bg'] = '#86cee4'
        self.L1=Label(self.instrucoes, text='1/5',fg='white',bg= '#86cee4'  )
        self.L1.pack()
        self.L2=Label(self.instrucoes, text='Conecte o microcontrolador a entrada USB do computador',fg='black',bg= '#86cee4',width=80,height=20 )
        self.L2.pack()
        Button(self.instrucoes, text='Próxima', width=20, bg='#f29cc2',fg='black',command=self.Incremento).pack(side=RIGHT)
        Button(self.instrucoes, text='Anterior', width=20, bg='#f29cc2',fg='black',command=self.Decremento).pack(side=LEFT)
        
        self.instrucoes.mainloop()
        
    def Comparacao(self):
        self.L1['text'] = '{}/5'.format(self.count)
        if (self.count==1):
            self.L2['text']='Conecte o microcontrolador a entrada USB do computador'
        elif (self.count==2):
            self.L2['text']='Coloque os eletrodos nas posições CZ, C3 e C4.\n Não se esqueça da referência!'
        elif (self.count==3):
            self.L2['text']='Caso você queira treinar a inteligência artificial,\n clique em "Treinamento \n  aaaaaaaaaaaaaaa \n'
        elif (self.count==4):
            self.L2['text']='Siga com atenção as instruções da aba "Treinamentos"'
        elif (self.count==5):
            self.L2['text']='frase 5'
        
    def Incremento(self):
        if ((self.count >=1 )& (self.count <5)):
            self.count=self.count+1
            self.Comparacao()

    def Decremento(self):
        if ((self.count >1) & (self.count <=5)):
            self.count=self.count-1
            self.Comparacao()
        
            
Janela=Janela_Carregamento()