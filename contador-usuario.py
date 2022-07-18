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


#clases
class Button:
    def __init__(self, text, action, bg="yellow"):
        self.font = font3
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.action = action
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
            self.action()

    def clickup(self):
        self.pressed = False

class Cola:
    def __init__(self, cola, pos, color):
        self.pos = pos
        self.color = color
        if cola == "C":
            self.cola = colaC
        elif cola == "P":
            self.cola = colaP
        elif cola == "OB":
            self.cola = colaOB
        self.buttonAdd = Button("Dar ticket",self.addTicket)
        buttons.append(self.buttonAdd)
        self.buttonDel = Button("Quitar ticket",self.delTicket)
        buttons.append(self.buttonDel)
        self.buttonCall = Button("Llamar ticket",self.callTicket)
        buttons.append(self.buttonCall)
        self.called = False

    def show(self):
        if self.cola == None:
            return
        #numero de turnos
        realPos = self.pos*screen.get_size()[0]/4
        firstRender = font2.render(str(len(self.cola))+" Turnos", 1, "black")
        screen.blit(firstRender, (realPos + (screen.get_size()[0]/4-firstRender.get_size()[0])/2 ,40))
        firstRender = font2.render("Clinica", 1, "black")
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
    
        self.buttonAdd.show(5+realPos, screen.get_size()[1]-firstRender.get_size()[1]*3)
        self.buttonDel.show(5+realPos, screen.get_size()[1]-firstRender.get_size()[1]*2)
        self.buttonCall.show(5+realPos, screen.get_size()[1]-firstRender.get_size()[1])

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

def draw():
    screen.fill((255,255,255))

    pygame.draw.rect(screen, (200,200,200), (0,0,screen.get_size()[0],100))
    
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