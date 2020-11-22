from tkinter import *
import math, random, threading, time

class PlotPot:

    def __init__(self, root,class_share):
        self.gf = self.makeGraph(root)
        self.cf = self.makeControls(root)
        self.gf.pack()
        self.cf.pack()
        self.Reset()
        self._class_share=class_share
        
        #puxa a saida do EEG para todos os dados de treinamento e validacao
    def makeGraph(self, frame):
        self.sw = 1000#largura
        self.h = 300#altura 
        self.top = 2
        gf = Canvas(frame, width=self.sw, height=self.h+10,
                    bg="#002", bd=0, highlightthickness=0)
        gf.p = PhotoImage(width=2*self.sw, height=self.h)
        self.item = gf.create_image(0, self.top, image=gf.p, anchor=NW)
        return(gf)

    def makeControls(self, frame):
        cf = Frame(frame, borderwidth=1, relief="raised")
        Button(cf, text="Run", command=self.Run).grid(column=2, row=2)
        Button(cf, text="Stop", command=self.Stop).grid(column=4, row=2)
        Button(cf, text="Reset", command=self.Reset).grid(column=6, row=2)
        self.fps = Label(cf, text="0 fps")
        self.fps.grid(column=2, row=4, columnspan=5)
        return(cf)

    def Run(self):
        self.go = 1#variavel de estado
        for t in threading.enumerate():#chama a thread
            if t.name == "_gen_":
                print("already running")
                return
        threading.Thread(target=self.do_start, name="_gen_").start()

    def Stop(self):
        self.go = 0#variavel de estado
        for t in threading.enumerate():
            if t.name == "_gen_":
                t.join()

    def Reset(self):
        self.Stop()
        self.clearstrip(self.gf.p, '#345')

    def do_start(self):
        t = 0
        y2 = 0
        tx = time.time()
        while self.go:
            y1 = self._class_share.pot[t]*0
            #y1 = self.C3[i,j]*1e4#tentativa fixa, percorre apenas o tempo
            #y2 = self.CZ[i,j]*1e4
            #y3 = self.C4[i,j]*1e4#indices faz percorrer apenas os sinais das tentativas que cairam no teste
            self.scrollstrip(self.gf.p,
               (+y1),
               ( '#ff4'),
                 "" if t % 65 else "#088")

            t += 1
            if not t % 100:#de 100 em 100
                tx2 = time.time()
                self.fps.config(text='%d fps' % int(100/(tx2 - tx)))#calcula o fps
                tx = tx2
#            time.sleep(0.001)

    def clearstrip(self, p, color):  # Fill strip with background color
        self.bg = color              # save background color for scroll
        self.data = None             # clear previous data
        self.x = 0
        p.tk.call(p, 'put', color, '-to', 0, 0, p['width'], p['height'])

    def scrollstrip(self, p, data, colors, bar=""):   # Scroll the strip, add new data
        self.x = (self.x + 1) % self.sw               # x = double buffer position
        bg = bar if bar else self.bg
        p.tk.call(p, 'put', bg, '-to', self.x, 0,
                  self.x+1, self.h)
        p.tk.call(p, 'put', bg, '-to', self.x+self.sw, 0,
                  self.x+self.sw+1, self.h)
        self.gf.coords(self.item, -1-self.x, self.top)  # scroll to just-written column
        if not self.data:
            self.data = data
        
        y0 = int((self.h-1) * (1.0-self.data))   # plot all the data points
        y1 = int((self.h-1) * (1.0-data))
        ya, yb = sorted((y0, y1))#atribui o menor para ya e o maioe para yb
        for y in range(ya, yb+1):                   # connect the dots
            p.put(colors, (self.x,y))
            p.put(colors, (self.x+self.sw,y))
        self.data = data            # save for next call


# def main():
#     root = Tk()
#     root.title("StripChart")
#     class_share=general()
#     app = PlotPot(root,class_share)
#     root.mainloop()
    
# class general():
#     def __init__(self):
#         self.pot=[1,2,3,4,5,6,7,8,9,10]

# main()