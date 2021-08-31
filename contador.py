import pygame,sys,time,pickle
from pygame.locals import *



pygame.init()
flags = pygame.RESIZABLE
screen = pygame.display.set_mode((1024,720), flags)
pygame.display.set_caption("contador")

archive = open("config","ab+")
archive.seek(0)
config = None
try:
    config = pickle.load(archive)
except:
    print("error")
finally:
    archive.close()
sound = pygame.mixer.Sound("music.wav")
font1 = pygame.font.SysFont("Arial", 100)
font2 = pygame.font.SysFont("Arial", 50)
font3 = pygame.font.SysFont("Arial", 30)

colaC = list((1,2,3))
colaP = list((1,2,3))
colaOB = list((1,2,3))
colorColaC = 0,200,255
colorColaP = 0,200,0
colorColaOB = 255,0,0

#clases
class Button:
    def __init__(self, text, action, parameter, bg="yellow"):
        self.font = font3
        self.textRaw = text
        self.text = self.font.render(self.textRaw, 1, pygame.Color("White"))
        self.size = (screen.get_size()[0]/4,self.text.get_size()[1]+10)
        self.action = action
        self.parameter = parameter
        self.pressed = False
        self.bg = bg

    def show(self,  x,y):
        self.rect = pygame.Rect(x-  self.size[0]/2+5, y-  self.size[1]/2, self.size[0]-10, self.size[1])
        if self.pressed:
            pygame.draw.rect(screen, self.bg, self.rect, border_radius=5)
        else:
            pygame.draw.rect(screen, "blue", self.rect, border_radius=5)
        screen.blit(self.text, (x-self.text.get_size()[0]/2, y-self.text.get_size()[1]/2))

    def clickdown(self):
        self.pressed = False
        posX,posY = pygame.mouse.get_pos()

        if self.rect.collidepoint(posX,posY):
            self.pressed = True
            self.action(self.parameter)
    def clickup(self):
        print("asd")
        self.pressed = False

#metodos

def addTicket (listN):
    if listN == 1:
        if len(colaC) > 0:
            colaC.append(colaC[-1]+1)
        else:
            colaC.append(1)
    elif listN == 2:
        if len(colaP) > 0:
            colaP.append(colaP[-1]+1)
        else:
            colaP.append(1)
    else:
        if len(colaOB) > 0:
            colaOB.append(colaOB[-1]+1)
        else:
            colaOB.append(1)

def callTicket ():
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()

def nextTicket ():
    if len(colaC) > 0:
        if len(colaC) == 0:
            colaC.clear()
        else:
            callTicket()
        colaC.pop(0)
        callTicket()

def resetTicket ():
    colaC.clear()
    colaC.append(1)

def draw():
    screen.fill((255,255,255))

    posTop = 70
    pygame.draw.rect(screen, "green", (0,0,screen.get_size()[0],posTop))
    
    posButton = 5
    for button in buttons:
        button.show(posButton+button.size[0]/2, screen.get_size()[1]-button.size[1]-5)
        posButton += button.size[0] 
    
    if colaC == None:
        return
    render = font2.render(str(len(colaC))+" Turnos", 1, "black")
    screen.blit(render, (screen.get_size()[0] / 2 - render.get_size()[0] / 2,0))

    posTopC = posTopP = posTopOB = posTop
    for n in colaC:
        if n == colaC[0]:
            render = font1.render(str(n), 1, "white")
        else:
            render = font2.render(str(n), 1, "white")
        rectFont = (5, posTopC+5, screen.get_size()[0]/4-5, render.get_size()[1])
        pygame.draw.rect(screen, colorColaC, rectFont, border_radius=5)
        screen.blit(render, (screen.get_size()[0] / 8 - render.get_size()[0] / 2, posTopC+5))
        posTopC += render.get_size()[1]+5
        
    for n in colaP:
        if n == colaP[0]:
            render = font1.render(str(n), 1, "white")
        else:
            render = font2.render(str(n), 1, "white")
        rectFont = (screen.get_size()[0]/4+5, posTopP+5, screen.get_size()[0]/4-5, render.get_size()[1])
        pygame.draw.rect(screen, colorColaP, rectFont, border_radius=5)
        screen.blit(render, (screen.get_size()[0] / 8*3 - render.get_size()[0] / 2, posTopP+5))
        posTopP += render.get_size()[1]+5
    
    for n in colaOB:
        if n == colaOB[0]:
            render = font1.render(str(n), 1, "white")
        else:
            render = font2.render(str(n), 1, "white")
        rectFont = (screen.get_size()[0]/2+5, posTopOB+5, screen.get_size()[0]/4-5, render.get_size()[1])
        pygame.draw.rect(screen, colorColaOB, rectFont, border_radius=5)
        screen.blit(render, (screen.get_size()[0] / 8*5 - render.get_size()[0] / 2, posTopOB+5))
        posTopOB += render.get_size()[1]+5

buttons = {
    Button("Dar Turno C",addTicket, 1),
    Button("Dar Turno P",addTicket, 2),
    Button("Dar Turno OB",addTicket, 3)
}

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                for button in buttons:
                    button.clickdown()
        if event.type == pygame.MOUSEBUTTONUP:
            for button in buttons:
                button.clickup()
    draw()
    pygame.display.flip()