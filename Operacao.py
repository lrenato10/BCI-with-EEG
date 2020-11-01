from tkinter import*#para toda a interface grafica
from gerargif import ImageLabel
from open_dataset import AbrirEEG
from threading import Thread 
import random
import time

class Janela_Operacao():
    def __init__(self): 
        self.operacao = Toplevel()  # é uma instancia de tk se a janela root for fechada ela tambpem será fechada
        self.operacao.resizable(False, False) # ampliar a janela
        self.operacao.title('Operação')
        self.operacao['bg'] = '#86cee4'
        
        