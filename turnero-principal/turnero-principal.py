import pygame,sys,pickle,threading
from conection_server import ConectionServer
from pygame.locals import *

pygame.init()
flags = pygame.RESIZABLE 
info = pygame.display.Info()
w = 1024
h = 800
screen = pygame.display.set_mode((w,h), flags)
pygame.display.set_caption("Turnero Principal")

sound = pygame.mixer.Sound("./music.wav")
font1 = pygame.font.SysFont("Arial", 100)
font2 = pygame.font.SysFont("Arial", 50)
font3 = pygame.font.SysFont("Arial", 30)

colaC = list((1,2,3))
colaP = list((1,2,3))
colaOB = list((1,2,3))
archive = open("list","ab+")

try:
    archive.seek(0)
    colaC = pickle.load(archive)
    colaP = pickle.load(archive)
    colaOB = pickle.load(archive)
except:
    print("error")
finally:
    archive.close()

def cargar():
    archive = open("list","wb")
    try:
        pickle.dump(colaC,archive)
        pickle.dump(colaP,archive)
        pickle.dump(colaOB,archive)
    except:
        print("error")
    finally:
        archive.close()


#clases

class Cola:
    def __init__(self, cola, pos, color):
        self.pos = pos
        self.color = color
        if cola == "C":
            self.cola = colaC
            self.name = "Clinica"
        elif cola == "P":
            self.cola = colaP
            self.name = "Pediatria"
        elif cola == "OB":
            self.cola = colaOB
            self.name = "OB"
        self.called = False

    def show(self):
        if self.cola == None:
            return
        #numero de turnos
        realPos = self.pos*screen.get_size()[0]/4
        firstRender = font2.render(str(len(self.cola))+" Turnos", 1, "black")
        screen.blit(firstRender, (realPos + (screen.get_size()[0]/4-firstRender.get_size()[0])/2 ,40))
        firstRender = font2.render(self.name, 1, "black")
        screen.blit(firstRender, (realPos + (screen.get_size()[0]/4-firstRender.get_size()[0])/2 ,0))

        #turnos
        postop = 100
        for n in self.cola:
            if n == self.cola[0]:
                render = font1.render(str(n), 1, "white")
                colorAdd = 125 * (int(pygame.time.get_ticks()/500) % 2)
                if self.called :
                    realColor = [(x+colorAdd if x+colorAdd < 255 else 255) for x in self.color] 
                    pygame.draw.rect(screen, "black", (realPos, postop, screen.get_size()[0]/4+5, render.get_size()[1]+10), border_radius=5)
                else :
                    realColor =self.color
            else:
                render = font2.render(str(n), 1, "white")
                realColor = self.color
            rectFont = (realPos+5, postop+5, screen.get_size()[0]/4-5, render.get_size()[1])
            pygame.draw.rect(screen, realColor, rectFont, border_radius=5)
            screen.blit(render, (realPos + (screen.get_size()[0]/4-render.get_size()[0])/2, postop+5))
            postop += render.get_size()[1]+5

    def addTicket (self):
        self.cola.append(self.cola[-1]+1)

    def delTicket (self):
        if len(self.cola) > 0:
            self.cola.pop(len(self.cola)-1)

    def _callTicket (self):
        self.cola.pop(0)
        self.called -= 1
    
    def callTicket (self):
        if len(self.cola) > 0:
            self.called += 1
            timer = threading.Timer(5,self._callTicket)
            timer.start()
            pygame.mixer.stop()
            pygame.mixer.Sound.play(sound)
#metodos

buttons = list()
colas = (Cola("C", 0, (0,155,200)),
Cola("P", 1, (0,155,0)),
Cola("OB", 2, (155,0,0)))


def update(rawMessage):
    message = str(rawMessage).strip("['']")
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            cargar()
            sys.exit()
    screen.fill((255,255,255))
    if message != "":
        if message[1:] == "C":
            selectedCola = colas[0]
        elif message[1:] == "P":
            selectedCola = colas[1]
        else :
            selectedCola = colas[2]

        if message[0] == "0":
            selectedCola.addTicket()
        elif message[0] == "1":
            selectedCola.delTicket()
        elif message[0] == "2":
            selectedCola.callTicket()
        print(message)
    
    pygame.draw.rect(screen, (200,200,200), (0,0,screen.get_size()[0],100))
    
    for c in colas:
        c.show()
    pygame.display.flip()
    return str(colaC)+str(colaP)+str(colaOB)

conexion = ConectionServer(update,cargar)
introScreen = font2.render("Esperando a que se conecten clientes", 1, "white")
screen.blit(introScreen, (400,400))
pygame.display.flip()
conexion.loop(str(colaC)+str(colaP)+str(colaOB))
