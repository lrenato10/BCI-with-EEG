from tkinter import *
import math, random, threading, time

class StripChart:

    def __init__(self, root,Y,indices):
        self.gf = self.makeGraph(root)
        self.gf['bg'] = '#86cee4'
        self.cf = self.makeControls(root)
        self.cf['bg'] = '#86cee4'
        self.gf.pack()
        self.cf.pack()
        self.Reset()
        self.indices=indices.astype(int)#indices dos dados va validacao na ordem deles
        #puxa a saida do EEG para todos os dados de treinamento e validacao
        self.C3=Y[:,:,0]
        self.CZ=Y[:,:,1]
        self.C4=Y[:,:,2]
        self.Run()#inicia o plot
    def makeGraph(self, frame):
        self.sw = 1000#largura
        self.h = 400#altura 
        self.top = 2
        gf = Canvas(frame, width=self.sw, height=self.h+10,
                    bg="#002", bd=0, highlightthickness=0)
        gf.p = PhotoImage(width=2*self.sw, height=self.h)
        self.item = gf.create_image(0, self.top, image=gf.p, anchor=NW)
        return(gf)

    def makeControls(self, frame):
        cf = Frame(frame, borderwidth=1, relief="raised")
        #Button(cf, text="Run", command=self.Run).grid(column=2, row=2)
        #Button(cf, text="Stop", command=self.Stop).grid(column=4, row=2)
        #Button(cf, text="Reset", command=self.Reset).grid(column=6, row=2)
        self.fps = Label(cf, text="0 fps",bg='#86cee4')
        self.fps.grid(column=2, row=1, columnspan=5)
        self.C3label = Label(cf, text=" C3 ",fg='blue',bg='#86cee4')
        self.C3label.grid(column=0, row=2, columnspan=1)
        self.Czlabel = Label(cf, text=" CZ ",fg='red',bg='#86cee4')
        self.Czlabel.grid(column=3, row=2, columnspan=1)
        self.C4label = Label(cf, text=" C4 ",fg='yellow',bg='#86cee4')
        self.C4label.grid(column=5, row=2, columnspan=1)
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
        i=0#tentativa
        j=0#tempo
        t = 0
        y2 = 0
        tx = time.time()
        while self.go:
            y1 = self.C3[self.indices[i],j]*1e4/2#tentativa fixa, percorre apenas o tempo
            y2 = self.CZ[self.indices[i],j]*1e4/2
            y3 = self.C4[self.indices[i],j]*1e4/2#indices faz percorrer apenas os sinais das tentativas que cairam no teste
            #y1 = self.C3[i,j]*1e4#tentativa fixa, percorre apenas o tempo
            #y2 = self.CZ[i,j]*1e4
            #y3 = self.C4[i,j]*1e4#indices faz percorrer apenas os sinais das tentativas que cairam no teste
            self.scrollstrip(self.gf.p,
               (0.25+y1, 0.5+y2, 0.75+y3),
               ( '#ff4', '#f40', '#4af'),
                 "" if t % 65 else "#088")
            j+=1#atualiza o tempo
            if j==250*2:#altera a tentativa a reseta o tempo
                j=0#rezeta o tempo
                i+=1
                print(i)
                print(self.indices[i])
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
        for d in range(len(data)):
            y0 = int((self.h-1) * (1.0-self.data[d]))   # plot all the data points
            y1 = int((self.h-1) * (1.0-data[d]))
            ya, yb = sorted((y0, y1))#atribui o menor para ya e o maioe para yb
            for y in range(ya, yb+1):                   # connect the dots
                p.put(colors[d], (self.x,y))
                p.put(colors[d], (self.x+self.sw,y))
        self.data = data            # save for next call

#def main():
#    root = Tk()
#    root.title("StripChart")
#    app = StripChart(root)
#    root.mainloop()

#main()