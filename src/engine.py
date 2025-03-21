import pygame
from pygame.locals import *

def setup():
        # pygame setup
    pygame.init()
    
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

class Button:
    def __init__(self,screen,font, text, action, actionArgs, bg="yellow"):
        self.screen = screen
        self.font = font
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.action = action
        self.actionArgs = actionArgs
        self.pressed = False
        self.bg = bg

    def show(self,  x,y):
        self.rect = pygame.Rect(x, y, self.screen.get_size()[0]/4-10,self.text.get_size()[1]+10)
        if self.pressed:
            pygame.draw.rect(self.screen, self.bg, self.rect, border_radius=5)
        else:
            pygame.draw.rect(self.screen, "blue", self.rect, border_radius=5)
        self.screen.blit(self.text, (x+self.screen.get_size()[0]/8-self.text.get_size()[0]/2, y))

    def clickdown(self):
        posX,posY = pygame.mouse.get_pos()
        if self.rect.collidepoint(posX,posY) and self.pressed != True:
            self.pressed = True
            self.action(self.actionArgs)

    def clickup(self):
        self.pressed = False

class Line:
    def __init__(self, name, pos, color, line,screen,font,font2,tasks,threading, buttonList,sound):
        self.pos = pos
        self.color = color
        self.sound = sound
        self.screen = screen
        self.font = font
        self.font2 = font2
        self.tasks = tasks
        self.threading = threading
        if name == "C":
            self.line = line
            self.name = "Clinica"
        elif name == "P":
            self.line = line
            self.name = "Pediatria"
        elif name == "OB":
            self.line = line
            self.name = "OB"
        self.buttonAdd = Button(self.screen,self.font,"Dar ticket",self.addTicket,line)
        buttonList.append(self.buttonAdd)
        self.buttonDel = Button(self.screen,self.font,"Quitar ticket",self.delTicket,line)
        buttonList.append(self.buttonDel)
        self.buttonCall = Button(self.screen,self.font,"Llamar ticket",self.callTicket,line)
        buttonList.append(self.buttonCall)
        self.called = False

    def show(self):
        if self.line == None:
            return
        #numero de turnos
        realPos = self.pos*self.screen.get_size()[0]/4
        firstRender = self.font.render(str(len(self.line))+" Turnos", 1, "black")
        self.screen.blit(firstRender, (realPos + (self.screen.get_size()[0]/4-firstRender.get_size()[0])/2 ,40))
        firstRender = self.font.render(self.name, 1, "black")
        self.screen.blit(firstRender, (realPos + (self.screen.get_size()[0]/4-firstRender.get_size()[0])/2 ,0))

        #turnos
        postop = 100
        for n in self.line:
            if n == self.line[0]:
                render = self.font2.render(str(n), 1, "white")
                colorAdd = 125 * (int(pygame.time.get_ticks()/500) % 2)
                if self.called :
                    realColor = [(x+colorAdd if x+colorAdd < 255 else 255) for x in self.color] 
                    pygame.draw.rect(self.screen, "black", (realPos, postop, self.screen.get_size()[0]/4+5, render.get_size()[1]+10), border_radius=5)
                else :
                    realColor =self.color
            else:
                render = self.font.render(str(n), 1, "white")
                realColor = self.color
            rectFont = (realPos+5, postop+5, self.screen.get_size()[0]/4-5, render.get_size()[1])
            pygame.draw.rect(self.screen, realColor, rectFont, border_radius=5)
            self.screen.blit(render, (realPos + (self.screen.get_size()[0]/4-render.get_size()[0])/2, postop+5))
            postop += render.get_size()[1]+5
    
        self.buttonAdd.show(5+realPos, self.screen.get_size()[1]-firstRender.get_size()[1]*3)
        self.buttonDel.show(5+realPos, self.screen.get_size()[1]-firstRender.get_size()[1]*2)
        self.buttonCall.show(5+realPos, self.screen.get_size()[1]-firstRender.get_size()[1])

    def addTicket (self,nomCola):
        if len(self.line) > 0:
            self.line.append(self.line[-1]+1)
            self.tasks.append("0"+nomCola)

    def delTicket (self,nomCola):
        if len(self.line) > 0:
            self.line.pop(len(self.line)-1)
            self.tasks.append("1"+nomCola)

    def _callTicket (self):
        self.line.pop(0)
        self.called -= 1
    
    def callTicket (self,nomCola):
        if len(self.line) > 0:
            self.called += 1
            timer = self.threading.Timer(5,self._callTicket)
            timer.start()
            self.tasks.append("2"+nomCola)
            pygame.mixer.stop()
            pygame.mixer.Sound.play(self.sound)