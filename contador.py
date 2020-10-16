# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 18:14:01 2020

@author: Luiz Renato
"""


from tkinter import*

root = Tk()

def tick(validador = False,sec = None):
    if validador == False:
        sec = 10
    if sec == 0:
        time['text'] = 'TEMPO ESGOTADO'
    else:
        sec = sec - 1
        time['text'] = sec
        time.after(1000, lambda : tick(True,sec))#atualiza de 1000 em 1000 ms (1 s)


time = Label(root, fg='green')
time.grid(row=2, column=0)
Button(root, fg='blue', text='Start', command=tick).grid(row=3, column=0)

root.mainloop()