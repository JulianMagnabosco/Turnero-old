import pygame,sys,time
from pygame.locals import *

startTime = time.time()
timer = (time.time() - startTime) / 5
pause = False
pygame.init()
flags = pygame.RESIZABLE
screen = pygame.display.set_mode((1024,720), flags)
pygame.display.set_caption("contador")
sound = pygame.mixer.Sound("music.wav")
font1 = pygame.font.SysFont("Arial", 100)
font2 = pygame.font.SysFont("Arial", 50)
font3 = pygame.font.SysFont("Arial", 30)
colorBF = 0,200,255

cola = list((1,2,3))

#clases
class Button:
    def __init__(self, text, action, bg="yellow"):
        self.font = font3
        self.textRaw = text
        self.text = self.font.render(self.textRaw, 1, pygame.Color("White"))
        self.size = (screen.get_size()[0]/3,self.text.get_size()[1]+10)
        self.action = action
        self.pressed = False
        self.bg = bg

    def show(self,  x,y):
        self.rect = pygame.Rect(x-  self.size[0]/2, y-  self.size[1]/2, self.size[0], self.size[1])
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
            self.action()
    def clickup(self):
        print("asd")
        self.pressed = False

#metodos

def pause ():
    global pause
    pause = not pause
    
def addTicket ():
    if len(cola) > 0:
        cola.append(cola[-1]+1)
    else:
        cola.append(1)

def callTicket ():
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()

def nextTicket ():
    if len(cola) > 0:
        if len(cola) == 0:
            cola.clear()
        else:
            callTicket()
        cola.pop(0)
        callTicket()

def resetTicket ():
    cola.clear()
    cola.append(1)

def draw():
    global startTime, timer
    screen.fill((255,255,255))

    posTop = 120
    pygame.draw.rect(screen, "green", (0,0,screen.get_size()[0],posTop))

    if pause: 
        timer = (time.time() - startTime) / 5
    print(timer)
    pygame.draw.rect(screen, "blue", (0,0,screen.get_size()[0]*timer,10))
    
    if timer > 1:
        startTime = time.time()
        nextTicket ()

    posButton = posTop + 5
    for button in buttons:
        button.show(screen.get_size()[0] * 0.75, button.size[1]/2 + posButton)
        posButton += button.size[1] + 5
    
    if cola == None:
        return
    render = font1.render(str(len(cola)), 1, "white")
    screen.blit(render, (screen.get_size()[0] / 2 - render.get_size()[0] / 2,0))
    for n in cola:
        if n == cola[0]:
            render = font1.render(str(n), 1, "white")
        else:
            render = font2.render(str(n), 1, "white")
        rectFont = (5, posTop+5, screen.get_size()[0]/2-5, render.get_size()[1])
        pygame.draw.rect(screen, colorBF, rectFont, border_radius=5)
        screen.blit(render, (screen.get_size()[0] / 4 - render.get_size()[0] / 2,posTop+5))
        posTop += render.get_size()[1]+5

buttons = {
    Button("Llamar y quitar",nextTicket),
    Button("Resetear todo",resetTicket),
    Button("Pausar",pause),
    Button("Agregar Turno",addTicket)
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