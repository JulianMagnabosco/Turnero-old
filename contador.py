import pygame,sys,pickle,threading
from pygame.locals import *

pygame.init()
flags = pygame.RESIZABLE
screen = pygame.display.set_mode((1024,720), flags)
pygame.display.set_caption("contador")

sound = pygame.mixer.Sound("music.wav")
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

buttons = list()

#clases
class Button:
    def __init__(self, text, action, parameter, bg="yellow"):
        self.font = font3
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.action = action
        self.parameter = parameter
        self.pressed = False
        self.bg = bg

    def show(self,  x,y):
        self.rect = pygame.Rect(x, y, screen.get_size()[0]/4-10,self.text.get_size()[1]+10)
        if self.pressed:
            pygame.draw.rect(screen, self.bg, self.rect, border_radius=5)
        else:
            pygame.draw.rect(screen, "blue", self.rect, border_radius=5)
        screen.blit(self.text, (x+screen.get_size()[0]/8-self.text.get_size()[0]/2, y))

    def clickdown(self):
        posX,posY = pygame.mouse.get_pos()
        if self.rect.collidepoint(posX,posY) and self.pressed != True:
            self.pressed = True
            self.action(self.parameter)

    def clickup(self):
        self.pressed = False


def addTicket (cola):
    if len(cola) > 0:
        cola.append(cola[-1]+1)
    else:
        cola.append(1)

def delTicket (cola):
    cola.pop(len(cola)-1)

def callTicket (cola):
    timer = threading.Timer(5,delTicket,[cola])
    timer.start()
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()

class Cola:
    def __init__(self, cola, pos, color):
        self.cola = cola
        self.pos = pos
        self.color = color
        self.buttonAdd = Button("Dar ticket",addTicket,cola)
        buttons.append(self.buttonAdd)
        self.buttonDel = Button("Quitar ticket",delTicket,cola)
        buttons.append(self.buttonDel)
        self.buttonCall = Button("Llamar ticket",callTicket,cola)
        buttons.append(self.buttonCall)

    def show(self):
        if self.cola == None:
            return
        firstRender = font2.render(str(len(self.cola))+" Turnos", 1, "black")
        realPos = self.pos*screen.get_size()[0]/4
        screen.blit(firstRender, (realPos + (screen.get_size()[0]/4-firstRender.get_size()[0])/2 ,0))

        postop = 70
        for n in self.cola:
            if n == self.cola[0]:
                render = font1.render(str(n), 1, "white")
            else:
                render = font2.render(str(n), 1, "white")
            rectFont = (realPos+5, postop+5, screen.get_size()[0]/4-5, render.get_size()[1])
            pygame.draw.rect(screen, self.color, rectFont, border_radius=5)
            screen.blit(render, (realPos + (screen.get_size()[0]/4-render.get_size()[0])/2, postop+5))
            postop += render.get_size()[1]+5
    
        self.buttonAdd.show(5+realPos, screen.get_size()[1]-firstRender.get_size()[1]*3)
        self.buttonDel.show(5+realPos, screen.get_size()[1]-firstRender.get_size()[1]*2)
        self.buttonCall.show(5+realPos, screen.get_size()[1]-firstRender.get_size()[1])

#metodos

colas = (Cola(colaC,0,(0,200,255)),
Cola(colaP,1,(0,200,0)),
Cola(colaOB,2,(255,0,0)))

def draw():
    screen.fill((255,255,255))

    pygame.draw.rect(screen, "green", (0,0,screen.get_size()[0],70))
    
    for c in colas:
        c.show()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            cargar()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                for button in buttons:
                    button.clickdown()
        if event.type == pygame.MOUSEBUTTONUP:
            for button in buttons:
                button.clickup()
    draw()
    pygame.display.flip()