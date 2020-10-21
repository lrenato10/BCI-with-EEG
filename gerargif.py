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
        self.objeto=objeto

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        self.delay = atraso#im.info['duration']#o padrao eh 100 ms

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames and self.loc<(len(self.frames)-1):
            self.loc += 1# de quanto em quantos frames
            #self.loc %= len(self.frames)# reinicia o vetor do frame quando ele chega no final
            self.config(image=self.frames[self.loc])#atualiza a a imagem do frame
            self.after(self.delay, self.next_frame)
            if self.loc%len(self.frames)==0:
                return
                self.count+=1
                self.objeto['text']=self.count
                print(self.count)
                
    def imprime_contador(self):
        return self.count

"""#root = tk.Tk()
lbl = ImageLabel(root)
lbl.pack()
lbl.load('esquerda.gif')
root.mainloop()"""