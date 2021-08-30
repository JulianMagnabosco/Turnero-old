import sys,pickle
import tkinter as tk
from tkinter import messagebox

screen = tk.Tk("configurar")
screen.title('Configurar')
frameTop = tk.Frame(screen)
frameBot = tk.Frame(screen)
frameTop.pack()
frameBot.pack()

jumps = 0
class section ():
    def __init__(self, name,number=False):
        global jumps
        self.maxchar = 20
        self.number = number
        self._name = name
        self.name = tk.Label(frameTop,text=name+":")
        self.name.grid(row=0+jumps,column=0,padx=20,pady=10, sticky=tk.E)
        
        self.text = tk.StringVar()
        self.entry = tk.Entry(frameTop, textvariable = self.text)
        self.text.trace("w", self._update)
        self.entry.grid(row=0+jumps,column=1)
        jumps+=1
    def _update(self,*args):
        if len(self.text.get()) > self.maxchar:
            self.entry.delete(self.maxchar)
        if self.number and not self.text.get().isnumeric():
            self.entry.delete(0)

columnjump = 0
class button ():
    def __init__(self, name, method):
        global columnjump
        self._button = tk.Button(frameBot, text=name, command=method,padx=5,pady=5)
        self._button.grid(row = 0+jumps+1, column = columnjump,padx=10,pady=10)
        columnjump +=1

#metodos
def Update():
    print(config)
    archive = open("config","wb")
    config.clear()
    for section in configSections:
        config.update({section : configSections[section].text.get()})
    pickle.dump(config, archive)
    archive.close()

#secciones
configSections = {
    "timer" : section("Segundos entre llamadas",True)
}

config = dict()

archive = open("config","ab+")
archive.seek(0)
try:
    config = pickle.load(archive)
    for section in configSections:
        print(config[section])
        configSections[section].text.set(config[section])
except:
    print("error")
finally:
    archive.close()

ButtonUpdate = button("Update", Update)
if __name__ == "__main__":
    screen.mainloop()