import tkinter as tk
from PIL import Image, ImageTk
from itertools import count



class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""    
    def load(self, im,atraso,objeto):
        if isinstance(im, str):
            im = Image.open(im)
        self.count = 0
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = atraso#im.info['duration']#o padrao eh 100 ms
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame(objeto)

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self,objeto):
        if self.frames:
            self.loc += 1# de quanto em quantos frames
            self.loc %= len(self.frames)# reinicia o vetor do frame quando ele chega no final
            self.config(image=self.frames[self.loc])#atualiza a a imagem do frame
            self.after(self.delay, self.next_frame)
            if self.loc%len(self.frames)==0:
                self.count+=1
                self.imprime_contador()
                print(self.count)
                objeto['text']=str(self.count)
                
   # def imprime_contador(self):
    #    return self.count

"""#root = tk.Tk()
lbl = ImageLabel(root)
lbl.pack()
lbl.load('esquerda.gif')
root.mainloop()"""